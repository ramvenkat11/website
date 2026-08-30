# Deploying the website (search2o.com)

The site and the docs are static files under `docs/website/html/`. They are served from the S3
bucket `search2o.com` (static-website hosting) behind the CloudFront distribution
`E330RKTBY31L8X`, which carries the aliases `search2o.com`, `www.search2o.com` and
`docs.search2o.com`. The distribution's origin is the bucket's **website endpoint**
(`search2o.com.s3-website-us-east-1.amazonaws.com`), so the bucket's index-document rule applies:
`/` serves `index.html`, and any missing key also serves `index.html` (there is no 404 page).

## Before deploying

1. Rebuild the docs if anything under `docs/website/docsrc/` or `docs/website/gen/` changed:

       PYTHONPATH=. .venv/bin/python docs/website/gen/build.py
       PYTHONPATH=. .venv/bin/python docs/website/gen/check_examples.py   # every jsonc example must validate

   The five site pages (`index.html`, `gettingstarted.html`, `pricing.html`, `support.html`,
   `about.html`) are edited directly in `docs/website/html/`.

2. Check it locally - serve `docs/website/html` on a port above 10000 and look at both themes:

       cd docs/website/html && python3 -m http.server 10483

## Deploy

Run from `docs/website/html`, with AWS credentials for account 406848153313:

    aws s3 sync . s3://search2o.com/ \
        --exclude logo.svg --exclude ".DS_Store" --exclude "*/.DS_Store" \
        --acl public-read

    aws cloudfront create-invalidation --distribution-id E330RKTBY31L8X --paths "/*"

That is the whole deploy. `sync` uploads only files that changed, sets the content type from the
extension, and never deletes anything in the bucket. The invalidation takes about a minute:

    aws cloudfront get-invalidation --distribution-id E330RKTBY31L8X --id <id> --query Invalidation.Status

## Verify

    curl -s -o /dev/null -w "%{http_code}\n" https://search2o.com/
    curl -s https://search2o.com/docs/index.html | grep -o "<title>[^<]*"

Screenshots live under `docs/img/` as light/dark pairs; check one of each renders.

## One-time setup (already done, recorded in case the bucket is ever recreated)

The bucket's index document was `home.html` (the 2024 "Coming soon" page). It is now:

    aws s3api put-bucket-website --bucket search2o.com --website-configuration \
        '{"IndexDocument":{"Suffix":"index.html"},"ErrorDocument":{"Key":"index.html"}}'

Objects are uploaded with `--acl public-read`; the bucket has ACLs enabled for that purpose.

## Notes

- `logo.svg` (589 KB) is excluded: nothing references it; `logo.png` is the wordmark in use.
- Because `sync` does not delete, retired files stay in the bucket until removed by hand. As of
  2026-08-28 the bucket still holds the old `home.html`, `css/`, `js/`, `docsweb/` and a stray
  `e2b6c55d-….html`, none referenced by the site.
- `maintenance/docswebuploader.py` uploads the OLD in-app docs (`docsweb/` prefix) and is not part
  of deploying the website.
- Add `--dryrun` to the `sync` command to see what would change before uploading.
