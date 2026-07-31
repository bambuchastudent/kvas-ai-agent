import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const root = process.env.KVASSISTENT_GAME_ROOT || "companion/game";
const stateModule = await import(pathToFileURL(path.resolve(root, "game-state.js")));
const {
  CONTINENT_IDS,
  COUNTDOWN_SECONDS,
  advanceCountdown,
  createGameState,
  nearestLaunchSite,
  registerLaunch,
} = stateModule;

const state = createGameState();
for (const id of CONTINENT_IDS) registerLaunch(state, id);
assert.equal(state.total, CONTINENT_IDS.length);
for (const id of CONTINENT_IDS) assert.equal(state.counts[id], 1);
assert.equal(state.seconds, COUNTDOWN_SECONDS);

const nextState = createGameState({ index: 2 });
for (let second = 1; second < COUNTDOWN_SECONDS; second += 1) {
  assert.equal(advanceCountdown(nextState), null);
}
assert.equal(advanceCountdown(nextState), CONTINENT_IDS[2]);

const centers = [
  { id: "europe", x: 100, y: 100 },
  { id: "oceania", x: 500, y: 400 },
];
assert.equal(nearestLaunchSite(110, 90, centers), "europe");
assert.equal(nearestLaunchSite(480, 410, centers), "oceania");

const [html, script, css] = await Promise.all([
  readFile(path.resolve(root, "index.html"), "utf8"),
  readFile(path.resolve(root, "game.js"), "utf8"),
  readFile(path.resolve(root, "styles.css"), "utf8"),
]);

for (const marker of [
  'id="globe"',
  'tabindex="0"',
  'role="button"',
  'id="launch-now"',
]) assert.ok(html.includes(marker), marker);

for (const marker of [
  'globe.addEventListener("click"',
  'globe.addEventListener("keydown"',
  'closest(".site")',
  "nearestLaunchSite",
  "registerLaunch",
  'class="craft-bottom"',
  'class="craft-neck"',
  'class="craft-cap"',
  'class="paper-wing left"',
  'class="paper-wing right"',
  'class="gas-bubble b1"',
]) assert.ok(script.includes(marker), marker);

for (const marker of [
  "touch-action:manipulation",
  "pointer-events:none",
  ".craft-bottom",
  ".craft-neck",
  ".craft-cap",
  ".paper-wing",
  ".gas-bubble",
  "@keyframes cap-unscrew",
  "@keyframes bubble-exhaust",
]) assert.ok(css.includes(marker), marker);

assert.ok(!script.includes('class="flame"'), "gas craft must not contain a flame element");
assert.ok(!css.includes("@keyframes flame"), "gas craft must not animate fire");

console.log(`KVASSISTENT game checks passed for ${root}: sphere click, keyboard launch, six sites, inverted bottle, bubbles and paper wings`);
