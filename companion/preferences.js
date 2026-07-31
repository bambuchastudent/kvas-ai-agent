export const SUPPORTED_LANGUAGES = Object.freeze(["ru", "en", "es", "de", "zh-CN", "el"]);
export const CONSENT_VALUES = Object.freeze(["essential", "all"]);

export function normalizeLanguage(value) {
  if (typeof value !== "string") return null;
  const normalized = value.trim().toLowerCase();
  if (normalized === "zh" || normalized.startsWith("zh-")) return "zh-CN";
  return SUPPORTED_LANGUAGES.find(language => language.toLowerCase() === normalized)
    ?? SUPPORTED_LANGUAGES.find(language => normalized.startsWith(`${language.toLowerCase()}-`))
    ?? null;
}

export function resolvePreferredLanguage(storedLanguage, deviceLanguages = []) {
  const stored = normalizeLanguage(storedLanguage);
  if (stored) return stored;
  for (const candidate of deviceLanguages) {
    const language = normalizeLanguage(candidate);
    if (language) return language;
  }
  return "en";
}

export function normalizeConsent(value) {
  return CONSENT_VALUES.includes(value) ? value : null;
}
