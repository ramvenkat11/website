// CloudFront Function (viewer-request) for the search2o.com distribution: one canonical host.
//   www.search2o.com/x   -> 301 https://search2o.com/x
//   docs.search2o.com/x  -> 301 https://search2o.com/docs/x   (a path already under /docs is kept)
// Deployed by scripts/cloudfront-setup.sh.
function handler(event) {
    var request = event.request;
    var host = request.headers.host && request.headers.host.value;
    var uri = request.uri;
    var target = null;
    if (host === 'www.search2o.com') {
        target = uri;
    } else if (host === 'docs.search2o.com') {
        target = uri.indexOf('/docs/') === 0 || uri === '/docs' ? uri : '/docs' + (uri === '/' ? '/' : uri);
    }
    if (target === null) {
        return request;
    }
    var qs = '';
    for (var key in request.querystring) {
        qs += (qs ? '&' : '?') + key + '=' + request.querystring[key].value;
    }
    return {
        statusCode: 301,
        statusDescription: 'Moved Permanently',
        headers: { location: { value: 'https://search2o.com' + target + qs } }
    };
}
