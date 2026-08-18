/*
  Prueba de una página de caso en un DOM real.

      npm install jsdom
      node tests/case-pages.check.js cg-legal-phishing
      for s in cg-legal-phishing attack-surface-automation reporting-engine granelco aaif; do
        node tests/case-pages.check.js $s
      done
*/
let JSDOM;
try { ({ JSDOM } = require("jsdom")); }
catch (e) { console.error("Falta jsdom. Instálalo con:  npm install jsdom"); process.exit(1); }
const fs = require("fs"), path = require("path");
const ROOT = path.resolve(__dirname, "..");
const SLUG = process.argv[2] || "cg-legal-phishing";

const dom = new JSDOM(fs.readFileSync(path.join(ROOT, "work", SLUG, "index.html"), "utf8"), {
  runScripts: "dangerously", url: "http://127.0.0.1:8000/work/" + SLUG + "/", pretendToBeVisual: true
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
check("migas traducidas", document.querySelector('[data-i18n="cs.crumbHome"]').textContent === "Inicio");
check("nav común traducido", document.querySelector('[data-i18n="nav.practices"]').textContent === "Prácticas");
check("form común traducido", document.querySelector('[data-i18n="form.company"]').textContent === "Empresa");
check("conclusión traducida", /[áéíóúñ¿]/i.test(document.querySelector('[data-i18n="cs.lesson"]').textContent));
check("métricas presentes", document.querySelectorAll(".metric").length === 4);
check("consentimiento presente", document.querySelector(".consent") !== null);
check("resultados traducidos", document.querySelector('[data-i18n="cs.resH"]').textContent.includes("números"));
check("value del option intacto", sel.value !== "" && !/[áéíóúñ]/.test(sel.value), sel.value);

// ninguna clave sin traducir (quedaría el inglés): comparar contra el HTML original
const untranslated = [...document.querySelectorAll('[data-i18n^="cs."]')]
  .filter(el => el.textContent.trim() !== "" && /^(Home|Case studies|The situation|What we did|Results|The takeaway|At a glance)$/.test(el.textContent.trim()));
check("sin claves cs.* en inglés", untranslated.length === 0,
      untranslated.map(e=>e.getAttribute("data-i18n")+":"+e.textContent).join(", "));

console.log("["+SLUG+"] PASAN "+ok.length+(bad.length?"  FALLAN "+bad.length:""));
bad.forEach(b=>console.log("   FALLA "+b));
errors.forEach(e=>console.log("   JS ERROR "+e));
process.exit(bad.length||errors.length?1:0);
