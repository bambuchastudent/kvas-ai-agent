import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { GAME_I18N, GAME_LANGUAGE_CODES, normalizeGameLanguage, resolveGameLanguage } from "../companion/game/i18n.js";

const root = path.resolve(import.meta.dirname, "..");
const companionHtml = fs.readFileSync(path.join(root, "companion/index.html"), "utf8");
assert.equal(/[А-Яа-яЁё]/.test(companionHtml), false, "Universal companion HTML must use English static fallback, not Russian");

assert.deepEqual(GAME_LANGUAGE_CODES, ["ru", "en", "es", "de", "zh-CN", "el"]);
for (const code of GAME_LANGUAGE_CODES) {
  const strings = GAME_I18N[code];
  assert.ok(strings, `Missing game locale ${code}`);
  for (const key of ["pageTitle", "heroLead", "statTotal", "launchNow", "maxCarbonationTitle", "sphereTitle"]) {
    assert.equal(typeof strings[key], "string", `${code}.${key} must be translated`);
    assert.ok(strings[key].length > 3, `${code}.${key} is empty`);
  }
  assert.equal(Object.keys(strings.continents).length, 6, `${code} must name six continents`);
  if (code !== "ru") {
    const serialized = JSON.stringify(strings);
    assert.equal(/[А-Яа-яЁё]/.test(serialized), false, `Russian leaked into ${code} game strings`);
  }
}

assert.equal(normalizeGameLanguage("zh-Hans-CN"), "zh-CN");
assert.equal(normalizeGameLanguage("es-MX"), "es");
assert.equal(resolveGameLanguage("de", ["ru-RU"]), "de");
assert.equal(resolveGameLanguage(null, ["fr-FR"]), "en");

const manifest = JSON.parse(fs.readFileSync(path.join(root, "publication/manifest.json"), "utf8"));
assert.deepEqual(manifest.knowledge_sources, ["ru", "en"]);
assert.equal(manifest.fallback_language, "en");
for (const language of manifest.languages) {
  for (const documentType of ["summary", "instructions"]) {
    const documentPath = path.join(root, language[documentType]);
    assert.ok(fs.existsSync(documentPath), `Missing ${language.code} ${documentType}`);
    const text = fs.readFileSync(documentPath, "utf8");
    if (language.code !== "ru") assert.equal(/[А-Яа-яЁё]/.test(text), false, `Russian leaked into ${documentPath}`);
  }
}

console.log("KVASSISTENT localization: six game locales, English fallback, and twelve aligned source documents passed");
