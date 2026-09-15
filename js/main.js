/* =====================================================================
   Vértice · VerticeLABS — lógica principal de la página
   Módulos: nav con blur, scroll reveal, tilt 3D, parallax del logo,
   constelación de partículas. Sin dependencias externas.
   ===================================================================== */

(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fino = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* ── 1. Nav con blur al scrollear + barra de progreso ──────────── */
  var nav = document.getElementById("nav");
  var progreso = document.getElementById("progreso");
  function alScroll() {
    if (window.scrollY > 24) nav.classList.add("scrolled");
    else nav.classList.remove("scrolled");
    var doc = document.documentElement;
    var max = doc.scrollHeight - doc.clientHeight;
    progreso.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + "%";
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

  /* ── 5. Contadores animados en stats ───────────────────────────── */
  var contadores = document.querySelectorAll(".contador");
  function animarContador(el) {
    var hasta = parseInt(el.getAttribute("data-hasta"), 10);
    if (reduce) { el.textContent = hasta; return; }
    var inicio = performance.now();
    var dur = 1400;
    function paso(ahora) {
      var t = Math.min((ahora - inicio) / dur, 1);
      var suave = 1 - Math.pow(1 - t, 3); // ease-out cúbico
      el.textContent = Math.round(suave * hasta);
      if (t < 1) requestAnimationFrame(paso);
    }
    requestAnimationFrame(paso);
  }
  var obsCont = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (e) {
      if (e.isIntersecting) {
        animarContador(e.target);
        obsCont.unobserve(e.target);
      }
    });
  }, { threshold: 0.6 });
  contadores.forEach(function (el) { obsCont.observe(el); });

  /* ── 6. Botones magnéticos (solo mouse fino) ───────────────────── */
  if (fino && !reduce) {
    document.querySelectorAll(".cta, .cta-wa, .cta-ghost, .nav-cta").forEach(function (b) {
      b.addEventListener("pointermove", function (ev) {
        var r = b.getBoundingClientRect();
        var dx = (ev.clientX - r.left - r.width / 2) * 0.14;
        var dy = (ev.clientY - r.top - r.height / 2) * 0.22;
        b.style.transition = "transform 0.15s ease";
        b.style.transform = "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px)";
      });
      b.addEventListener("pointerleave", function () {
        b.style.transform = "translate(0,0)";
      });
    });

    /* foco de luz que sigue al mouse en los segmentos: lo maneja el
       tilt de .card3d (clase aplicada a .segmento) */
  }

  /* ── 7. Brillo que sigue al cursor (solo mouse fino) ───────────── */
  if (fino && !reduce) {
    var glow = document.getElementById("cursor-glow");
    var gx = 0, gy = 0, px2 = 0, py2 = 0;
    window.addEventListener("pointermove", function (ev) {
      gx = ev.clientX; gy = ev.clientY;
      glow.style.opacity = "1";
    });
    (function animarGlow() {
      px2 += (gx - px2) * 0.09;
      py2 += (gy - py2) * 0.09;
      glow.style.transform = "translate(" + px2.toFixed(1) + "px," + py2.toFixed(1) + "px)";
      requestAnimationFrame(animarGlow);
    })();
  }

  /* ── 8. Parallax suave de secciones ─────────────────────────────── */
  if (!reduce) {
    var secciones = Array.prototype.slice.call(document.querySelectorAll(".seccion, .contacto, .divisor"));
    var ultimoScroll = 0;
    function parallax() {
      var vh = window.innerHeight;
      secciones.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -80 || r.top > vh + 80) return;
        var delta = (r.top + r.height / 2 - vh / 2) * 0.035;
        el.style.transform = "translateY(" + (-delta).toFixed(1) + "px)";
      });
    }
    window.addEventListener("scroll", function () {
      if (window.scrollY !== ultimoScroll) {
        ultimoScroll = window.scrollY;
        requestAnimationFrame(parallax);
      }
    }, { passive: true });
    parallax();
  }

  /* ── 9. Palabras del hero con entrada escalonada ────────────────── */
  var sub = document.querySelector(".sub");
  if (sub) {
    if (reduce) {
      sub.style.opacity = "1";
    } else {
      var palabras = sub.textContent.trim().split(/\s+/);
      sub.innerHTML = "";
      palabras.forEach(function (w, i) {
        var s = document.createElement("span");
        s.className = "palabra";
        s.textContent = w;
        s.style.animationDelay = (0.55 + i * 0.05) + "s";
        sub.appendChild(s);
        sub.appendChild(document.createTextNode(" "));
      });
    }
  }

  /* ── 10. Constelación de partículas ─────────────────────────────── */
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
