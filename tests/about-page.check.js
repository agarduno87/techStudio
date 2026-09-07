/*
  Prueba de la página About en un DOM real.
      npm install jsdom
      node tests/about-page.check.js
*/
let JSDOM;
try { ({ JSDOM } = require("jsdom")); }
catch (e) { console.error("Falta jsdom. Instálalo con:  npm install jsdom"); process.exit(1); }
const fs = require("fs"), path = require("path");
const ROOT = path.resolve(__dirname, "..");
const SLUG = "about";

const dom = new JSDOM(fs.readFileSync(path.join(ROOT, "about", "index.html"), "utf8"), {
  runScripts: "dangerously", url: "http://127.0.0.1:8000/about/", pretendToBeVisual: true
});
const { window } = dom, { document } = window;
const errors = [];
function run(rel){ window.eval(fs.readFileSync(path.join(ROOT, rel.replace(/^\//,"")), "utf8")); }

const origAppend = document.head.appendChild.bind(document.head);
document.head.appendChild = function(node){
  const r = origAppend(node);
  if (node.tagName === "SCRIPT" && node.src) {
    const rel = node.src.replace("http://127.0.0.1:8000", "");
    try { run(rel); if (node.onload) node.onload(); }
    catch(e){ errors.push("dict "+rel+": "+e.message); if (node.onerror) node.onerror(); }
  }
  return r;
};
try { run("/i18n.js"); run("/app.js"); } catch(e){ errors.push(e.message); }

const $ = id => document.getElementById(id);
const ok=[], bad=[];
const check=(n,c,x="")=>(c?ok:bad).push(n+(x?" → "+x:""));

check("selector visible", $("langSelect") && !$("langSelect").hidden);
check("h1 en inglés", /\w/.test(document.querySelector("h1").textContent));
check("sin calculadora (no rompe)", $("calcTotal") === null);
check("formulario presente", $("contactForm") !== null);
const sel = document.querySelector('select[name=practice]');
check("práctica preseleccionada", sel.value !== "", sel.value);

$("langSelect").value = "es";
$("langSelect").dispatchEvent(new window.Event("change"));

check("h1 traducido", document.querySelector("h1").textContent !== "" && document.documentElement.lang === "es",
      document.querySelector("h1").textContent.slice(0,60));
check("migas traducidas", document.querySelector('[data-i18n="ab.crumbHome"]').textContent === "Inicio");
check("dos personas", document.querySelectorAll(".person").length === 2);
check("dos retratos", document.querySelectorAll(".person-photo img").length === 2);
check("nombres intactos", [...document.querySelectorAll(".person-name")].map(e=>e.textContent).join("|") === "Antonio Garduño|Samuel González",
      [...document.querySelectorAll(".person-name")].map(e=>e.textContent).join("|"));
check("alt traducido", document.querySelector('[data-i18n-alt="ab.p1alt"]').alt.startsWith("Retrato"),
      document.querySelector('[data-i18n-alt="ab.p1alt"]').alt);
check("rol traducido", document.querySelector('[data-i18n="ab.p1role"]').textContent === "Fundador · Director técnico");
check("bio de Samuel traducida", /[áéíóúñ]/.test(document.querySelector('[data-i18n="ab.p2b1"]').textContent));
check("nav común traducido", document.querySelector('[data-i18n="nav.practices"]').textContent === "Prácticas");
check("form común traducido", document.querySelector('[data-i18n="form.company"]').textContent === "Empresa");

check("credenciales traducidas", document.querySelector('[data-i18n="ab.p1ch"]').textContent === "Credenciales");
check("value del option intacto", sel.value !== "" && !/[áéíóúñ]/.test(sel.value), sel.value);

// ninguna clave sin traducir (quedaría el inglés): comparar contra el HTML original
const untranslated = [...document.querySelectorAll('[data-i18n^="ab."]')]
  .filter(el => el.textContent.trim() !== "" && /^(Home|About|Who does the work|Credentials|How we work|The studio)$/.test(el.textContent.trim()));
check("sin claves ab.* en inglés", untranslated.length === 0,
      untranslated.map(e=>e.getAttribute("data-i18n")+":"+e.textContent).join(", "));

console.log("[about] PASAN "+ok.length+(bad.length?"  FALLAN "+bad.length:""));
bad.forEach(b=>console.log("   FALLA "+b));
errors.forEach(e=>console.log("   JS ERROR "+e));
process.exit(bad.length||errors.length?1:0);
