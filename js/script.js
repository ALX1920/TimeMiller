// =========================================================
// TimeMiller — lógica del reloj de dilatación temporal
// =========================================================

// --- CONFIG ---
const START_DATE = new Date("2014-11-07T00:00:00");
const MILLER_RATIO_MS = 7 * 365 * 24 * 60 * 60 * 1000; // ms en la Tierra por 1 hora en Miller

// URL del backend del contador de visitas (Django).
// Déjalo vacío ("") para desactivar el contador sin tocar más código.
// Ejemplo: "https://api.tu-dominio.dev"
const VISITS_API_BASE = "";

const UNIT_LABELS = {
  years: "años",
  months: "meses",
  days: "días",
  hours: "horas",
  minutes: "min",
  seconds: "seg",
};

// --- CÁLCULO DE TIEMPO ---
function breakDownTime(ms) {
  let totalSeconds = Math.floor(ms / 1000);

  const totalDays = Math.floor(totalSeconds / 86400);
  totalSeconds %= 86400;

  const years = Math.floor(totalDays / 365);
  const remainingDays = totalDays % 365;

  const months = Math.floor(remainingDays / 30);
  const days = remainingDays % 30;

  const hours = Math.floor(totalSeconds / 3600);
  totalSeconds %= 3600;

  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  return { years, months, days, hours, minutes, seconds };
}

// --- RENDER DEL PANEL TIPO HUD ---
function renderTimeGrid(containerId, timeObj) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.innerHTML = Object.entries(timeObj)
    .map(([unit, value]) => `
      <div class="time-unit">
        <span class="time-unit__value">${String(value).padStart(2, "0")}</span>
        <span class="time-unit__label">${UNIT_LABELS[unit] ?? unit}</span>
      </div>
    `)
    .join("");
}

// --- CONTADOR DE VISITAS (backend Django, opcional) ---
async function initVisitCounter() {
  const badge = document.getElementById("visits");
  const countEl = document.getElementById("visits-count");
  if (!VISITS_API_BASE || !badge || !countEl) return;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 4000);

  try {
    const response = await fetch(`${VISITS_API_BASE}/api/visits/register/`, {
      method: "POST",
      signal: controller.signal,
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();
    countEl.textContent = data.visits.toLocaleString("es-MX");
    badge.hidden = false;
  } catch (err) {
    // Si el backend no está disponible, no mostramos el contador
    // en vez de romper la página.
    console.debug("Contador de visitas no disponible:", err.message);
    badge.hidden = true;
  } finally {
    clearTimeout(timeout);
  }
}

// --- LOOP PRINCIPAL ---
function updateTime() {
  const now = new Date();

  const earthElapsedMs = now - START_DATE;
  renderTimeGrid("earth-time", breakDownTime(earthElapsedMs));

  const millerElapsedHours = earthElapsedMs / MILLER_RATIO_MS;
  const millerElapsedMs = millerElapsedHours * 60 * 60 * 1000;
  renderTimeGrid("miller-time", breakDownTime(millerElapsedMs));

  const startDateEl = document.getElementById("start-date");
  const currentDateEl = document.getElementById("current-date");
  const infoTextEl = document.getElementById("info-text");

  if (startDateEl) startDateEl.textContent = START_DATE.toLocaleString("es-MX");
  if (currentDateEl) currentDateEl.textContent = now.toLocaleString("es-MX");
  if (infoTextEl) {
    infoTextEl.textContent =
      `El tiempo corre desde el ${START_DATE.toLocaleString("es-MX")}, ` +
      `bajo la regla de que 1 hora en Miller equivale a 7 años en la Tierra.`;
  }
}

setInterval(updateTime, 1000);
updateTime();
initVisitCounter();
