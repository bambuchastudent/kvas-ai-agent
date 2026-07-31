export const CONTINENT_IDS = Object.freeze([
  "north-america",
  "south-america",
  "europe",
  "africa",
  "asia",
  "oceania",
]);

export const COUNTDOWN_SECONDS = 10;

export function createGameState(saved = {}) {
  return {
    total: Number(saved.total) || 0,
    counts: Object.fromEntries(
      CONTINENT_IDS.map(id => [id, Number(saved.counts?.[id]) || 0]),
    ),
    index: Number.isInteger(Number(saved.index)) ? Number(saved.index) : 0,
    paused: false,
    seconds: COUNTDOWN_SECONDS,
  };
}

export function registerLaunch(state, id) {
  if (!CONTINENT_IDS.includes(id)) {
    throw new RangeError(`Unknown launch site: ${id}`);
  }
  state.total += 1;
  state.counts[id] += 1;
  state.index = (CONTINENT_IDS.indexOf(id) + 1) % CONTINENT_IDS.length;
  state.seconds = COUNTDOWN_SECONDS;
  return state;
}

export function advanceCountdown(state) {
  if (state.paused) return null;
  state.seconds -= 1;
  if (state.seconds > 0) return null;
  return CONTINENT_IDS[state.index % CONTINENT_IDS.length];
}

export function nearestLaunchSite(pointerX, pointerY, centers) {
  if (!Number.isFinite(pointerX) || !Number.isFinite(pointerY) || !centers.length) {
    return CONTINENT_IDS[0];
  }

  return centers.reduce((best, candidate) => {
    const dx = pointerX - candidate.x;
    const dy = pointerY - candidate.y;
    const distance = dx * dx + dy * dy;
    return distance < best.distance ? { id: candidate.id, distance } : best;
  }, { id: centers[0].id, distance: Number.POSITIVE_INFINITY }).id;
}
