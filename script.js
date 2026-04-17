/* ══════════════════════════════════════════
   露涼社 CampCool — Main JavaScript
══════════════════════════════════════════ */
(function () {
  'use strict';

  /* ── Navbar scroll state ── */
  var navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('scrolled', window.scrollY > 30);
    }, { passive: true });
  }

  /* ── Mobile hamburger menu ── */
  var hamburger = document.getElementById('hamburger');
  var navLinks = document.getElementById('navLinks');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', function () {
      hamburger.classList.toggle('active');
      navLinks.classList.toggle('open');
      document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
    });
    navLinks.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        hamburger.classList.remove('active');
        navLinks.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  /* ── Smooth scroll for anchor links ── */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  /* ── Carousel class ── */
  function Carousel(containerId, dotsId) {
    var container = document.getElementById(containerId);
    if (!container) return;

    var track = container.querySelector('.carousel-track');
    var slides = container.querySelectorAll('.carousel-slide');
    var prevBtn = container.querySelector('.carousel-prev');
    var nextBtn = container.querySelector('.carousel-next');
    var dotsWrap = document.getElementById(dotsId);
    var current = 0;
    var total = slides.length;
    var startX = 0;
    var diffX = 0;
    var dragging = false;

    // Build dots
    if (dotsWrap && total > 1) {
      for (var i = 0; i < total; i++) {
        var dot = document.createElement('button');
        dot.className = 'carousel-dot' + (i === 0 ? ' active' : '');
        dot.setAttribute('aria-label', '\u7b2c ' + (i + 1) + ' \u9805');
        dot.dataset.index = i;
        dot.addEventListener('click', function () {
          goTo(parseInt(this.dataset.index));
        });
        dotsWrap.appendChild(dot);
      }
    }

    function goTo(index) {
      if (index < 0) index = total - 1;
      if (index >= total) index = 0;
      current = index;
      track.style.transform = 'translateX(-' + (current * 100) + '%)';
      updateDots();
    }

    function updateDots() {
      if (!dotsWrap) return;
      var dots = dotsWrap.querySelectorAll('.carousel-dot');
      dots.forEach(function (d, i) {
        d.classList.toggle('active', i === current);
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', function () { goTo(current - 1); });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', function () { goTo(current + 1); });
    }

    // Touch swipe support
    track.addEventListener('touchstart', function (e) {
      startX = e.touches[0].clientX;
      dragging = true;
    }, { passive: true });

    track.addEventListener('touchmove', function (e) {
      if (!dragging) return;
      diffX = e.touches[0].clientX - startX;
    }, { passive: true });

    track.addEventListener('touchend', function () {
      if (!dragging) return;
      dragging = false;
      if (Math.abs(diffX) > 50) {
        if (diffX < 0) goTo(current + 1);
        else goTo(current - 1);
      }
      diffX = 0;
    });

    // Mouse drag support for desktop
    track.addEventListener('mousedown', function (e) {
      startX = e.clientX;
      dragging = true;
      track.style.cursor = 'grabbing';
      e.preventDefault();
    });

    track.addEventListener('mousemove', function (e) {
      if (!dragging) return;
      diffX = e.clientX - startX;
    });

    track.addEventListener('mouseup', function () {
      if (!dragging) return;
      dragging = false;
      track.style.cursor = '';
      if (Math.abs(diffX) > 50) {
        if (diffX < 0) goTo(current + 1);
        else goTo(current - 1);
      }
      diffX = 0;
    });

    track.addEventListener('mouseleave', function () {
      if (dragging) {
        dragging = false;
        track.style.cursor = '';
        diffX = 0;
      }
    });

    // Keyboard support
    container.setAttribute('tabindex', '0');
    container.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') goTo(current - 1);
      if (e.key === 'ArrowRight') goTo(current + 1);
    });
  }

  /* ── Initialize carousels ── */
  new Carousel('acCarousel', 'acDots');
  new Carousel('fridgeCarousel', 'fridgeDots');

  /* ── Fade-in on scroll ── */
  function initFadeIn() {
    var selectors = [
      '.section-header',
      '.product-card',
      '.pricing-card',
      '.step-card',
      '.feature-card',
      '.location-card',
      '.review-card',
      '.faq-item',
      '.compare-table-wrap',
      '.note-box',
      '.cta-section .container',
      '.carousel'
    ];
    var elements = document.querySelectorAll(selectors.join(','));
    elements.forEach(function (el) { el.classList.add('fade-in'); });

    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

      elements.forEach(function (el) { observer.observe(el); });
    } else {
      elements.forEach(function (el) { el.classList.add('visible'); });
    }
  }

  /* ── Active nav highlight ── */
  function initActiveNav() {
    var sections = document.querySelectorAll('section[id]');
    var navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');

    if ('IntersectionObserver' in window && sections.length && navAnchors.length) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var id = entry.target.getAttribute('id');
            navAnchors.forEach(function (a) {
              a.classList.toggle('active', a.getAttribute('href') === '#' + id);
            });
          }
        });
      }, { threshold: 0.2, rootMargin: '-80px 0px -50% 0px' });

      sections.forEach(function (s) { observer.observe(s); });
    }
  }

  /* ── Init ── */
  initFadeIn();
  initActiveNav();

})();
