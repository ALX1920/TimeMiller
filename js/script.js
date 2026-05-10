
// --- CONFIG ---
const START_DATE = new Date("2014-11-07T00:00:00");
const MILLER_RATIO = 7 * 365 * 24 * 60 * 60 * 1000; // ms per 1 Miller hour

// --- FORMAT HELPERS ---
function formatTime(ms) {
    let totalSeconds = Math.floor(ms / 1000);

    let totalDays = Math.floor(totalSeconds / 86400);
    totalSeconds %= 86400;

    let years = Math.floor(totalDays / 365);
    let days = totalDays % 365;

    let hours = Math.floor(totalSeconds / 3600);
    totalSeconds %= 3600;

    let minutes = Math.floor(totalSeconds / 60);
    let seconds = totalSeconds % 60;

    return {
        years,
        days,
        hours,
        minutes,
        seconds
    };
}

function displayFormatted(id, timeObj) {
    document.getElementById(id).textContent =
        `${timeObj.years} years, ` +
        `${timeObj.days} days, ` +
        `${timeObj.hours} hours, ` +
        `${timeObj.minutes} minutes, ` +
        `${timeObj.seconds} seconds`;
}

// --- LOCAL VISIT COUNTER ---
let visits = localStorage.getItem("timemiller_visits");

if (!visits) {
  visits = 1;
} else {
  visits = parseInt(visits) + 1;
}

localStorage.setItem("timemiller_visits", visits);
document.getElementById("visits").textContent = "Visits: " + visits;


// --- MAIN UPDATE LOOP ---
function updateTime() {
    const now = new Date();

    // Earth elapsed time
    const earthElapsed = now - START_DATE;
    const earthTime = formatTime(earthElapsed);
    displayFormatted("earth-time", earthTime);

    // Miller elapsed time
    const millerElapsed = earthElapsed / MILLER_RATIO; // in Miller hours
    const millerMs = millerElapsed * 60 * 60 * 1000; // convert hours → ms
    const millerTime = formatTime(millerMs);
    displayFormatted("miller-time", millerTime);

    // Update date display
    document.getElementById("start-date").textContent = START_DATE.toLocaleString();
    document.getElementById("current-date").textContent = now.toLocaleString();

    // Info text
    document.getElementById("info-text").textContent =
      `Time has been running since ${START_DATE.toLocaleString()} based on the rule that 1 hour on Miller equals 7 years on Earth.`;
}

setInterval(updateTime, 1000);
updateTime();
