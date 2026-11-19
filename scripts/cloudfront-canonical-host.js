// CloudFront Function (viewer-request) for the tactet.com distribution.
//   www.tactet.com/x -> 301 https://tactet.com/x
// docs.tactet.com is NOT redirected: the GUI reads data under that host (the docsweb/ prefix
// and other paths not linked from the site), so it must keep serving the bucket root as is.
// Deployed by scripts/cloudfront-setup.sh.
function handler(event) {
    var request = event.request;
    var host = request.headers.host && request.headers.host.value;
    if (host !== 'www.tactet.com') {
        return request;
    }
    var qs = '';
    for (var key in request.querystring) {
        qs += (qs ? '&' : '?') + key + '=' + request.querystring[key].value;
    }
    return {
        statusCode: 301,
        statusDescription: 'Moved Permanently',
        headers: { location: { value: 'https://tactet.com' + request.uri + qs } }
    };
}
