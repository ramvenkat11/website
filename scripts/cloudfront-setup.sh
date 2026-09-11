#!/usr/bin/env bash
# One-time CloudFront and S3 setup for search engine friendliness. Safe to re-run.
#
#   1. Publishes scripts/cloudfront-canonical-host.js as the CloudFront Function
#      "search2o-canonical-host" and attaches it to the distribution's viewer-request event:
#      www.search2o.com and docs.search2o.com redirect (301) to search2o.com.
#   2. Maps the origin's 403 and 404 answers to a real 404 status with /404.html as the body.
#   3. Makes 404.html the bucket's error document (it was index.html).
#
#   scripts/cloudfront-setup.sh          apply
#   scripts/cloudfront-setup.sh --wait   apply, then wait until the distribution reports Deployed
#
# Requires AWS credentials for account 406848153313. Deploy the site first (scripts/deploy.sh --go)
# so that /404.html exists in the bucket.
set -euo pipefail

BUCKET="search2o.com"
DISTRIBUTION="E330RKTBY31L8X"
AWS_ACCOUNT="406848153313"
FUNCTION_NAME="search2o-canonical-host"
ERROR_PAGE="/404.html"
DEPLOY_POLL_SECONDS=20
DEPLOY_MAX_WAIT_SECONDS=1200

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODE="$ROOT/scripts/cloudfront-canonical-host.js"
wait_for_deploy=false
[[ "${1:-}" == "--wait" ]] && wait_for_deploy=true

step() { printf '\n== %s\n' "$*"; }
fail() { echo "setup stopped: $*" >&2; exit 1; }

step "Preflight"
identity="$(aws sts get-caller-identity --query Account --output text 2>/dev/null || true)"
[[ "$identity" == "$AWS_ACCOUNT" ]] || fail "AWS credentials are for account '${identity:-none}', expected $AWS_ACCOUNT"
[[ -f "$CODE" ]] || fail "$CODE not found"
page_status="$(curl -s -o /dev/null -w '%{http_code}' "https://search2o.com$ERROR_PAGE")"
[[ "$page_status" == "200" ]] || fail "https://search2o.com$ERROR_PAGE returns $page_status - deploy the site first"
echo "account $identity; $ERROR_PAGE is live"

# ---- 1. the function ---------------------------------------------------------------------------
step "Function $FUNCTION_NAME"
config='{"Comment":"Redirect www. and docs. hosts to search2o.com","Runtime":"cloudfront-js-2.0"}'
if etag="$(aws cloudfront describe-function --name "$FUNCTION_NAME" --query ETag --output text 2>/dev/null)"; then
    aws cloudfront update-function --name "$FUNCTION_NAME" --if-match "$etag" \
        --function-config "$config" --function-code "fileb://$CODE" --query ETag --output text >/dev/null
    echo "updated"
else
    aws cloudfront create-function --name "$FUNCTION_NAME" \
        --function-config "$config" --function-code "fileb://$CODE" --query ETag --output text >/dev/null
    echo "created"
fi
etag="$(aws cloudfront describe-function --name "$FUNCTION_NAME" --query ETag --output text)"

# A redirect and a pass-through, checked against the DEVELOPMENT stage before publishing.
# The event goes in as a raw JSON file: the CLI base64-encodes a blob argument itself.
event_file="$(mktemp)"
run_test() {   # host, uri -> the function's output
    printf '{"version":"1.0","context":{"eventType":"viewer-request"},"viewer":{"ip":"203.0.113.1"},"request":{"method":"GET","uri":"%s","querystring":{},"headers":{"host":{"value":"%s"}},"cookies":{}}}' "$2" "$1" > "$event_file"
    aws cloudfront test-function --name "$FUNCTION_NAME" --if-match "$etag" --stage DEVELOPMENT \
        --event-object "fileb://$event_file" --query TestResult.FunctionOutput --output text
}
out="$(run_test www.search2o.com /pricing.html)"
[[ "$out" == *'"statusCode":301'* && "$out" == *'https://search2o.com/pricing.html'* ]] || fail "www redirect test failed: $out"
out="$(run_test search2o.com /pricing.html)"
[[ "$out" == *'"uri":"/pricing.html"'* && "$out" != *statusCode* ]] || fail "apex pass-through test failed: $out"
out="$(run_test docs.search2o.com /docsweb/uitext_current.json)"   # the GUI reads under this host: never redirected
[[ "$out" == *'"uri":"/docsweb/uitext_current.json"'* && "$out" != *statusCode* ]] || fail "docs-host pass-through test failed: $out"
rm -f "$event_file"
echo "tests passed"

arn="$(aws cloudfront publish-function --name "$FUNCTION_NAME" --if-match "$etag" \
    --query FunctionSummary.FunctionMetadata.FunctionARN --output text)"
echo "published $arn"

# ---- 2. the distribution: function association + error responses ---------------------------------
step "Distribution $DISTRIBUTION"
tmp="$(mktemp -d)"
aws cloudfront get-distribution-config --id "$DISTRIBUTION" > "$tmp/dist.json"
dist_etag="$(python3 -c "import json,sys; print(json.load(open('$tmp/dist.json'))['ETag'])")"
python3 - "$tmp/dist.json" "$tmp/config.json" "$arn" "$ERROR_PAGE" <<'PY'
import json, sys
src, dst, arn, page = sys.argv[1:]
cfg = json.load(open(src))["DistributionConfig"]
cfg["DefaultCacheBehavior"]["FunctionAssociations"] = {
    "Quantity": 1, "Items": [{"FunctionARN": arn, "EventType": "viewer-request"}]}
cfg["CustomErrorResponses"] = {"Quantity": 2, "Items": [
    {"ErrorCode": code, "ResponsePagePath": page, "ResponseCode": "404", "ErrorCachingMinTTL": 10}
    for code in (403, 404)]}
json.dump(cfg, open(dst, "w"))
PY
aws cloudfront update-distribution --id "$DISTRIBUTION" --if-match "$dist_etag" \
    --distribution-config "file://$tmp/config.json" --query Distribution.Status --output text
rm -rf "$tmp"
echo "function attached to viewer-request; 403 and 404 now answer 404 with $ERROR_PAGE"

# ---- 3. the bucket's error document ------------------------------------------------------------------
step "Bucket $BUCKET error document"
aws s3api put-bucket-website --bucket "$BUCKET" --website-configuration \
    "{\"IndexDocument\":{\"Suffix\":\"index.html\"},\"ErrorDocument\":{\"Key\":\"${ERROR_PAGE#/}\"}}"
echo "error document is ${ERROR_PAGE#/}"

# ---- wait and verify -----------------------------------------------------------------------------------
if $wait_for_deploy; then
    step "Waiting for the distribution to deploy (a few minutes)"
    waited=0
    while :; do
        status="$(aws cloudfront get-distribution --id "$DISTRIBUTION" --query Distribution.Status --output text)"
        [[ "$status" == "Deployed" ]] && break
        (( waited >= DEPLOY_MAX_WAIT_SECONDS )) && fail "distribution still $status after ${waited}s"
        sleep "$DEPLOY_POLL_SECONDS"; waited=$(( waited + DEPLOY_POLL_SECONDS ))
        echo "  $status (${waited}s)"
    done
    step "Verifying"
    printf '%-42s %s\n' "https://www.search2o.com/pricing.html" "$(curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}' https://www.search2o.com/pricing.html)"
    printf '%-42s %s\n' "https://docs.search2o.com/runtime/allowlist.html" "$(curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}' https://docs.search2o.com/runtime/allowlist.html)"
    printf '%-42s %s\n' "https://search2o.com/no-such-page" "$(curl -s -o /dev/null -w '%{http_code}' https://search2o.com/no-such-page)"
else
    echo
    echo "Applied. The distribution takes a few minutes to deploy; re-run with --wait, or check later:"
    echo "  curl -sI https://www.search2o.com/ | head -3          # expect 301 to https://search2o.com/"
    echo "  curl -s -o /dev/null -w '%{http_code}\\n' https://search2o.com/no-such-page   # expect 404"
fi
