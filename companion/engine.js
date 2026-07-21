export const PROTOCOL_VERSION = "kvassistent-live-batch-v1";

const SAFE_SURFACES = new Set(["clear", "foam"]);
const SAFE_SMELLS = new Set(["bread", "sour", "alcohol"]);

function numberOr(value, fallback) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

export function latestCheckin(batch) {
  return batch.checkins[batch.checkins.length - 1];
}

export function elapsedHours(batch, now = new Date()) {
  const started = new Date(batch.startedAt).getTime();
  return Math.max(0, (now.getTime() - started) / 3_600_000);
}

export function makeBatch(input, now = new Date()) {
  const startedAt = input.startedAt ? new Date(input.startedAt) : now;
  const initial = {
    id: globalThis.crypto?.randomUUID?.() || `batch-${now.getTime()}`,
    protocolVersion: PROTOCOL_VERSION,
    name: String(input.name || "My kvass").trim(),
    volumeL: Math.max(0.5, numberOr(input.volumeL, 3)),
    sugarG: Math.max(0, numberOr(input.sugarG, 110)),
    startedAt: startedAt.toISOString(),
    createdAt: now.toISOString(),
    checkins: [],
  };

  return addCheckin(initial, {
    temperatureC: numberOr(input.temperatureC, 22),
    surface: input.surface || "clear",
    smell: input.smell || "bread",
    taste: input.taste || "sweet",
    sunlight: Boolean(input.sunlight),
    seal: input.seal || "cloth",
    notes: input.notes || "",
  }, now);
}

export function addCheckin(batch, input, now = new Date()) {
  const checkin = {
    id: globalThis.crypto?.randomUUID?.() || `checkin-${now.getTime()}`,
    at: now.toISOString(),
    temperatureC: numberOr(input.temperatureC, 22),
    surface: input.surface || "clear",
    smell: input.smell || "bread",
    taste: input.taste || "unknown",
    sunlight: Boolean(input.sunlight),
    seal: input.seal || "cloth",
    notes: String(input.notes || "").trim(),
  };
  return { ...batch, checkins: [...batch.checkins, checkin] };
}

export function assessBatch(batch, now = new Date()) {
  const checkin = latestCheckin(batch);
  const hours = elapsedHours(batch, now);
  const temperature = checkin.temperatureC;
  const issues = [];
  let level = "good";
  let action = "continue";
  let nextCheckHours = 12;

  const raise = (nextLevel, issue) => {
    const rank = { good: 0, watch: 1, danger: 2, stop: 3 };
    if (rank[nextLevel] > rank[level]) level = nextLevel;
    if (!issues.includes(issue)) issues.push(issue);
  };

  if (!SAFE_SURFACES.has(checkin.surface)) raise("stop", `surface_${checkin.surface}`);
  if (!SAFE_SMELLS.has(checkin.smell)) raise("stop", `smell_${checkin.smell}`);
  if (temperature >= 35) raise("stop", "temperature_stop");

  if (level !== "stop") {
    if (checkin.seal === "tight" && hours < 72) raise("danger", "tight_seal");
    if (temperature >= 31) raise("danger", "temperature_hot");
    if (checkin.sunlight) raise(temperature >= 28 ? "danger" : "watch", "direct_sunlight");
    if (hours >= 72 && temperature >= 24) raise("danger", "extended_warm");
    else if (hours >= 48 && temperature >= 24) raise("watch", "warm_too_long");
    if (temperature < 18) raise("watch", "temperature_slow");
    else if (temperature >= 28) raise("watch", "temperature_fast");
  }

  const ready = level !== "stop"
    && hours >= 18
    && hours <= 72
    && SAFE_SURFACES.has(checkin.surface)
    && SAFE_SMELLS.has(checkin.smell)
    && ["balanced", "sour"].includes(checkin.taste);

  if (level === "stop") {
    action = "discard";
    nextCheckHours = null;
  } else if (level === "danger") {
    action = issues.includes("tight_seal") ? "release_pressure" : "move_and_cool";
    nextCheckHours = 1;
  } else if (ready) {
    action = "strain_and_chill";
    nextCheckHours = null;
  } else if (temperature >= 28) {
    action = "shade_check_soon";
    nextCheckHours = 4;
  } else if (temperature >= 25) {
    action = "check_soon";
    nextCheckHours = 6;
  } else if (temperature < 18) {
    action = "warm_gently";
    nextCheckHours = 18;
  } else if (hours >= 18) {
    action = "taste_and_assess";
    nextCheckHours = 4;
  }

  const phase = hours < 18 ? "ferment" : hours < 48 ? "taste" : "finish";
  const progress = Math.min(100, Math.max(6, Math.round((hours / 36) * 100)));
  const nextCheckAt = nextCheckHours === null
    ? null
    : new Date(now.getTime() + nextCheckHours * 3_600_000).toISOString();

  return {
    level,
    verdict: level === "stop" ? "stop" : level === "danger" ? "act_now" : ready ? "ready" : level === "watch" ? "watch" : "on_track",
    action,
    issues,
    ready,
    hours,
    phase,
    progress,
    nextCheckHours,
    nextCheckAt,
  };
}

export function decisionTrace(batch, now = new Date()) {
  const checkin = latestCheckin(batch);
  const assessment = assessBatch(batch, now);
  const hours = assessment.hours;
  const temperature = checkin.temperatureC;
  const rank = { good: 0, watch: 1, danger: 2, stop: 3 };
  const statusFor = (...statuses) => statuses.reduce((best, status) => (
    rank[status] > rank[best] ? status : best
  ), "good");

  return {
    status: assessment.level,
    signals: [
      {
        key: "temperature",
        status: temperature >= 35 ? "stop" : temperature >= 31 ? "danger" : temperature >= 28 || temperature < 18 ? "watch" : "good",
        value: temperature,
      },
      {
        key: "surface",
        status: SAFE_SURFACES.has(checkin.surface) ? "good" : "stop",
        value: checkin.surface,
      },
      {
        key: "smell",
        status: SAFE_SMELLS.has(checkin.smell) ? "good" : "stop",
        value: checkin.smell,
      },
      {
        key: "closure",
        status: checkin.seal === "tight" && hours < 72 ? "danger" : "good",
        value: checkin.seal,
      },
      {
        key: "sunlight",
        status: checkin.sunlight ? (temperature >= 28 ? "danger" : "watch") : "good",
        value: checkin.sunlight,
      },
      {
        key: "timing",
        status: hours >= 72 && temperature >= 24 ? "danger" : hours >= 48 && temperature >= 24 ? "watch" : "good",
        value: Math.round(hours),
      },
    ],
    unknowns: [
      "microbiological_safety",
      "starter_activity",
    ],
    confidence: assessment.level === "stop" ? "high_for_stop_signal" : "household_guidance",
    overall: statusFor(...assessment.issues.map(issue => issue.startsWith("temperature") ? "watch" : "danger"), assessment.level),
  };
}

export function agentHandoff(batch, now = new Date()) {
  const checkin = latestCheckin(batch);
  const assessment = assessBatch(batch, now);
  const trace = decisionTrace(batch, now);
  return {
    protocol_version: PROTOCOL_VERSION,
    batch_id: batch.id,
    batch_name: batch.name,
    stage: assessment.phase,
    started_at: batch.startedAt,
    target_volume_l: batch.volumeL,
    ingredients: { added_sugar_g: batch.sugarG },
    observations: {
      checked_at: checkin.at,
      temperature_c: checkin.temperatureC,
      surface: checkin.surface,
      smell: checkin.smell,
      taste: checkin.taste,
      direct_sunlight: checkin.sunlight,
      closure: checkin.seal,
      notes: checkin.notes || null,
    },
    safety_flags: assessment.issues,
    decision_trace: trace,
    verdict: assessment.verdict,
    next_action: assessment.action,
    unknowns: trace.unknowns,
    updated_from_user_message: false,
  };
}
