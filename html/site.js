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
