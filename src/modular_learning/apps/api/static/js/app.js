/* Modular Learning Web — SPA en Vanilla JS (consume la API del adaptador web). */
"use strict";

const $ = (id) => document.getElementById(id);
const state = { sesion: null, paso: 0, quiz: null, quizIdx: 0, quizResp: [], silaboFile: null, silaboData: null, matFile: null, es: null };

/* ---------- Utilidades ---------- */
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function toast(msg, tipo = "ok") {
  const t = document.createElement("div");
  t.className = `toast ${tipo}`;
  t.textContent = msg;
  $("toasts").appendChild(t);
  setTimeout(() => t.remove(), 5200);
}

function loader(show, text = "Procesando…") {
  $("loader-text").textContent = text;
  $("loader").classList.toggle("hidden", !show);
}

async function api(url, opts = {}) {
  const res = await fetch(url, opts);
  if (!res.ok) {
    let detail = res.statusText;
    try { const j = await res.json(); detail = typeof j.detail === "string" ? j.detail : JSON.stringify(j.detail); } catch (_) { /* sin cuerpo JSON */ }
    throw new Error(detail);
  }
  return res.json();
}
const postJSON = (url, body) => api(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

async function conLoader(texto, fn) {
  loader(true, texto);
  try { return await fn(); }
  catch (e) { toast(e.message, "error"); return null; }
  finally { loader(false); }
}

/* Renderizador Markdown mínimo y seguro (escapa HTML antes de transformar). */
function markdown(src) {
  const bloques = [];
  let t = esc(src).replace(/```(\w*)\n([\s\S]*?)```/g, (_, __, code) => { bloques.push(`<pre><code>${code}</code></pre>`); return `\u0000${bloques.length - 1}\u0000`; });
  t = t.replace(/```(\w*)\n?([\s\S]*)$/g, (_, __, code) => { bloques.push(`<pre><code>${code}</code></pre>`); return `\u0000${bloques.length - 1}\u0000`; });
  const inline = (s) => s
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/(^|[\s(])\*([^*\n]+)\*/g, "$1<em>$2</em>")
    .replace(/\[\[([^\]]+)\]\]/g, "<code>$1</code>");
  const out = [];
  let lista = null;
  const cerrar = () => { if (lista) { out.push(`</${lista}>`); lista = null; } };
  for (const raw of t.split("\n")) {
    const l = raw.trimEnd();
    let m;
    if (/^\u0000\d+\u0000$/.test(l.trim())) { cerrar(); out.push(l.trim()); }
    else if ((m = l.match(/^(#{1,4})\s+(.*)$/))) { cerrar(); out.push(`<h${m[1].length}>${inline(m[2])}</h${m[1].length}>`); }
    else if (/^\s*([-*])\s+/.test(l)) { if (lista !== "ul") { cerrar(); out.push("<ul>"); lista = "ul"; } out.push(`<li>${inline(l.replace(/^\s*[-*]\s+/, ""))}</li>`); }
    else if (/^\s*\d+[.)]\s+/.test(l)) { if (lista !== "ol") { cerrar(); out.push("<ol>"); lista = "ol"; } out.push(`<li>${inline(l.replace(/^\s*\d+[.)]\s+/, ""))}</li>`); }
    else if (/^-{3,}$/.test(l.trim())) { cerrar(); out.push("<hr>"); }
    else if (/^&gt;\s?/.test(l)) { cerrar(); out.push(`<blockquote>${inline(l.replace(/^&gt;\s?/, ""))}</blockquote>`); }
    else if (l.trim() === "") { cerrar(); }
    else { cerrar(); out.push(`<p>${inline(l)}</p>`); }
  }
  cerrar();
  return out.join("\n").replace(/\u0000(\d+)\u0000/g, (_, i) => bloques[+i]);
}

/* ---------- Navegación ---------- */
const TITULOS = {
  dashboard: "Dashboard",
  tutor: "Sesión de tutoría",
  quiz: "Quiz de recuerdo activo",
  silabo: "Extracción de sílabos",
  material: "Ingesta de material",
  plugins: "Gestor de plugins",
  config: "Configuración del Entorno"
};

function mostrarVista(v) {
  document.querySelectorAll(".nav-item").forEach((b) => b.classList.toggle("active", b.dataset.view === v));
  document.querySelectorAll(".view").forEach((s) => s.classList.toggle("active", s.id === `view-${v}`));
  $("view-title").textContent = TITULOS[v] || "Modular Learning";
  $("sidebar").classList.remove("open");
  if (v === "dashboard") cargarDashboard();
  if (v === "tutor") cargarMaterias();
  if (v === "material") { cargarMaterias(); cargarMaterialSync(); }
  if (v === "config") cargarConfig();
}
document.querySelectorAll(".nav-item").forEach((b) => b.addEventListener("click", () => mostrarVista(b.dataset.view)));
$("menu-btn").addEventListener("click", () => $("sidebar").classList.toggle("open"));

/* ---------- Dashboard (ml stats) ---------- */
async function cargarDashboard() {
  try {
    const s = await api("/api/stats");
    const pct = Math.round(s.porcentaje_global);
    $("ring-global").style.setProperty("--pct", pct);
    $("pct-global").textContent = `${pct}%`;
    $("kpis").innerHTML = `
      <div class="kpi c1"><small>Temas totales</small><strong>${s.total_temas}</strong></div>
      <div class="kpi c2"><small>Completados</small><strong>${s.temas_completados}</strong></div>
      <div class="kpi c3"><small>Pendientes</small><strong>${s.total_temas - s.temas_completados}</strong></div>
      <div class="kpi c4"><small>Plugins activos</small><strong>${s.plugins_activos}</strong></div>`;
    const mats = Object.entries(s.materias);
    $("materias-stats").innerHTML = mats.length
      ? mats.map(([n, i]) => `
        <article class="card"><h4>${esc(n)}</h4>
          <div class="progress"><div class="progress-bar" style="width:${i.porcentaje}%"></div></div>
          <div class="meta"><span>${i.completados}/${i.total} temas</span><span>${i.porcentaje.toFixed(1)}%</span></div>
        </article>`).join("")
      : `<p class="muted">Aún no hay cronogramas. Extrae un sílabo para comenzar.</p>`;
  } catch (e) { toast(e.message, "error"); }
}

/* ---------- Materias (compartido) ---------- */
let materiasCache = [];
async function cargarMaterias() {
  try {
    materiasCache = (await api("/api/materias")).materias;
    $("tutor-materia").innerHTML = materiasCache.map((m) => `<option>${esc(m)}</option>`).join("") + `<option value="__nueva__">➕ Añadir nueva asignatura…</option>`;
    $("mat-materia").innerHTML = materiasCache.map((m) => `<option>${esc(m)}</option>`).join("") + `<option value="__nueva__">➕ Añadir nueva asignatura…</option>`;
    cargarClases();
  } catch (e) { toast(e.message, "error"); }
}

/* ---------- Tutoría (ml init) ---------- */
async function cargarClases() {
  const mat = $("tutor-materia").value;
  const esNueva = mat === "__nueva__";
  $("tutor-nueva-wrap").classList.toggle("hidden", !esNueva);
  $("clases-pendientes").classList.add("hidden");
  if (esNueva || !mat) return;
  try {
    const { clases } = await api(`/api/materias/${encodeURIComponent(mat)}/clases`);
    if (!clases.length) return;
    $("clases-lista").innerHTML = clases.map((c, i) => `
      <button class="clase-item" data-i="${i}" type="button">
        <span class="clase-num">${i + 1}</span>
        <div class="clase-body">
          <div class="clase-meta">
            <span class="clase-fecha">📅 ${esc(c.fecha || "Sin fecha")}</span>
            <span class="tag">${esc(c.estado || "pendiente")}</span>
          </div>
          <div class="clase-tema">${esc(c.tema)}</div>
          ${c.contenido ? `<div class="clase-desc">${esc(c.contenido)}</div>` : ""}
        </div>
      </button>
    `).join("");
    $("clases-lista").querySelectorAll(".clase-item").forEach((b) => b.addEventListener("click", () => {
      $("tutor-tema").value = clases[+b.dataset.i].tema;
      $("clases-lista").querySelectorAll(".clase-item").forEach((x) => x.classList.toggle("selected", x === b));
    }));
    $("clases-pendientes").classList.remove("hidden");
  } catch (_) { /* sin cronograma */ }
}
$("tutor-materia").addEventListener("change", cargarClases);

$("tutor-iniciar").addEventListener("click", async () => {
  let materia = $("tutor-materia").value;
  if (materia === "__nueva__") materia = $("tutor-nueva").value.trim();
  const tema = $("tutor-tema").value.trim();
  if (!materia || !tema) return toast("Indica la asignatura y el tema.", "error");
  const data = await conLoader("Generando roadmap con el tutor IA…", () => postJSON("/api/tutoria/iniciar", { materia, tema, nivel_profundidad: $("tutor-nivel").value }));
  if (!data) return;
  state.sesion = data;
  state.paso = 0;
  $("tutor-setup").classList.add("hidden");
  $("tutor-session").classList.remove("hidden");
  $("ses-tema").textContent = data.tema;
  $("ses-meta").textContent = `${data.materia} · Nivel ${data.nivel_profundidad}`;
  const brain = $("ses-brain");
  const partes = [];
  if (data.materiales_asociados.length) partes.push(`🧠 Segundo Cerebro activo: ${data.materiales_asociados.join(", ")}`);
  if (data.subtemas_adicionales.length) partes.push(`Subtemas detectados: ${data.subtemas_adicionales.join(", ")}`);
  brain.textContent = partes.join(" · ");
  brain.classList.toggle("hidden", !partes.length);
  $("roadmap").innerHTML = data.pasos.map((p, i) => `<li id="rm-${i}"><span class="n">${i + 1}</span><div><strong>${esc(p.titulo)}</strong><br><small>${esc(p.descripcion)}</small></div></li>`).join("");
  iniciarPaso(0);
});

function actualizarProgreso() {
  const total = state.sesion.pasos.length;
  document.querySelectorAll("#roadmap li").forEach((li, i) => {
    li.classList.toggle("active", i === state.paso);
    li.classList.toggle("done", i < state.paso);
  });
  $("ses-progress").style.width = `${(state.paso / total) * 100}%`;
  $("ses-progress-txt").textContent = `Paso ${state.paso + 1} de ${total}`;
}

function iniciarPaso(i) {
  state.paso = i;
  actualizarProgreso();
  $("chat-log").innerHTML = "";
  $("btn-siguiente").disabled = true;
  $("btn-siguiente").textContent = i === state.sesion.pasos.length - 1 ? "Finalizar y generar guía 🎓" : "Entendido, siguiente paso ➜";
  const out = $("tutor-output");
  out.innerHTML = "";
  out.classList.add("cursor");
  let texto = "";
  let terminado = false;
  if (state.es) state.es.close();
  const es = new EventSource(`/api/tutoria/${state.sesion.sesion_id}/paso/${i}/stream`);
  state.es = es;
  es.onmessage = (ev) => {
    texto += JSON.parse(ev.data).chunk;
    out.innerHTML = markdown(texto);
  };
  es.addEventListener("fin", () => { terminado = true; es.close(); out.classList.remove("cursor"); $("btn-siguiente").disabled = false; });
  es.addEventListener("error", (ev) => {
    if (terminado) return;
    es.close();
    out.classList.remove("cursor");
    let msg = "Se perdió la conexión con el tutor.";
    if (ev.data) { try { msg = JSON.parse(ev.data).error; } catch (_) { /* mensaje por defecto */ } }
    toast(msg, "error");
    $("btn-siguiente").disabled = false;
  });
  out.scrollIntoView({ behavior: "smooth", block: "start" });
}

function chatMsg(rol, html) {
  const d = document.createElement("div");
  d.className = `msg ${rol}`;
  d.innerHTML = html;
  $("chat-log").appendChild(d);
  d.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

async function enviarDuda() {
  const duda = $("duda-input").value.trim();
  if (!duda) return;
  $("duda-input").value = "";
  chatMsg("user", esc(duda));
  $("duda-enviar").disabled = true;
  try {
    const { respuesta } = await postJSON(`/api/tutoria/${state.sesion.sesion_id}/duda`, { paso: state.paso, duda });
    chatMsg("ia markdown", markdown(respuesta));
  } catch (e) { toast(e.message, "error"); }
  finally { $("duda-enviar").disabled = false; }
}
$("duda-enviar").addEventListener("click", enviarDuda);
$("duda-input").addEventListener("keydown", (e) => { if (e.key === "Enter") enviarDuda(); });

$("btn-siguiente").addEventListener("click", async () => {
  if (state.paso < state.sesion.pasos.length - 1) return iniciarPaso(state.paso + 1);
  const r = await conLoader("Generando guía de estudio y guardando en Obsidian…", () => postJSON(`/api/tutoria/${state.sesion.sesion_id}/finalizar`, {}));
  if (!r) return;
  $("tutor-session").classList.add("hidden");
  $("tutor-final").classList.remove("hidden");
  $("final-status").textContent = r.guardado_obsidian
    ? `✅ Guía guardada en tu bóveda de Obsidian${r.clase_completada ? " y clase marcada como completada." : "."}`
    : "⚠️ No se pudo guardar la guía en Obsidian.";
  $("final-guia").innerHTML = markdown(r.guia);
});

function reiniciarTutor() {
  if (state.es) state.es.close();
  state.sesion = null;
  ["tutor-session", "tutor-final"].forEach((id) => $(id).classList.add("hidden"));
  $("tutor-setup").classList.remove("hidden");
  $("tutor-tema").value = "";
  cargarMaterias();
}
$("btn-nueva").addEventListener("click", reiniciarTutor);
$("btn-cancelar").addEventListener("click", () => { if (confirm("¿Cancelar la sesión actual?")) reiniciarTutor(); });

/* ---------- Quiz (ml quiz) ---------- */
$("quiz-generar").addEventListener("click", async () => {
  const q = await conLoader("Generando preguntas a partir de tus temas completados…", () => api("/api/quiz/generar"));
  if (!q) return;
  Object.assign(state, { quiz: q, quizIdx: 0, quizResp: [] });
  $("quiz-intro").classList.add("hidden");
  $("quiz-result").classList.add("hidden");
  $("quiz-box").classList.remove("hidden");
  mostrarPregunta();
});

function mostrarPregunta() {
  const { preguntas } = state.quiz;
  const p = preguntas[state.quizIdx];
  $("quiz-counter").textContent = `Pregunta ${state.quizIdx + 1}/${preguntas.length}`;
  $("quiz-progress").style.width = `${(state.quizIdx / preguntas.length) * 100}%`;
  $("quiz-enunciado").textContent = p.enunciado;
  $("quiz-opciones").innerHTML = p.opciones.map((o) => `<button class="option">${esc(o)}</button>`).join("");
  $("quiz-next").disabled = true;
  $("quiz-next").textContent = state.quizIdx === preguntas.length - 1 ? "Ver resultados" : "Siguiente";
  $("quiz-opciones").querySelectorAll(".option").forEach((b, i) => b.addEventListener("click", () => {
    $("quiz-opciones").querySelectorAll(".option").forEach((x) => x.classList.remove("selected"));
    b.classList.add("selected");
    state.quizResp[state.quizIdx] = p.opciones[i];
    $("quiz-next").disabled = false;
  }));
}

$("quiz-next").addEventListener("click", async () => {
  if (state.quizIdx < state.quiz.preguntas.length - 1) { state.quizIdx++; return mostrarPregunta(); }
  const r = await conLoader("Evaluando tus respuestas…", () => postJSON("/api/quiz/evaluar", { quiz_id: state.quiz.quiz_id, respuestas: state.quizResp }));
  if (!r) return;
  $("quiz-box").classList.add("hidden");
  const box = $("quiz-result");
  box.classList.remove("hidden");
  box.innerHTML = `
    <h3 class="section-title">📊 Puntuación final</h3>
    <div class="ring score-ring" style="--pct:${r.porcentaje}"><div class="ring-inner"><strong>${r.aciertos}/${r.total}</strong><small>${r.porcentaje}%</small></div></div>
    <div class="review">${r.detalle.map((d, i) => `
      <div class="item ${d.correcto ? "ok" : "bad"}"><strong>${d.correcto ? "✔" : "✖"} ${esc(state.quiz.preguntas[i].enunciado)}</strong><br>
      <small>Tu respuesta: ${esc(d.elegida)}${d.correcto ? "" : ` · Correcta: ${esc(d.respuesta_correcta)}`}</small></div>`).join("")}</div>
    <button class="btn primary" id="quiz-repetir">🔁 Nuevo quiz</button>`;
  $("quiz-repetir").addEventListener("click", () => { box.classList.add("hidden"); $("quiz-intro").classList.remove("hidden"); });
});

/* ---------- Dropzones ---------- */
function dropzone(zoneId, inputId, onFile) {
  const z = $(zoneId), inp = $(inputId);
  z.addEventListener("click", () => inp.click());
  z.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") inp.click(); });
  inp.addEventListener("change", () => inp.files[0] && onFile(inp.files[0]));
  ["dragenter", "dragover"].forEach((ev) => z.addEventListener(ev, (e) => { e.preventDefault(); z.classList.add("over"); }));
  ["dragleave", "drop"].forEach((ev) => z.addEventListener(ev, (e) => { e.preventDefault(); z.classList.remove("over"); }));
  z.addEventListener("drop", (e) => e.dataTransfer.files[0] && onFile(e.dataTransfer.files[0]));
}

/* ---------- Sílabos (ml es) ---------- */
dropzone("silabo-drop", "silabo-file", (f) => {
  state.silaboFile = f;
  $("silabo-file-name").textContent = `📎 ${f.name}`;
  $("silabo-extraer").disabled = false;
});

$("silabo-extraer").addEventListener("click", async () => {
  const fd = new FormData();
  fd.append("archivo", state.silaboFile);
  fd.append("materia", $("silabo-materia").value);
  const r = await conLoader("Analizando sílabo con IA…", () => api("/api/silabo/extraer", { method: "POST", body: fd }));
  if (!r) return;
  state.silaboData = r;
  const datos = r.datos;
  const clases = Array.isArray(datos) ? datos : (datos.clases || datos.cronograma || []);
  $("silabo-result-title").textContent = `${clases.length} clases detectadas · ${r.materia}`;
  const cols = ["fecha", "tema", "objetivo", "contenido", "estado"];
  $("silabo-table").innerHTML = `<thead><tr>${cols.map((c) => `<th>${c}</th>`).join("")}</tr></thead><tbody>${clases.map((c) => `<tr>${cols.map((k) => `<td contenteditable="true" data-k="${k}">${esc(c[k] ?? "")}</td>`).join("")}</tr>`).join("")}</tbody>`;
  $("silabo-result").classList.remove("hidden");
});

$("silabo-guardar").addEventListener("click", async () => {
  const filas = [...$("silabo-table").querySelectorAll("tbody tr")].map((tr) => Object.fromEntries([...tr.querySelectorAll("td")].map((td) => [td.dataset.k, td.textContent.trim()])));
  const orig = state.silaboData.datos;
  const datos = Array.isArray(orig) ? filas : { ...orig, clases: filas };
  const r = await conLoader("Guardando cronograma…", () => postJSON("/api/silabo/guardar", { materia: state.silaboData.materia, datos }));
  if (r) { toast("Cronograma guardado correctamente."); $("silabo-result").classList.add("hidden"); }
});

/* ---------- Ingesta (ml im) ---------- */
// Sincronización Automática estilo Plugin
async function cargarMaterialSync() {
  $("mat-sync-materia").innerHTML = `
    <option value="__todas__">✨ Todas las asignaturas</option>
    ${materiasCache.map((m) => `<option value="${esc(m)}">${esc(m)}</option>`).join("")}
  `;
  escanearMaterial();
}

$("mat-sync-materia").addEventListener("change", escanearMaterial);
$("mat-btn-ajustes").addEventListener("click", () => mostrarVista("config"));

async function escanearMaterial() {
  const mat = $("mat-sync-materia").value;
  try {
    const r = await api(`/api/material/escanear${mat && mat !== "__todas__" ? `?materia=${encodeURIComponent(mat)}` : ""}`);
    const escaneos = r.escaneos || [];
    const totalPend = escaneos.reduce((acc, e) => acc + (e.pendientes?.length || 0), 0);
    const totalOmit = escaneos.reduce((acc, e) => acc + (e.omitidos || 0), 0);
    const algunaExiste = escaneos.some((e) => e.existe);

    $("mat-info-materia").textContent = mat === "__todas__" ? `Todas las asignaturas (${escaneos.length})` : mat;
    $("mat-info-path").textContent = escaneos[0]?.carpeta || "Carpeta no asignada";
    $("mat-info-folder-status").textContent = algunaExiste ? "✔ Carpeta activa" : "⚠️ Carpeta no existe";
    $("mat-info-folder-status").style.color = algunaExiste ? "var(--emerald)" : "var(--rose)";
    $("mat-count-pendientes").textContent = totalPend;
    $("mat-count-omitidos").textContent = totalOmit;

    $("mat-btn-sync").disabled = (totalPend === 0);
    if (totalPend === 0 && algunaExiste) {
      $("mat-btn-sync").textContent = "✔ Todo el material está al día";
    } else {
      $("mat-btn-sync").textContent = `🔄 Sincronizar (${totalPend} nuevos)`;
    }
  } catch (e) {
    toast(e.message, "error");
  }
}

$("mat-btn-sync").addEventListener("click", async () => {
  const mat = $("mat-sync-materia").value;
  $("mat-sync-progress-wrap").classList.remove("hidden");
  $("mat-sync-log").classList.remove("hidden");
  $("mat-sync-log").innerHTML = "";
  $("mat-btn-sync").disabled = true;

  try {
    const res = await fetch("/api/material/sincronizar/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ materia: mat })
    });
    if (!res.ok) throw new Error(res.statusText);

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n\n");
      buffer = lines.pop();

      for (const block of lines) {
        if (!block.trim()) continue;
        if (block.includes("event: fin")) break;
        const match = block.match(/data:\s*(.*)/);
        if (!match) continue;
        const ev = JSON.parse(match[1]);

        if (ev.evento === "inicio") {
          $("mat-sync-progress-bar").style.width = "0%";
          $("mat-sync-progress-txt").textContent = `Iniciando ingesta de ${ev.total} archivos...`;
        } else if (ev.evento === "archivo") {
          const pct = Math.round((ev.indice / ev.total) * 100);
          $("mat-sync-progress-bar").style.width = `${pct}%`;
          $("mat-sync-progress-txt").textContent = `Procesando ${ev.indice} de ${ev.total} (${pct}%)`;
          $("mat-sync-progress-file").textContent = `${ev.materia} · ${ev.archivo}`;

          const item = document.createElement("div");
          item.className = `sync-log-item ${ev.ok ? "ok" : "err"}`;
          item.innerHTML = `
            <div><strong>${esc(ev.archivo)}</strong> <small class="muted">(${esc(ev.materia)})</small></div>
            <div>${ev.ok ? `<span class="tag">Clase ${ev.clase_asignada ?? "X"} · ${ev.afinidad ?? 0}%</span>` : `<span class="muted">${esc(ev.error)}</span>`}</div>
          `;
          $("mat-sync-log").appendChild(item);
          item.scrollIntoView({ behavior: "smooth", block: "nearest" });
        } else if (ev.evento === "fin") {
          $("mat-sync-progress-bar").style.width = "100%";
          $("mat-sync-progress-txt").textContent = `Completado: ${ev.exitosos} procesados, ${ev.fallidos} fallidos.`;
          toast(`Sincronización finalizada: ${ev.exitosos} archivos ingestados.`);
        }
      }
    }
    escanearMaterial();
    cargarDashboard();
  } catch (err) {
    toast(err.message, "error");
  } finally {
    $("mat-btn-sync").disabled = false;
  }
});

// Subida manual puntual
dropzone("mat-drop", "mat-file", (f) => {
  state.matFile = f;
  $("mat-file-name").textContent = `📎 ${f.name}`;
  $("mat-ingestar").disabled = false;
});

$("mat-ingestar").addEventListener("click", async () => {
  let materia = $("mat-materia").value;
  if (materia === "__nueva__") materia = (prompt("Nombre de la nueva asignatura:") || "").trim();
  if (!materia) return toast("Indica la asignatura.", "error");
  const fd = new FormData();
  fd.append("archivo", state.matFile);
  fd.append("materia", materia);
  fd.append("tipo", $("mat-tipo").value);
  const r = await conLoader("Extrayendo conocimiento y alineando con el cronograma…", () => api("/api/material/ingestar", { method: "POST", body: fd }));
  if (!r) return;
  const al = r.alineacion || {};
  $("mat-result").classList.remove("hidden");
  $("mat-result").innerHTML = `
    <h3 class="section-title">✅ ${esc(r.archivo)} ingestado</h3>
    <p class="muted small">Guardado en: ${esc(r.ruta_salida)}</p>
    <p>${al.clase_asignada !== undefined ? `<span class="tag">Clase ${esc(al.clase_asignada)} · afinidad ${esc(al.peso_afinidad)}%</span>` : ""}
       ${r.plugin_actualizado ? `<span class="tag">Memoria de plugin actualizada</span>` : ""}</p>
    <div class="markdown">${markdown(r.contenido_md)}</div>`;
  toast("Material ingestado en Obsidian.");
  $("mat-ingestar").disabled = true;
  $("mat-file-name").textContent = "";
  cargarDashboard();
});

/* ---------- Plugins (ml up) ---------- */
const PLUGINS_UI = {
  "Cisco (Actividades)": ["🌐", "Actividades de redes y Packet Tracer."],
  "Web (Proyectos)": ["💻", "Proyectos de programación web detectados."],
  "Node-RED (Flujos JSON)": ["🔀", "Análisis de flujos JSON de IoT."],
  "Todos": ["⚡", "Actualiza todos los plugins a la vez."],
};

async function cargarPlugins() {
  try {
    const { opciones } = await api("/api/plugins");
    $("plugin-cards").innerHTML = opciones.map((o) => `
      <button class="card plugin-card" data-p="${esc(o)}"><div class="ico">${(PLUGINS_UI[o] || ["🔌"])[0]}</div><h4>${esc(o)}</h4><p>${esc((PLUGINS_UI[o] || ["", ""])[1])}</p></button>`).join("");
    $("plugin-cards").querySelectorAll(".plugin-card").forEach((b) => b.addEventListener("click", async () => {
      const r = await conLoader(`Actualizando ${b.dataset.p}…`, () => postJSON("/api/plugins/actualizar", { seleccion: b.dataset.p }));
      if (!r) return;
      $("plugin-result-title").textContent = `Actualización de plugin: ${r.seleccion}`;
      $("plugin-result-body").innerHTML = markdown(r.resultado);
      $("plugin-result").classList.remove("hidden");
      toast("Plugin actualizado.");
    }));
  } catch (e) { toast(e.message, "error"); }
}

/* ---------- Configuración ---------- */
async function cargarConfig() {
  try {
    const cfg = await api("/api/config");
    $("cfg-carpeta-material").value = cfg.carpeta_material || "";
    $("cfg-ruta-obsidian").value = cfg.ruta_obsidian || "";

    $("cfg-status-material").innerHTML = cfg.carpeta_material_existe
      ? `<span class="path-status ok">✔ Directorio encontrado en disco</span>`
      : `<span class="path-status bad">✖ Directorio no encontrado. Verifica la ruta o créalo.</span>`;

    $("cfg-status-obsidian").innerHTML = cfg.ruta_obsidian_existe
      ? `<span class="path-status ok">✔ Bóveda de Obsidian activa</span>`
      : `<span class="path-status">ℹ Se creará automáticamente al guardar notas si aún no existe</span>`;
  } catch (e) { toast(e.message, "error"); }
}

$("cfg-guardar").addEventListener("click", async () => {
  const mat = $("cfg-carpeta-material").value.trim();
  const obs = $("cfg-ruta-obsidian").value.trim();
  if (!mat || !obs) return toast("Debes completar ambas rutas.", "error");

  const r = await conLoader("Guardando configuración…", () => postJSON("/api/config", {
    carpeta_material: mat,
    ruta_obsidian: obs
  }));
  if (r) {
    toast("Configuración guardada correctamente.");
    cargarConfig();
  }
});

/* ---------- Inicio ---------- */
cargarDashboard();
cargarPlugins();
api("/api/config").then((cfg) => {
  if (!cfg.configurado && !cfg.carpeta_material_existe) {
    toast("💡 Sugerencia: Revisa la pestaña de Configuración para confirmar tus carpetas de estudio.", "ok");
  }
}).catch(() => {});
