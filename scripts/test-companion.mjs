import assert from "node:assert/strict";
import { agentHandoff, assessBatch, decisionTrace, makeBatch } from "../companion/engine.js";
import { normalizeConsent, normalizeLanguage, resolvePreferredLanguage } from "../companion/preferences.js";

const now = new Date("2026-07-21T12:00:00Z");
const started = new Date("2026-07-20T12:00:00Z");

function batchWith(overrides = {}) {
  return makeBatch({name:"Test",volumeL:3,sugarG:110,startedAt:started,temperatureC:22,surface:"clear",smell:"bread",taste:"sweet",seal:"cloth",...overrides},now);
}

assert.equal(assessBatch(batchWith(), now).verdict,"on_track");
assert.equal(assessBatch(batchWith({surface:"mold"}), now).verdict,"stop");
assert.equal(assessBatch(batchWith({smell:"rotten"}), now).verdict,"stop");
assert.equal(assessBatch(batchWith({temperatureC:35}), now).verdict,"stop");
assert.equal(assessBatch(batchWith({temperatureC:28,sunlight:true}), now).verdict,"act_now");
assert.equal(assessBatch(batchWith({seal:"tight"}), now).action,"release_pressure");
assert.equal(assessBatch(batchWith({taste:"balanced"}), now).verdict,"ready");

const hotTrace = decisionTrace(batchWith({temperatureC:28,sunlight:true}), now);
assert.equal(hotTrace.status,"danger");
assert.equal(hotTrace.signals.find(signal => signal.key === "temperature").status,"watch");
assert.equal(hotTrace.signals.find(signal => signal.key === "sunlight").status,"danger");
assert.deepEqual(hotTrace.unknowns,["microbiological_safety","starter_activity"]);
assert.equal(agentHandoff(batchWith({temperatureC:28,sunlight:true}), now).decision_trace.signals.length,6);
assert.equal("alcohol_estimate" in agentHandoff(batchWith(), now),false);

assert.equal(resolvePreferredLanguage("ru", ["de-DE"]), "ru");
assert.equal(resolvePreferredLanguage(null, ["es-MX", "en-US"]), "es");
assert.equal(resolvePreferredLanguage(null, ["zh-Hans-CN"]), "zh-CN");
assert.equal(resolvePreferredLanguage(null, ["zh-SG"]), "zh-CN");
assert.equal(resolvePreferredLanguage(null, ["el-GR"]), "el");
assert.equal(resolvePreferredLanguage("xx", ["fr-FR"]), "en");
assert.equal(normalizeLanguage("de-DE"), "de");
for (const language of ["ru", "en", "es", "de", "zh-CN", "el"]) {
  assert.equal(resolvePreferredLanguage(language, ["fr-FR"]), language);
}
assert.equal(normalizeConsent("essential"), "essential");
assert.equal(normalizeConsent("all"), "all");
assert.equal(normalizeConsent("maybe"), null);

console.log("KVASSISTENT companion: 29 deterministic rule, language, and consent checks passed");
