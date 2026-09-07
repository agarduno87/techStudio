/*
  Technical Transformation Studio — app.js

  - Navegación móvil accesible (aria-expanded, cierre con Escape).
  - Calculadora del costo del trabajo manual, 100% en el navegador. Cambia de moneda
    con el idioma: inglés en USD, español en MXN. No se envía ni se guarda nada.
  - Formulario enviado desde la propia página por fetch a /api/contact. Sin mailto,
    sin direcciones de correo en el código del cliente.
  - Antispam sin CAPTCHA: honeypot + trampa de tiempo, revalidados en el servidor.
  - Sin innerHTML, sin eval, sin localStorage, sin dependencias externas.
*/
(function () {
  "use strict";

  var API_ENDPOINT = "/api/contact";
  var REQUEST_TIMEOUT_MS = 15000;
  var MIN_FILL_SECONDS = 3;
  var WORKING_WEEKS = 48;

  var $ = function (id) { return document.getElementById(id); };

  function t(key, fallback) {
    if (window.ttsI18n && typeof window.ttsI18n.t === "function") {
      return window.ttsI18n.t(key, fallback);
    }
    return fallback;
  }

  /* ---------------------------------------------------------------
     Año del footer
     --------------------------------------------------------------- */
  (function () {
    var year = $("year");
    if (year) { year.textContent = String(new Date().getFullYear()); }
  })();

  /* ---------------------------------------------------------------
     Navegación móvil
     --------------------------------------------------------------- */
  (function () {
    var burger = $("burger");
    var nav = $("mainnav");
    if (!burger || !nav) { return; }

    function setOpen(open) {
      nav.classList.toggle("open", open);
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      burger.setAttribute("aria-label", open ? t("menu.close", "Close menu") : t("menu.open", "Open menu"));
    }

    burger.addEventListener("click", function () {
      setOpen(!nav.classList.contains("open"));
    });

    /* El selector de idioma vive dentro del nav: usarlo no debe cerrarlo. */
    nav.addEventListener("click", function (event) {
      if (event.target.tagName === "A") { setOpen(false); }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && nav.classList.contains("open")) {
        setOpen(false);
        burger.focus();
      }
    });
  })();

  /* ---------------------------------------------------------------
     Calculadora del costo del trabajo manual
     --------------------------------------------------------------- */
  (function () {
    var people = $("people");
    var hours = $("hours");
    var rate = $("rate");
    var totalOut = $("calcTotal");
    var hoursOut = $("calcHours");
    if (!people || !hours || !rate || !totalOut || !hoursOut) { return; }

    /* Moneda por defecto hasta que i18n.js anuncie el idioma activo. */
    var currency = { code: "USD", intl: "en-US", min: 5, max: 120, step: 1, value: 25 };

    function format(value, style) {
      try {
        if (style === "currency") {
          /* currencyDisplay:"code" a propósito: en México el peso también usa "$",
             así que "$460,800" se puede leer como dólares. "MXN 460,800" no. */
          return new Intl.NumberFormat(currency.intl, {
            style: "currency",
            currency: currency.code,
            currencyDisplay: "code",
            maximumFractionDigits: 0
          }).format(value);
        }
        return new Intl.NumberFormat(currency.intl, { maximumFractionDigits: 0 }).format(value);
      } catch (e) {
        /* Si el navegador no conoce la moneda o el locale, no se rompe la página. */
        return currency.code + " " + Math.round(value);
      }
    }

    function recalc() {
      var p = Number(people.value);
      var h = Number(hours.value);
      var r = Number(rate.value);
      var totalHours = p * h * WORKING_WEEKS;
      var cost = totalHours * r;

      $("peopleOut").textContent = String(p);
      $("hoursOut").textContent = String(h);
      $("rateOut").textContent = format(r, "currency");
      totalOut.textContent = format(cost, "currency");
      hoursOut.textContent = format(totalHours, "number") + " " + t("calc.hours", "hours a year");
    }

    function setCurrency(next) {
      if (!next) { return; }
      currency = next;
      /* El rango de costo por hora depende de la moneda: nadie piensa el costo de
         su gente en una divisa convertida. Personas y horas se conservan; solo la
         tarifa vuelve a su valor de referencia para esa moneda. */
      rate.min = String(next.min);
      rate.max = String(next.max);
      rate.step = String(next.step);
      rate.value = String(next.value);

      var label = $("rateLabel");
      if (label) { label.textContent = t("calc.rateLabel", "Fully loaded cost per hour (USD)"); }
      recalc();
    }

    [people, hours, rate].forEach(function (el) { el.addEventListener("input", recalc); });
    document.addEventListener("tts:locale", function (event) {
      setCurrency(event.detail && event.detail.currency);
    });

    recalc();
  })();

  /* ---------------------------------------------------------------
     Formulario de contacto
     --------------------------------------------------------------- */
  (function () {
    var form = $("contactForm");
    var statusEl = $("formStatus");
    var submitBtn = $("submitBtn");
    var renderedAt = $("renderedAt");
    if (!form || !statusEl || !submitBtn) { return; }

    if (renderedAt) { renderedAt.value = String(Date.now()); }
    var idleLabel = submitBtn.textContent;

    function say(message, state) {
      statusEl.textContent = message;
      if (state) { statusEl.setAttribute("data-state", state); }
      else { statusEl.removeAttribute("data-state"); }
    }

    function markInvalid(field, invalid) {
      if (!field) { return; }
      if (invalid) { field.setAttribute("aria-invalid", "true"); }
      else { field.removeAttribute("aria-invalid"); }
    }

    function busy(isBusy) {
      submitBtn.disabled = isBusy;
      if (isBusy) {
        idleLabel = submitBtn.textContent;
        submitBtn.textContent = t("form.sending", "Sending…");
      } else {
        submitBtn.textContent = idleLabel;
      }
    }

    function validate() {
      var company = form.elements.company;
      var email = form.elements.email;
      var message = form.elements.message;

      [company, email, message].forEach(function (f) { markInvalid(f, false); });

      if (!company.value.trim()) {
        markInvalid(company, true);
        return { ok: false, field: company, text: t("msg.company", "Add your company name.") };
      }
      if (!email.value.trim() || !email.checkValidity()) {
        markInvalid(email, true);
        return { ok: false, field: email, text: t("msg.email", "Add a valid work email address.") };
      }
      if (message.value.trim().length < 20) {
        markInvalid(message, true);
        return {
          ok: false, field: message,
          text: t("msg.message", "Describe the problem in a line or two — at least 20 characters.")
        };
      }
      return { ok: true };
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();

      /* Abierto con file://: no hay servidor al que enviar. Se dice claramente
         en vez de fallar en silencio. */
      if (window.location.protocol === "file:") {
        say(t("msg.fileProtocol", "Open the site over http:// to send the form."), "error");
        return;
      }

      /* Honeypot: si viene lleno es un bot. Se acepta en silencio para no darle
         al script la señal de que fue detectado. */
      var honeypot = form.elements.website;
      if (honeypot && honeypot.value !== "") {
        say(t("msg.thanks", "Thanks — we will be in touch."), null);
        return;
      }

      if (renderedAt) {
        var elapsed = (Date.now() - Number(renderedAt.value)) / 1000;
        if (elapsed < MIN_FILL_SECONDS) {
          say(t("msg.tooFast", "Take a moment to describe the problem, then send."), "error");
          return;
        }
      }

      var check = validate();
      if (!check.ok) {
        say(check.text, "error");
        if (check.field) { check.field.focus(); }
        return;
      }

      /* practice.value siempre va en inglés: el idioma cambia la etiqueta visible
         del <option>, nunca el valor que el backend valida contra su lista blanca. */
      var payload = {
        company: form.elements.company.value.trim(),
        email: form.elements.email.value.trim(),
        practice: form.elements.practice.value,
        message: form.elements.message.value.trim(),
        website: "",
        rendered_at: renderedAt ? Number(renderedAt.value) : 0,
        locale: window.ttsI18n ? window.ttsI18n.current : "en"
      };

      var controller = new AbortController();
      var timer = setTimeout(function () { controller.abort(); }, REQUEST_TIMEOUT_MS);

      busy(true);
      say(t("msg.sending", "Sending your message…"), "sending");

      fetch(API_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(payload),
        credentials: "same-origin",
        signal: controller.signal
      })
        .then(function (response) {
          clearTimeout(timer);
          if (response.ok) {
            form.reset();
            if (renderedAt) { renderedAt.value = String(Date.now()); }
            say(t("msg.sent", "Message sent."), null);
            return;
          }
          if (response.status === 429) { say(t("msg.rate", "Too many messages."), "error"); return; }
          if (response.status === 400 || response.status === 422) {
            say(t("msg.invalid", "Some fields need fixing."), "error");
            return;
          }
          say(t("msg.error", "The message could not be sent right now."), "error");
        })
        .catch(function () {
          clearTimeout(timer);
          say(t("msg.connection", "Connection problem — the message was not sent."), "error");
        })
        .then(function () { busy(false); });
    });
  })();
})();
