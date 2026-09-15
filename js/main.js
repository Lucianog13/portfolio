/* =====================================================================
   Vértice · VerticeLABS — lógica principal de la página
   Módulos: nav con blur, scroll reveal, tilt 3D, parallax del logo,
   constelación de partículas. Sin dependencias externas.
   ===================================================================== */

(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fino = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* ── 1. Nav con blur al scrollear ──────────────────────────────── */
  var nav = document.getElementById("nav");
  function alScroll() {
    if (window.scrollY > 24) nav.classList.add("scrolled");
    else nav.classList.remove("scrolled");
  }
  window.addEventListener("scroll", alScroll, { passive: true });
  alScroll();

  /* ── 2. Scroll reveal 3D con stagger ───────────────────────────── */
  var obs = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add("visible");
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll(".revelar").forEach(function (el, i) {
    el.style.transitionDelay = (i % 4) * 0.08 + "s";
    obs.observe(el);
  });

  /* ── 3. Tilt 3D de tarjetas y parallax del logo (solo mouse) ───── */
  if (fino && !reduce) {
    document.querySelectorAll(".card3d").forEach(function (card) {
      card.addEventListener("pointermove", function (ev) {
        var r = card.getBoundingClientRect();
        var px = (ev.clientX - r.left) / r.width;
        var py = (ev.clientY - r.top) / r.height;
        card.style.setProperty("--rx", ((0.5 - py) * 9).toFixed(2) + "deg");
        card.style.setProperty("--ry", ((px - 0.5) * 11).toFixed(2) + "deg");
        card.style.setProperty("--mx", (px * 100).toFixed(1) + "%");
        card.style.setProperty("--my", (py * 100).toFixed(1) + "%");
      });
      card.addEventListener("pointerleave", function () {
        card.style.setProperty("--rx", "0deg");
        card.style.setProperty("--ry", "0deg");
      });
    });

    var plataforma = document.getElementById("plataforma");
    var hero = document.querySelector(".hero");
    var tx = 0, ty = 0, cx = 0, cy = 0;
    hero.addEventListener("pointermove", function (ev) {
      var r = hero.getBoundingClientRect();
      tx = ((ev.clientX - r.left) / r.width - 0.5) * 22;
      ty = ((ev.clientY - r.top) / r.height - 0.5) * -18;
    });
    (function animarParallax() {
      cx += (tx - cx) * 0.08;
      cy += (ty - cy) * 0.08;
      if (Math.abs(cx) > 0.02 || Math.abs(cy) > 0.02) {
        plataforma.style.transform = "rotateX(" + cy.toFixed(2) + "deg) rotateY(" + cx.toFixed(2) + "deg)";
      }
      requestAnimationFrame(animarParallax);
    })();
  }

  /* ── 4. Constelación de partículas ─────────────────────────────── */
  if (!reduce) {
    var canvas = document.getElementById("particulas");
    var ctx = canvas.getContext("2d");
    var W, H, puntos = [], N;
    var COLORES = ["59,130,246", "168,85,247", "34,211,238"];

    function medir() {
      W = canvas.width = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }
    function sembrar() {
      N = W < 700 ? 42 : 85;
      puntos = [];
      for (var i = 0; i < N; i++) {
        puntos.push({
          x: Math.random() * W,
          y: Math.random() * H,
          vx: (Math.random() - 0.5) * 0.28,
          vy: (Math.random() - 0.5) * 0.28,
          r: Math.random() * 1.6 + 0.4,
          c: COLORES[Math.random() * COLORES.length | 0]
        });
      }
    }
    medir(); sembrar();
    window.addEventListener("resize", function () { medir(); sembrar(); });

    function dibujar() {
      ctx.clearRect(0, 0, W, H);
      var i, j, p, q, d;
      for (i = 0; i < N; i++) {
        p = puntos[i];
        p.x += p.vx; p.y += p.vy;
        if (p.x < -10) p.x = W + 10; if (p.x > W + 10) p.x = -10;
        if (p.y < -10) p.y = H + 10; if (p.y > H + 10) p.y = -10;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(" + p.c + ",0.55)";
        ctx.fill();
      }
      for (i = 0; i < N; i++) {
        p = puntos[i];
        for (j = i + 1; j < N; j++) {
          q = puntos[j];
          d = (p.x - q.x) * (p.x - q.x) + (p.y - q.y) * (p.y - q.y);
          if (d < 12100) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(q.x, q.y);
            ctx.strokeStyle = "rgba(" + p.c + "," + ((1 - d / 12100) * 0.14).toFixed(3) + ")";
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }
      }
      requestAnimationFrame(dibujar);
    }
    dibujar();
  }
})();
