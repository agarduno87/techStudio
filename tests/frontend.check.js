/*
  Prueba del frontend en un DOM real (jsdom): conmutador de idioma, moneda de la
  calculadora, validación del formulario y accesibilidad del menú.

  Opcional — requiere Node:
      npm install jsdom
      node tests/frontend.check.js

  No hace falta para correr el sitio. Es para tu ciclo de pruebas.
*/
let JSDOM;
try {
  ({ JSDOM } = require("jsdom"));
} catch (e) {
  console.error("Falta jsdom. Instálalo con:  npm install jsdom");
  process.exit(1);
}
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..");

const dom = new JSDOM(fs.readFileSync(path.join(ROOT, "index.html"), "utf8"), {
  runScripts: "dangerously",
  url: "http://127.0.0.1:8123/",
  resources: {
    // Sirve i18n/<code>.js y los <script src> desde disco
    fetch(url) { return null; }
  },
  pretendToBeVisual: true
});
const { window } = dom;
const { document } = window;

// Cargar manualmente los scripts en orden (defer)
function run(file) {
  const code = fs.readFileSync(path.join(ROOT, file), "utf8");
  window.eval(code);
}

const errors = [];
window.addEventListener("error", e => errors.push("window error: " + e.message));
const origError = console.error;

// Interceptar la inyección de <script src="i18n/es.js"> y ejecutarlo desde disco
const origAppend = window.document.head.appendChild.bind(window.document.head);
window.document.head.appendChild = function (node) {
  const r = origAppend(node);
  if (node.tagName === "SCRIPT" && node.src) {
    const rel = node.src.replace("http://127.0.0.1:8123/", "");
    try {
      run(rel);
      if (node.onload) node.onload();
    } catch (e) {
      errors.push("dict load error: " + e.message);
      if (node.onerror) node.onerror();
    }
  }
  return r;
};

try { run("i18n.js"); } catch (e) { errors.push("i18n.js: " + e.message); }
try { run("app.js"); } catch (e) { errors.push("app.js: " + e.message); }

const $ = id => document.getElementById(id);
const ok = [], bad = [];
const check = (name, cond, extra="") => (cond ? ok : bad).push(name + (extra ? " → " + extra : ""));

// 1. Selector de idioma
check("selector visible", $("langSelect") && !$("langSelect").hidden);
check("2 idiomas", $("langSelect").options.length === 2,
      [...$("langSelect").options].map(o=>o.textContent).join("/"));

// 2. Estado inicial en inglés
check("h1 en inglés", document.querySelector("h1").textContent.includes("written scope"));
check("calc inicial USD", $("calcTotal").textContent.includes("USD"), $("calcTotal").textContent);
const usdTotal = $("calcTotal").textContent;

// 3. Calculadora: 4 personas × 6 h × 48 semanas × 25 = 28,800  → y 1,152 horas
$("people").value = "4"; $("hours").value = "6"; $("rate").value = "25";
$("people").dispatchEvent(new window.Event("input"));
check("cálculo USD correcto", $("calcTotal").textContent.replace(/[^\d]/g,"") === "28800",
      $("calcTotal").textContent);
check("horas correctas", $("calcHours").textContent.replace(/[^\d]/g,"") === "1152",
      $("calcHours").textContent);

// 4. Cambio a español
$("langSelect").value = "es";
$("langSelect").dispatchEvent(new window.Event("change"));

check("h1 traducido", document.querySelector("h1").textContent.includes("alcance escrito"),
      document.querySelector("h1").textContent.trim());
check("html lang=es", document.documentElement.lang === "es");
check("nav traducido", document.querySelector('[data-i18n="nav.practices"]').textContent === "Prácticas");
check("práctica 4 traducida", document.querySelector('[data-i18n="p4.t"]').textContent === "Datos, analítica e ingeniería");
check("placeholder traducido",
      document.querySelector('[data-i18n-ph="form.ph.company"]').placeholder === "Tu empresa");

// 5. Moneda en pesos
const esTotal = $("calcTotal").textContent;
check("calc cambia a MXN", /MX|\$/.test(esTotal) && esTotal !== usdTotal, esTotal);
check("tarifa reescalada a MXN", $("rate").value === "400" && $("rate").max === "2000",
      "value=" + $("rate").value + " max=" + $("rate").max);
check("label tarifa en MXN", $("rateLabel").textContent.includes("MXN"), $("rateLabel").textContent);
check("horas en español", $("calcHours").textContent.includes("horas al año"), $("calcHours").textContent);
// 4 × 6 × 48 × 400 = 460,800
check("cálculo MXN correcto", $("calcTotal").textContent.replace(/[^\d]/g,"") === "460800",
      $("calcTotal").textContent);

// 6. Valores del formulario siguen en inglés
const opts = [...document.querySelectorAll('form select[name=practice] option')];
check("option label en español", opts[3].textContent === "Datos y analítica", opts[3].textContent);
check("option VALUE sigue en inglés", opts[3].value === "Data & Analytics", opts[3].value);

// 7. Volver a inglés
$("langSelect").value = "en";
$("langSelect").dispatchEvent(new window.Event("change"));
check("regresa a inglés", document.querySelector('[data-i18n="p4.t"]').textContent === "Data, Analytics & Engineering");
check("moneda regresa a USD", $("rate").value === "25" && $("rate").max === "120");

// 8. URL refleja idioma
$("langSelect").value = "es";
$("langSelect").dispatchEvent(new window.Event("change"));
check("URL con ?lang=es", window.location.search.includes("lang=es"), window.location.search);

// 9. Menú accesible
$("burger").dispatchEvent(new window.MouseEvent("click"));
check("aria-expanded true", $("burger").getAttribute("aria-expanded") === "true");
check("aria-label traducido", $("burger").getAttribute("aria-label") === "Cerrar menú",
      $("burger").getAttribute("aria-label"));
$("burger").dispatchEvent(new window.MouseEvent("click"));
check("aria-expanded false", $("burger").getAttribute("aria-expanded") === "false");

// 10. Validación del formulario sin backend
const form = $("contactForm");
$("renderedAt").value = String(Date.now() - 10000);   // pasar la trampa de tiempo
form.elements.company.value = "";
form.dispatchEvent(new window.Event("submit", { cancelable: true, bubbles: true }));
check("valida empresa vacía", $("formStatus").textContent.includes("empresa"), $("formStatus").textContent);

$("renderedAt").value = String(Date.now());            // trampa de tiempo activa
form.elements.company.value = "ACME";
form.dispatchEvent(new window.Event("submit", { cancelable: true, bubbles: true }));
check("trampa de tiempo dispara", $("formStatus").textContent.includes("momento"), $("formStatus").textContent);

check("moneda con código", $("calcTotal").textContent.includes("MXN"), $("calcTotal").textContent);

console.log("\n=== PASAN (" + ok.length + ") ===");
ok.forEach(o => console.log("  ok    " + o));
if (bad.length) { console.log("\n=== FALLAN (" + bad.length + ") ==="); bad.forEach(b => console.log("  FALLA " + b)); }
if (errors.length) { console.log("\n=== ERRORES JS ==="); errors.forEach(e => console.log("  " + e)); }
process.exit(bad.length || errors.length ? 1 : 0);
