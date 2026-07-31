import { GAME_I18N, resolveGameLanguage } from "./i18n.js";
import {
  CONTINENT_IDS,
  advanceCountdown,
  createGameState,
  nearestLaunchSite,
  registerLaunch,
} from "./game-state.js";

(() => {
  const ids = CONTINENT_IDS;
  const stateKey = "kvassistent-globe-v29";
  const legacyKeys = ["kvassistent-globe-v16", "kvassistent-globe-v14"];
  const languageKey = "kvassistent-language";

  function readSavedState() {
    for (const key of [stateKey, ...legacyKeys]) {
      try {
        const raw = localStorage.getItem(key);
        if (raw) return JSON.parse(raw);
      } catch (error) {
        console.warn(`Ignoring broken game state ${key}`, error);
      }
    }
    return {};
  }

  const state = createGameState(readSavedState());
  const totalEls = [document.getElementById("total"), document.getElementById("corner-total")];
  const countdown = document.getElementById("countdown");
  const globe = document.getElementById("globe");
  const sites = [...document.querySelectorAll(".site")];
  const stats = document.getElementById("continent-stats");
  const pause = document.getElementById("pause");
  const sound = document.getElementById("sound");
  const languageSelect = document.getElementById("game-language");
  const launchNow = document.getElementById("launch-now");
  const reset = document.getElementById("reset");
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
    globe.setAttribute("aria-label", t.globeAria);
    stats.setAttribute("aria-label", t.statsLabel);
    sound.textContent = audioOn ? t.soundOn : t.soundOff;
    pause.textContent = state.paused ? t.resume : t.pause;
    render();
  }

  function render() {
    const t = copy();
    totalEls.forEach(element => { element.textContent = state.total.toLocaleString(t.locale); });
    countdown.textContent = state.seconds;
    sites.forEach(site => {
      site.querySelector("small").textContent = state.counts[site.dataset.id].toLocaleString(t.locale);
    });
    stats.innerHTML = ids
      .map(id => `<article><span>${t.continents[id]}</span><strong>${state.counts[id].toLocaleString(t.locale)}</strong></article>`)
      .join("");
  }

  function beep() {
    if (!audioOn) return;
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return;
    const context = new AudioContextClass();
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    oscillator.type = "sine";
    oscillator.frequency.setValueAtTime(160, context.currentTime);
    oscillator.frequency.exponentialRampToValueAtTime(780, context.currentTime + 0.28);
    gain.gain.setValueAtTime(0.07, context.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, context.currentTime + 0.34);
    oscillator.connect(gain).connect(context.destination);
    oscillator.start();
    oscillator.stop(context.currentTime + 0.36);
  }

  function craftMarkup() {
    return `
      <i class="craft-bottom"></i>
      <i class="craft-body"><b>Ж</b></i>
      <i class="paper-wing left"><span></span></i>
      <i class="paper-wing right"><span></span></i>
      <i class="craft-neck"></i>
      <i class="craft-cap"></i>
      <span class="gas-stream" aria-hidden="true">
        <i class="gas-bubble b1"></i><i class="gas-bubble b2"></i>
        <i class="gas-bubble b3"></i><i class="gas-bubble b4"></i>
        <i class="gas-bubble b5"></i><i class="gas-bubble b6"></i>
      </span>`;
  }

  function launch(id) {
    const site = sites.find(candidate => candidate.dataset.id === id);
    if (!site) return false;

    const globeRect = globe.getBoundingClientRect();
    const siteRect = site.getBoundingClientRect();
    const x = siteRect.left - globeRect.left + siteRect.width / 2;
    const y = siteRect.top - globeRect.top + siteRect.height / 2;
    const centerX = globeRect.width / 2;
    const centerY = globeRect.height / 2;
    const vectorX = x - centerX;
    const vectorY = y - centerY;
    const vectorLength = Math.hypot(vectorX, vectorY) || 1;
    const distance = Math.max(window.innerWidth, window.innerHeight) * 0.5;

    const craft = document.createElement("div");
    craft.className = "gas-craft launch";
    craft.style.left = `${x}px`;
    craft.style.top = `${y}px`;
    craft.style.setProperty("--dx", `${vectorX / vectorLength * distance}px`);
    craft.style.setProperty("--dy", `${vectorY / vectorLength * distance}px`);
    craft.style.setProperty("--angle", `${Math.atan2(vectorY, vectorX) * 180 / Math.PI + 90}deg`);
    craft.innerHTML = craftMarkup();
    globe.appendChild(craft);
    setTimeout(() => craft.remove(), 2600);

    registerLaunch(state, id);
    save();
    render();
    beep();
    return true;
  }

  function siteCenters() {
    return sites.map(site => {
      const rect = site.getBoundingClientRect();
      return { id: site.dataset.id, x: rect.left + rect.width / 2, y: rect.top + rect.height / 2 };
    });
  }

  function resolveLaunchId(event) {
    const directSite = event.target.closest(".site");
    if (directSite && globe.contains(directSite)) return directSite.dataset.id;
    return nearestLaunchSite(event.clientX, event.clientY, siteCenters());
  }

  globe.addEventListener("click", event => {
    launch(resolveLaunchId(event));
  });

  globe.addEventListener("keydown", event => {
    if (event.key !== "Enter" && event.key !== " ") return;
    event.preventDefault();
    launch(ids[state.index % ids.length]);
  });

  launchNow.addEventListener("click", () => launch(ids[state.index % ids.length]));
  pause.addEventListener("click", () => {
    state.paused = !state.paused;
    pause.textContent = state.paused ? copy().resume : copy().pause;
  });
  reset.addEventListener("click", () => {
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
    const autoLaunchId = advanceCountdown(state);
    if (autoLaunchId) launch(autoLaunchId);
    render();
  }, 1000);

  applyLanguage(language);
})();
