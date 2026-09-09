// Copy-to-clipboard buttons ([data-copy]) and footer year.
document.querySelectorAll("[data-copy]").forEach(function (btn) {
  var original = btn.innerHTML;
  btn.addEventListener("click", function () {
    navigator.clipboard.writeText(btn.getAttribute("data-copy")).then(function () {
      btn.innerHTML =
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#15803d" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
      setTimeout(function () { btn.innerHTML = original; }, 1400);
    });
  });
});

var year = document.getElementById("year");
if (year) year.textContent = String(new Date().getFullYear());

// Theme: system preference by default (pure CSS); the toggle sets an explicit
// data-theme override, persisted. Toggling back to the system's own value clears
// the override, so the page follows the system again. A tiny inline script in
// each page's <head> re-applies the stored override before first paint.
var themeBtn = document.querySelector(".theme-toggle");
if (themeBtn) {
  var darkQuery = window.matchMedia("(prefers-color-scheme: dark)");
  var resolvedTheme = function () {
    return document.documentElement.dataset.theme || (darkQuery.matches ? "dark" : "light");
  };
  var updateLabel = function () {
    themeBtn.setAttribute("aria-label",
      resolvedTheme() === "dark" ? "Switch to light theme" : "Switch to dark theme");
  };
  themeBtn.addEventListener("click", function () {
    var next = resolvedTheme() === "dark" ? "light" : "dark";
    var system = darkQuery.matches ? "dark" : "light";
    if (next === system) {
      delete document.documentElement.dataset.theme;
      try { localStorage.removeItem("s2o-theme"); } catch (e) {}
    } else {
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem("s2o-theme", next); } catch (e) {}
    }
    updateLabel();
  });
  darkQuery.addEventListener("change", updateLabel);
  updateLabel();
}

// Account creation: one call to the API. Success returns the license key, shown
// exactly once. The user sets a password on first sign-in to the GUI.
(function () {
  if (!document.getElementById("reg-go1")) return;
  var BASE = (window.SEARCH2O_CONFIG && window.SEARCH2O_CONFIG.apiUrl) || "https://api.search2o.com";
  var REG_ERRORS = {
    notHuman: "Human verification failed. Please try again.",
    didYouMean: "Please check your email address. Did you mean {didYouMean}?",
    invalidEmail: "Please enter a valid email address.",
    bogusEmail: "Disposable email addresses cannot be used to create an account.",
    freeEmailCurrentlyNotAllowed: "Public email domains are currently not allowed. Please use your work email address.",
    currentlySuspended: "New accounts are paused at the moment due to high volume. Please try again in a few days.",
    termsNotAccepted: "You must accept the Terms of Service and Privacy Policy to create an account.",
    individualAccountExists: "An individual account already exists for this email address. " +
        "You should upgrade the other account, before you can register another account with the same email. " +
        "If you lost your license key, please contact us at support@search2o.com."
  };
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }
  function regErrorMessages(data) {
    var msgs = [];
    ((data && data.registrationErrors) || []).forEach(function (key) {
      var m = REG_ERRORS[key];
      if (key === "didYouMean") {
        m = data.didYouMean ? m.replace("{didYouMean}", esc(data.didYouMean))
                            : "Please check your email address.";
      }
      if (m) msgs.push(m);
    });
    return msgs;
  }
  var $ = function (id) { return document.getElementById(id); };

  function say(msg, ok) {
    var o = $("reg-out");
    o.hidden = false;
    o.className = "reg-out " + (ok ? "ok" : "err");
    o.innerHTML = msg;
  }

  function showLicense(license) {
    var o = $("reg-out");
    o.hidden = false;
    o.className = "reg-done";
    o.innerHTML = '<p class="reg-ready">Your account is ready.</p>'
      + '<div class="reg-keybox">'
      +   '<div class="reg-keylabel">License key</div>'
      +   '<div class="reg-keyrow"><code id="reg-key"></code>'
      +   '<button type="button" id="reg-copy" aria-label="Copy license key">'
      +     '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>'
      +   '</button></div>'
      + '</div>'
      + '<p class="reg-note">This key is shown only once &mdash; please copy it and store it on your machine right away. The next steps use it.</p>';
    $("reg-key").textContent = license;
    var copyBtn = $("reg-copy");
    var original = copyBtn.innerHTML;
    copyBtn.addEventListener("click", function () {
      navigator.clipboard.writeText(license).then(function () {
        copyBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#15803d" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
        setTimeout(function () { copyBtn.innerHTML = original; }, 1400);
      });
    });
  }

  function post(path, body) {
    return fetch(BASE + path, {
      method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)
    }).then(function (r) { return r.json().catch(function () { return null; }); });
  }

  $("reg-go1").addEventListener("click", function () {
    var email = $("reg-email").value.trim();
    var userName = $("reg-name").value.trim(), accountName = $("reg-account").value.trim();
    if (!email || !userName || !accountName) return say("Please fill in every field.", false);
    if (!$("reg-terms").checked) return say("Please accept the Terms of Service.", false);

    var token = "";
    try { token = hcaptcha.getResponse(); } catch (e) {}
    if (!token) return say("Please complete the hCaptcha.", false);

    $("reg-go1").disabled = true;
    post("/register", {email: email, userName: userName, accountName: accountName, terms: true, token: token})
      .then(function (data) {
        if (data && data.success && data.license) {
          $("reg-step1").hidden = true;
          showLicense(data.license);
        } else {
          var msgs = regErrorMessages(data);
          say(msgs.length ? msgs.join("<br>")
                          : "We could not create your account. Please check your details and try again.", false);
        }
      })
      .catch(function () { say("Something went wrong. Please try again.", false); })
      .finally(function () {
        $("reg-go1").disabled = false;
        try { hcaptcha.reset(); } catch (e) {}
      });
  });
})();
