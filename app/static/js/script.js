(function () {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector("body");
    const selectHeader = document.querySelector("#header");

    if (!selectBody || !selectHeader) return;

    // Only apply on home page
    if (!selectBody.classList.contains("home-page")) return;

    if (
      !selectHeader.classList.contains("scroll-up-sticky") &&
      !selectHeader.classList.contains("sticky-top") &&
      !selectHeader.classList.contains("fixed-top")
    )
      return;

    window.scrollY > 100
      ? selectBody.classList.add("scrolled")
      : selectBody.classList.remove("scrolled");
  }

  document.addEventListener("scroll", toggleScrolled);
  window.addEventListener("load", toggleScrolled);

  /**
   * Change header class based on page type
   */
  function toggleHeaderClass() {
    const selectBody = document.querySelector("body");
    const selectHeader = document.querySelector("#header");
    if (!selectBody || !selectHeader) return;

    if (selectBody.classList.contains("home-page")) {
      selectHeader.classList.add("fixed-top");
      selectHeader.classList.remove("sticky-top");
    } else {
      selectHeader.classList.remove("fixed-top");
      selectHeader.classList.add("sticky-top");
    }
  }
  window.addEventListener("load", toggleHeaderClass);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector(".mobile-nav-toggle");
  function mobileNavToggle() {
    const body = document.querySelector("body");
    if (!body || !mobileNavToggleBtn) return;
    body.classList.toggle("mobile-nav-active");
    mobileNavToggleBtn.classList.toggle("bi-list");
    mobileNavToggleBtn.classList.toggle("bi-x");
  }
  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener("click", mobileNavToggle);
  }

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll("#navmenu a").forEach((navmenu) => {
    navmenu.addEventListener("click", () => {
      if (document.querySelector(".mobile-nav-active")) {
        mobileNavToggle();
      }
    });
  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll(".navmenu .toggle-dropdown").forEach((navmenu) => {
    navmenu.addEventListener("click", function (e) {
      e.preventDefault();
      this.parentNode.classList.toggle("active");
      const dropdown = this.parentNode.querySelector("ul");
      if (dropdown) dropdown.classList.toggle("dropdown-active");
      e.stopImmediatePropagation();
    });
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector("#preloader");
  if (preloader) {
    window.addEventListener("load", () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  const scrollTop = document.querySelector(".scroll-top");
  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100
        ? scrollTop.classList.add("active")
        : scrollTop.classList.remove("active");
    }
  }
  if (scrollTop) {
    scrollTop.addEventListener("click", (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }
  window.addEventListener("load", toggleScrollTop);
  document.addEventListener("scroll", toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    if (window.AOS) {
      AOS.init({
        duration: 600,
        easing: "ease-in-out",
        once: true,
        mirror: false,
      });
    }
  }
  window.addEventListener("load", aosInit);

  /**
   * Auto generate the carousel indicators
   */
  document
    .querySelectorAll(".carousel-indicators")
    .forEach((carouselIndicator) => {
      const carousel = carouselIndicator.closest(".carousel");
      if (!carousel) return;
      const items = carousel.querySelectorAll(".carousel-item");
      carouselIndicator.innerHTML = ""; // prevent duplicates
      items.forEach((carouselItem, index) => {
        carouselIndicator.innerHTML += `
        <li data-bs-target="#${carousel.id}" data-bs-slide-to="${index}" ${
          index === 0 ? 'class="active"' : ""
        }></li>
      `;
      });
    });

  /**
   * Navmenu Scrollspy
   */
  const navmenulinks = document.querySelectorAll(".navmenu a");
  function navmenuScrollspy() {
    const position = window.scrollY + 200;
    navmenulinks.forEach((link) => {
      if (!link.hash) return;
      const section = document.querySelector(link.hash);
      if (!section) return;
      if (
        position >= section.offsetTop &&
        position <= section.offsetTop + section.offsetHeight
      ) {
        document
          .querySelectorAll(".navmenu a.active")
          .forEach((el) => el.classList.remove("active"));
        link.classList.add("active");
      } else {
        link.classList.remove("active");
      }
    });
  }
  window.addEventListener("load", navmenuScrollspy);
  document.addEventListener("scroll", navmenuScrollspy);

  /**
   * Auto-hide Bootstrap alerts
   */
  setTimeout(function () {
    document.querySelectorAll(".alert").forEach(function (alertEl) {
      alertEl.classList.remove("show");
    });
  }, 3000);
})();
