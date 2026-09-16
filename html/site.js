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

var captchaWidget = null;
var captchaAsked = false;
var captchaLoaded = null;      // resolves once Google's script has run
var captchaLoadedResolve = null;

/**
 * reCAPTCHA v3, on the pages that carry a form.
 *
 * v3 shows NOTHING and has nothing to solve: the script is loaded, a widget is
 * rendered invisibly, and a token is minted per press. Each page carries its own
 * site key on a `.recaptcha-v3` element, which is also where Google's badge is
 * drawn — `badge: "inline"` puts it there rather than floating it in the corner
 * of the window. The badge has to stay visible somewhere: the alternative is
 * hiding it and showing the reCAPTCHA privacy text instead.
 *
 * The standalone pages under content/register carry their own inline scripts and
 * do not use this file.
 */
function captchaBox() {
  return document.querySelector(".recaptcha-v3");
}

function renderCaptcha() {
  var box = captchaBox();
  if (!box || captchaWidget !== null || !window.grecaptcha || !window.grecaptcha.render) return;
  try {
    captchaWidget = window.grecaptcha.render(box, {
      sitekey: box.getAttribute("data-sitekey"),
      size: "invisible",
      badge: "inline"
    });
  } catch (e) {}
}

function resetCaptcha() {
  // v3 tokens are single use and the widget is invisible: nothing to reset.
}

function loadCaptcha() {
  var box = captchaBox();
  if (!box) return Promise.resolve(false);
  if (captchaLoaded) return captchaLoaded;
  captchaLoaded = new Promise(function (resolve) {
    captchaLoadedResolve = resolve;
    if (window.grecaptcha && window.grecaptcha.render) return resolve(true);
    if (captchaAsked) return;
    captchaAsked = true;
    var s = document.createElement("script");
    s.src = "https://www.google.com/recaptcha/api.js?render=explicit&onload=s2oCaptchaReady";
    s.async = true;
    s.defer = true;
    s.onerror = function () { resolve(false); };
    document.head.appendChild(s);
    // Never leave a press waiting for a script that is not coming.
    setTimeout(function () { resolve(!!(window.grecaptcha && window.grecaptcha.render)); }, 10000);
  });
  return captchaLoaded;
}

/**
 * A fresh token, as a promise. Resolves to "" when one cannot be had, and the
 * caller says so. The action is checked against the token by the server, so each
 * form's string must match what the server expects, exactly.
 */
function captchaToken(action) {
  if (!captchaBox()) return Promise.resolve("");
  return loadCaptcha().then(function (ok) {
    if (!ok || !window.grecaptcha) return "";
    return new Promise(function (resolve) {
      try {
        window.grecaptcha.ready(function () {
          renderCaptcha();
          if (captchaWidget === null) return resolve("");
          window.grecaptcha
            .execute(captchaWidget, {action: action})
            .then(resolve, function () { resolve(""); });
        });
      } catch (e) { resolve(""); }
    });
  });
}

window.s2oCaptchaReady = function () {
  renderCaptcha();
  if (captchaLoadedResolve) captchaLoadedResolve(true);
};

(function () {
  if (!document.getElementById("reg-go1")) return;
  var BASE = (window.SEARCH2O_CONFIG && window.SEARCH2O_CONFIG.apiUrl) || "https://reg.api.search2o.com";
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

    $("reg-go1").disabled = true;
    // v3 mints a token per press, so it is asked for here rather than read from a
    // widget. "register" is checked against the token by the server, so it must
    // match exactly — a different string makes every visitor `notHuman`.
    loadCaptcha();
    captchaToken("register").then(function (token) {
      if (!token) {
        $("reg-go1").disabled = false;
        return say("We could not verify this request. Please reload the page and try again.", false);
      }
      return post("/register", {email: email, userName: userName, accountName: accountName, terms: true, token: token})
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
          resetCaptcha();
        });
    });
  });
})();

(function () {
  var btn = document.getElementById("agen-go");
  if (!btn) return;
  var BASE = (window.SEARCH2O_CONFIG && window.SEARCH2O_CONFIG.apiUrl) || "https://reg.api.search2o.com";
  var text = document.getElementById("agen-text");
  var out = document.getElementById("agen-out");
  var codeEl = document.getElementById("agen-code");
  var fname = document.getElementById("agen-fname");
  var count = document.getElementById("agen-count");
  var MIN_CHARS = 40, MAX_CHARS = 400;

  function tally() {
    var n = text.value.trim().length;
    var short = MIN_CHARS - n;
    if (short > 0) {
      count.textContent = short + (short === 1 ? " more character" : " more characters");
    } else {
      var left = MAX_CHARS - n;
      count.textContent = left + (left === 1 ? " character left" : " characters left");
    }
    btn.disabled = short > 0;
  }
  text.addEventListener("input", function () { tally(); loadCaptcha(); });
  text.addEventListener("focus", loadCaptcha);
  tally();

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function span(cls, txt) { return '<span class="' + cls + '">' + esc(txt) + "</span>"; }
  function hlLine(line) {
    var res = "", i = 0, n = line.length;
    while (i < n) {
      var ch = line[i];
      if (ch === "/" && line[i + 1] === "/") { res += span("tk-com", line.slice(i)); break; }
      if (ch === '"') {
        var j = i + 1;
        while (j < n && (line[j] !== '"' || line[j - 1] === "\\")) j++;
        var str = line.slice(i, Math.min(j + 1, n));
        var rest = line.slice(j + 1);
        var inner = str.slice(1, -1);
        var cls = /^\s*:/.test(rest) ? "tk-key" : (/^\s*\{.*\}\s*$/.test(inner) ? "tk-expr" : "tk-str");
        res += span(cls, str);
        i = j + 1; continue;
      }
      if (/[{}\[\]:,]/.test(ch)) { res += span("tk-pun", ch); i++; continue; }
      var word = /^(true|false|null)\b/.exec(line.slice(i));
      if (word) { res += span("tk-bool", word[0]); i += word[0].length; continue; }
      var plain = i;
      while (i < n && !/["{}\[\]:,\/]/.test(line[i]) && !/^(true|false|null)\b/.test(line.slice(i))) i++;
      if (i === plain) { res += esc(ch); i++; } else { res += esc(line.slice(plain, i)); }
    }
    return res;
  }
  function highlight(src) {
    return String(src).replace(/\r\n/g, "\n").split("\n").map(hlLine).join("\n");
  }
  function say(msg, ok) {
    out.hidden = false;
    out.className = "reg-out " + (ok ? "ok" : "err");
    out.textContent = msg;
  }

  btn.addEventListener("click", function () {
    var v = text.value.trim();
    if (v.length < MIN_CHARS || v.length > MAX_CHARS) return;

    btn.disabled = true;
    var label = btn.textContent;
    btn.textContent = "Generating\u2026";
    out.hidden = true;
    // The token is fetched here, not read from a widget: v3 mints one per press.
    // "demoAgentGen" is checked against the token by the server, so it must match
    // exactly — a different string makes every visitor `notHuman`.
    loadCaptcha();
    captchaToken("demoAgentGen").then(function (token) {
      if (!token) {
        btn.textContent = label;
        tally();
        return say("We could not verify this request. Please reload the page and try again.", false);
      }
      return fetch(BASE + "/demoAgentGen", {
        method: "POST", headers: {"Content-Type": "application/json"},
        body: JSON.stringify({userPrompt: v, token: token})
      }).then(function (r) { return r.json().catch(function () { return null; }); })
        .then(function (data) {
          if (data && data.success) {
            if (data.code) {
              codeEl.innerHTML = highlight(data.code);
              fname.textContent = "generated \u00b7 agent definition";
            }
            if (data.message) say(data.message, true);
          } else {
            say((data && data.message) || "We could not generate the agent. Please try again.", false);
          }
        })
        .catch(function () { say("Something went wrong. Please try again.", false); })
        .finally(function () {
          btn.textContent = label;
          tally();
          resetCaptcha();
        });
    });
  });
})();
