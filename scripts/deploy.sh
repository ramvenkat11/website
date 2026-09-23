#!/usr/bin/env bash
# Deploys the website (html/) to the search2o.com S3 bucket and invalidates CloudFront.
#
#   scripts/deploy.sh                 rebuild the docs, upload what changed, delete bucket objects that no
#                                     longer exist locally, invalidate, wait for it, verify with curl
#   scripts/deploy.sh --dry-run       show what would upload and what would be deleted; touch nothing
#   scripts/deploy.sh --skip-build    do not rebuild the docs first (either mode)
#
# The full procedure and the one-time bucket setup are in website_deploy.md.
set -euo pipefail

BUCKET="search2o.com"
DISTRIBUTION="E330RKTBY31L8X"
AWS_ACCOUNT="406848153313"
SITE_URL="https://search2o.com"
# docsweb/ is excluded from the sync itself: it holds the in-app docs data that s2oserver's
# maintenance/docswebuploader.py maintains, so --delete must never touch it.
SYNC_EXCLUDES=(--exclude ".DS_Store" --exclude "*/.DS_Store" --exclude "docsweb/*")
CACHE_CONTROL="public, max-age=600"   # pages, CSS, JS: short, so a deploy reaches browsers within minutes
IMAGE_CACHE_CONTROL="public, max-age=2592000"   # images, icons and fonts: 30 days; they change rarely
IMAGE_INCLUDES=(--exclude "*" --include "*.png" --include "*.svg" --include "*.jpg" --include "*.ico" --include "*.woff2")
IMAGE_EXCLUDES=(--exclude "*.png" --exclude "*.svg" --exclude "*.jpg" --exclude "*.ico" --exclude "*.woff2")
INVALIDATION_POLL_SECONDS=10
INVALIDATION_MAX_WAIT_SECONDS=600

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HTML="$ROOT/html"
PYTHON="${S2O_PYTHON:-$ROOT/../s2oserver/.venv/bin/python}"

go=true
skip_build=false
for arg in "$@"; do
    case "$arg" in
        --dry-run) go=false ;;
        --go) go=true ;;
        --skip-build) skip_build=true ;;
        -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
        *) echo "unknown option: $arg" >&2; exit 2 ;;
    esac
done

step() { printf '\n== %s\n' "$*"; }
fail() { echo "deploy stopped: $*" >&2; exit 1; }

# ---- preflight -------------------------------------------------------------------------------
step "Preflight"
command -v aws >/dev/null || fail "aws CLI not found"
identity="$(aws sts get-caller-identity --query Account --output text 2>/dev/null || true)"
[[ "$identity" == "$AWS_ACCOUNT" ]] || fail "AWS credentials are for account '${identity:-none}', expected $AWS_ACCOUNT"
echo "AWS account $identity"

# STANDING RULE (Ram, 2026-09-13; demoUrl added 2026-09-21): the website is never published unless
# config.js carries exactly the production URLs. A test or local URL here has gone live before; it
# must not again. Every key in PRODUCTION_URLS is checked, locally before the upload and live after it.
PRODUCTION_URLS=(
    "apiUrl=https://reg.api.search2o.com"
    "demoUrl=https://demo.api.search2o.com"
)
config_value() {   # config_value <key> <config.js text>: the string assigned to the key, or nothing
    printf '%s\n' "$2" | grep -E "^[[:space:]]*$1:" | sed -E "s/.*$1: *\"([^\"]*)\".*/\\1/"
}
check_config() {   # check_config <label> <config.js text>: fail on the first key that is not production
    local entry key expected value
    for entry in "${PRODUCTION_URLS[@]}"; do
        key="${entry%%=*}"; expected="${entry#*=}"
        value="$(config_value "$key" "$2")"
        [[ "$value" == "$expected" ]] || fail "$1 $key is '${value:-missing}', not $expected - nothing is published"
        echo "$1 $key: $value"
    done
}
check_config "html/js/config.js" "$(cat "$HTML/js/config.js")"

if [[ -n "$(git -C "$ROOT" status --porcelain -- html docsrc gen)" ]]; then
    echo "note: uncommitted changes under html/, docsrc/ or gen/ - they will be deployed as they are on disk"
fi

if ! $skip_build; then
    step "Rebuilding the docs"
    [[ -x "$PYTHON" ]] || fail "python not found at $PYTHON (set S2O_PYTHON)"
    (cd "$ROOT" && "$PYTHON" gen/build.py) || fail "gen/build.py failed"
    (cd "$ROOT" && "$PYTHON" gen/check_examples.py) || fail "gen/check_examples.py failed"
fi

# ---- what would change ---------------------------------------------------------------------------
step "Files that differ from the bucket (delete: an object with no local file)"
(cd "$HTML" && aws s3 sync . "s3://$BUCKET/" "${SYNC_EXCLUDES[@]}" "${IMAGE_EXCLUDES[@]}" --delete --acl public-read --cache-control "$CACHE_CONTROL" --dryrun \
    && aws s3 sync . "s3://$BUCKET/" "${IMAGE_INCLUDES[@]}" --exclude "docsweb/*" --delete --acl public-read --cache-control "$IMAGE_CACHE_CONTROL" --dryrun) \
    | sed 's/^(dryrun) //' || fail "s3 sync dry run failed"

if ! $go; then
    echo
    echo "Dry run only. Run without --dry-run to deploy."
    exit 0
fi

# ---- deploy ----------------------------------------------------------------------------------------
step "Uploading to s3://$BUCKET/"
(cd "$HTML" && aws s3 sync . "s3://$BUCKET/" "${SYNC_EXCLUDES[@]}" "${IMAGE_EXCLUDES[@]}" --delete --acl public-read --cache-control "$CACHE_CONTROL") || fail "s3 sync failed"
(cd "$HTML" && aws s3 sync . "s3://$BUCKET/" "${IMAGE_INCLUDES[@]}" --exclude "docsweb/*" --delete --acl public-read --cache-control "$IMAGE_CACHE_CONTROL") || fail "s3 sync of images failed"

step "Invalidating CloudFront $DISTRIBUTION"
invalidation_id="$(aws cloudfront create-invalidation --distribution-id "$DISTRIBUTION" --paths "/*" \
    --query Invalidation.Id --output text)" || fail "create-invalidation failed"
echo "invalidation $invalidation_id"
waited=0
while :; do
    status="$(aws cloudfront get-invalidation --distribution-id "$DISTRIBUTION" --id "$invalidation_id" \
        --query Invalidation.Status --output text)"
    [[ "$status" == "Completed" ]] && break
    (( waited >= INVALIDATION_MAX_WAIT_SECONDS )) && fail "invalidation still $status after ${waited}s"
    sleep "$INVALIDATION_POLL_SECONDS"; waited=$(( waited + INVALIDATION_POLL_SECONDS ))
    echo "  $status (${waited}s)"
done
echo "Completed"

# ---- verify ------------------------------------------------------------------------------------------
step "Verifying"
home_status="$(curl -s -o /dev/null -w '%{http_code}' "$SITE_URL/")"
docs_title="$(curl -s "$SITE_URL/docs/index.html" | grep -o '<title>[^<]*' | head -1)"
live_config="$(curl -s "$SITE_URL/js/config.js")"
echo "$SITE_URL/            $home_status"
echo "$SITE_URL/docs/index.html  ${docs_title:-no title found}"
[[ "$home_status" == "200" ]] || fail "home page returned $home_status"
check_config "LIVE $SITE_URL/js/config.js" "$live_config"

echo
echo "Deployed. If the docs changed, regenerate the in-app summaries with s2oserver's maintenance/docs_create.py."
