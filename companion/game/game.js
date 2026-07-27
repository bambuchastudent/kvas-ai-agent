import { GAME_I18N, resolveGameLanguage } from "./i18n.js";

(() => {
  const ids = ["north-america", "south-america", "europe", "africa", "asia", "oceania"];
  const stateKey = "kvassistent-globe-v16";
  const legacyKey = "kvassistent-globe-v14";
  const languageKey = "kvassistent-language";
  const saved = JSON.parse(localStorage.getItem(stateKey) || localStorage.getItem(legacyKey) || "{}");
  const state = {
    total: Number(saved.total) || 0,
    counts: Object.fromEntries(ids.map(id => [id, Number(saved.counts?.[id]) || 0])),
    index: Number(saved.index) || 0,
    paused: false,
    seconds: 10,
  };

  const totalEls = [document.getElementById("total"), document.getElementById("corner-total")];
  const countdown = document.getElementById("countdown");
  const globe = document.getElementById("globe");
  const sites = [...document.querySelectorAll(".site")];
  const stats = document.getElementById("continent-stats");
  const pause = document.getElementById("pause");
  const sound = document.getElementById("sound");
  const languageSelect = document.getElementById("game-language");
  let audioOn = false;
  let language = resolveGameLanguage(localStorage.getItem(languageKey), navigator.languages || [navigator.language]);

  function copy() {
    return GAME_I18N[language] || GAME_I18N.en;
  }

  function save() {
    localStorage.setItem(stateKey, JSON.stringify({ total: state.total, counts: state.counts, index: state.index }));
  }

  function applyLanguage(nextLanguage) {
    language = GAME_I18N[nextLanguage] ? nextLanguage : "en";
    localStorage.setItem(languageKey, language);
    languageSelect.value = language;
    const t = copy();
    document.documentElement.lang = t.htmlLang;
    document.title = t.pageTitle;
    document.querySelector('meta[name="description"]')?.setAttribute("content", t.description);

    document.querySelectorAll("[data-game-i18n]").forEach(element => {
      const value = t[element.dataset.gameI18n];
      if (typeof value === "string") element.textContent = value;
    });

    document.querySelectorAll("[data-continent-label]").forEach(element => {
      element.textContent = t.shortContinents[element.dataset.continentLabel];
    });

    sites.forEach(site => {
      site.setAttribute("aria-label", t.launchFrom(t.continents[site.dataset.id]));
    });
    stats.setAttribute("aria-label", t.statsLabel);
    sound.textContent = audioOn ? t.soundOn : t.soundOff;
    pause.textContent = state.paused ? t.resume : t.pause;
    render();
  }

  function render() {
    const t = copy();
    totalEls.forEach(element => { element.textContent = state.total.toLocaleString(t.locale); });
    countdown.textContent = state.seconds;
    sites.forEach(site => { site.querySelector("small").textContent = state.counts[site.dataset.id].toLocaleString(t.locale); });
    stats.innerHTML = ids.map(id => `<article><span>${t.continents[id]}</span><strong>${state.counts[id].toLocaleString(t.locale)}</strong></article>`).join("");
  }

  function beep() {
    if (!audioOn) return;
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return;
    const context = new AudioContextClass();
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    oscillator.type = "sine";
    oscillator.frequency.setValueAtTime(180, context.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(620, context.currentTime + 0.22);
    gain.gain.setValueAtTime(0.08, context.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, context.currentTime + 0.28);
    oscillator.connect(gain).connect(context.destination);
    oscillator.start();
    oscillator.stop(context.currentTime + 0.3);
  }

  function launch(id) {
    const site = sites.find(candidate => candidate.dataset.id === id);
    if (!site) return;
    const globeRect = globe.getBoundingClientRect();
    const siteRect = site.getBoundingClientRect();
    const x = siteRect.left - globeRect.left + siteRect.width / 2;
    const y = siteRect.top - globeRect.top + siteRect.height / 2;
    const centerX = globeRect.width / 2;
    const centerY = globeRect.height / 2;
    const vectorX = x - centerX;
    const vectorY = y - centerY;
    const vectorLength = Math.hypot(vectorX, vectorY) || 1;
    const distance = Math.max(innerWidth, innerHeight) * 0.46;
    const rocket = document.createElement("div");
    rocket.className = "rocket launch";
    rocket.style.left = `${x}px`;
    rocket.style.top = `${y}px`;
    rocket.style.setProperty("--dx", `${vectorX / vectorLength * distance}px`);
    rocket.style.setProperty("--dy", `${vectorY / vectorLength * distance}px`);
    rocket.style.setProperty("--angle", `${Math.atan2(vectorY, vectorX) * 180 / Math.PI + 90}deg`);
    rocket.innerHTML = '<i class="cap"></i><i class="bottle"></i><i class="fin l"></i><i class="fin r"></i><i class="flame"></i>';
    globe.appendChild(rocket);
    setTimeout(() => rocket.remove(), 2500);
    state.total += 1;
    state.counts[id] += 1;
    state.index = (ids.indexOf(id) + 1) % ids.length;
    state.seconds = 10;
    save();
    render();
    beep();
  }

  sites.forEach(site => site.addEventListener("click", () => launch(site.dataset.id)));
  document.getElementById("launch-now").addEventListener("click", () => launch(ids[state.index % ids.length]));
  pause.addEventListener("click", () => {
    state.paused = !state.paused;
    pause.textContent = state.paused ? copy().resume : copy().pause;
  });
  document.getElementById("reset").addEventListener("click", () => {
    state.total = 0;
    state.index = 0;
    state.seconds = 10;
    ids.forEach(id => { state.counts[id] = 0; });
    save();
    render();
  });
  sound.addEventListener("click", () => {
    audioOn = !audioOn;
    sound.textContent = audioOn ? copy().soundOn : copy().soundOff;
    sound.setAttribute("aria-pressed", String(audioOn));
  });
  languageSelect.addEventListener("change", event => applyLanguage(event.target.value));

  setInterval(() => {
    if (state.paused) return;
    state.seconds -= 1;
    if (state.seconds <= 0) launch(ids[state.index % ids.length]);
    render();
  }, 1000);

  applyLanguage(language);
})();
