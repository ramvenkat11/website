<!-- In your HTML -->
<script src="/config.js"></script>

<script>
    async function register(data) {
    const response = await fetch(`${window.SEARCH2O_CONFIG.apiUrl}/register`, {
    method: "POST",
    headers: {
    "Content-Type": "application/json",
},
    body: JSON.stringify(data),
});

    return response.json();
}
</script>


<!-- Local config.js -->
<script>
    window.SEARCH2O_CONFIG = {
    apiUrl: "http://localhost:8080",
};
</script>


<!-- Production config.js -->
<script>
    window.SEARCH2O_CONFIG = {
    apiUrl: "https://api.search2o.com",
};
</script>