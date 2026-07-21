import assert from "node:assert/strict";
import { agentHandoff, assessBatch, decisionTrace, makeBatch } from "../companion/engine.js";

const now = new Date("2026-07-21T12:00:00Z");
const started = new Date("2026-07-20T12:00:00Z");

function batchWith(overrides = {}) {
  return makeBatch({name:"Test",volumeL:3,sugarG:110,startedAt:started,temperatureC:22,surface:"clear",smell:"bread",taste:"sweet",seal:"cloth",...overrides},now);
}

assert.equal(assessBatch(batchWith()).verdict,"on_track");
assert.equal(assessBatch(batchWith({surface:"mold"})).verdict,"stop");
assert.equal(assessBatch(batchWith({smell:"rotten"})).verdict,"stop");
assert.equal(assessBatch(batchWith({temperatureC:35})).verdict,"stop");
assert.equal(assessBatch(batchWith({temperatureC:28,sunlight:true})).verdict,"act_now");
assert.equal(assessBatch(batchWith({seal:"tight"})).action,"release_pressure");
assert.equal(assessBatch(batchWith({taste:"balanced"})).verdict,"ready");

const hotTrace = decisionTrace(batchWith({temperatureC:28,sunlight:true}));
assert.equal(hotTrace.status,"danger");
assert.equal(hotTrace.signals.find(signal => signal.key === "temperature").status,"watch");
assert.equal(hotTrace.signals.find(signal => signal.key === "sunlight").status,"danger");
assert.deepEqual(hotTrace.unknowns,["microbiological_safety","starter_activity"]);
assert.equal(agentHandoff(batchWith({temperatureC:28,sunlight:true})).decision_trace.signals.length,6);
assert.equal("alcohol_estimate" in agentHandoff(batchWith()),false);

console.log("KVASSISTENT companion rule engine: 13 checks passed");
