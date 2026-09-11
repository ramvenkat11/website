// CloudFront Function (viewer-request) for the search2o.com distribution.
//   www.search2o.com/x -> 301 https://search2o.com/x
// docs.search2o.com is NOT redirected: the GUI reads data under that host (the docsweb/ prefix
// and other paths not linked from the site), so it must keep serving the bucket root as is.
// Deployed by scripts/cloudfront-setup.sh.
function handler(event) {
    var request = event.request;
    var host = request.headers.host && request.headers.host.value;
    if (host !== 'www.search2o.com') {
        return request;
    }
    var qs = '';
    for (var key in request.querystring) {
        qs += (qs ? '&' : '?') + key + '=' + request.querystring[key].value;
    }
    return {
        statusCode: 301,
        statusDescription: 'Moved Permanently',
        headers: { location: { value: 'https://search2o.com' + request.uri + qs } }
    };
}
