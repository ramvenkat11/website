// Sidebar toggle on narrow screens, and the on-page TOC following the scroll position.
(function () {
  var toggle = document.querySelector(".sb-toggle");
  var wrap = document.getElementById("sidebar");
  if (toggle && wrap) {
    toggle.addEventListener("click", function () {
      var open = wrap.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  var links = Array.prototype.slice.call(document.querySelectorAll(".pagetoc a"));
  if (!links.length || !("IntersectionObserver" in window)) return;
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
  var current = null;
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      if (current) current.classList.remove("active");
      current = byId[e.target.id];
      if (current) current.classList.add("active");
    });
  }, { rootMargin: "-80px 0px -70% 0px", threshold: 0 });
  Object.keys(byId).forEach(function (id) {
    var h = document.getElementById(id);
    if (h) observer.observe(h);
  });
})();
