/* ============================================
   Scheduler — Landing Page Scripts
   ============================================ */

(function () {
  "use strict";

  // --- Fade-in on scroll (Intersection Observer) -----
  var fadeEls = document.querySelectorAll(".fade-in");

  if (fadeEls.length && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );

    fadeEls.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    fadeEls.forEach(function (el) {
      el.classList.add("visible");
    });
  }

  // --- Smooth scroll for anchor links ----------------
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      var targetId = this.getAttribute("href");
      if (targetId === "#") return;
      var target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        var headerOffset = 70;
        var top =
          target.getBoundingClientRect().top +
          window.pageYOffset -
          headerOffset;
        window.scrollTo({ top: top, behavior: "smooth" });
      }
    });
  });

  // --- GitHub star count (decorative) ----------------
  var badge = document.querySelector(".github-link .star-count");
  if (badge) {
    fetch("https://api.github.com/repos/AkaruiYami/Scheduler")
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.stargazers_count !== undefined) {
          badge.textContent = data.stargazers_count;
        }
      })
      .catch(function () {});
  }
})();
