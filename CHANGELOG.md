# Changelog

## 1.0.5

- Added mandatory explicit state management for the current kvass batch.
- Added canonical process stages from `planning` to `ready`, plus `discard` and `unknown`.
- Added state guides in Russian, English, Spanish, German, and Simplified Chinese.
- Added `agent-instructions/state.schema.json` and a complete handoff example.
- Added identical publication sources for `summary` and `instructions` in all five languages.
- Added stable section markers and parity validation across translations.
- Added `scripts/build-publication.py` to generate both PDF and HTML from the same rendered source.
- Added 10 versioned PDF files: one summary and one AI-agent instruction per language.
- Added 10 versioned web pages with matching content.
- Added Noto font installation and PDF rendering checks for Cyrillic, Latin, and Chinese.
- Replaced the separate package, release, and Pages workflows with one validated publish pipeline.
- Added automatic update of tag `v1.0.5`, GitHub Release assets, and GitHub Pages.
- Added publication ZIP/TAR bundles and a machine-readable manifest.

## 1.0.4

- Added a dedicated Telegram share landing page with the title **Квас Жижа для ИИ-агента**.
- Added custom Open Graph and Twitter Card metadata for Telegram and other messengers.
- Added a branded share image generated from the user-provided kvass photo.
- Added a versioned share URL: `https://bambuchastudent.github.io/kvas-ai-agent/v1.0.4/`.
- Added `.github/workflows/pages.yml` to deploy the share page through GitHub Pages.
- Added `docs/telegram-sharing.md` and `share/telegram-message.txt`.
- Simplified README and moved the Telegram share link to the top.
- Added panela as a valid replacement for white sugar in the simple recipe.
- Updated package metadata, build script, workflow artifacts, version marker, and release notes to 1.0.4.

## 1.0.3

- Added photo example guidance for a too-thick bread mash / bread slurry.
- Added `docs/photo-examples.md` with visual-control rules.
- Updated README with a new visual-control link and a section for the case when the mash looks like thick porridge.
- Clarified that a thick bread mash should be strained and only the liquid should continue to fermentation.
- Added photo examples to package metadata, build script, workflow artifacts, README structure, and release notes.

## 1.0.2

- Corrected the reproducible baseline for dry bread / crackers.
- Changed 3 l baseline from 400 g dry bread to 180-220 g dry crackers / fully dry bread.
- Added distinction between fully dry crackers and merely stale bread: 250-300 g for stale but not fully dry bread.
- Reduced sugar baseline from 120 g to 100-120 g.
- Reduced malt baseline from 30 g to 20-30 g.
- Reduced rye flour baseline from 20 g to 10-20 g.
- Reduced yeast baseline to 2-3 g fresh yeast or 0.5-1 g dry yeast.
- Added explanation: bread contains mostly starch, while simple kvass needs sugar unless doing a real malt mash with temperature rests.
- Added anonymized community note about the beer comparison and sugar in bread.
- Updated package metadata, build script, workflow artifacts, version marker, README, and release notes to 1.0.2.

## 1.0.1

- Restored the visible project name to **Квас**.
- Kept **«Жижа»** as the project brand, voice, and public-facing nickname.
- Added the main goal: **reproducible household kvass**.
- Added a reproducible baseline protocol: `recipes/kvas-reproducible.md`.
- Added a batch log template: `docs/batch-log-template.md`.
- Added release notes: `release/RELEASE-1.0.1.md`.
- Added package metadata: `package.json`.
- Added package build script: `scripts/build-package.sh`.
- Added GitHub Actions workflow: `.github/workflows/package.yml`.
- Updated README sharing messages to say: project name **Квас**, brand **Жижа**.
- Updated documentation structure from `zhizha/` back to `kvas/`.
- Added a dedicated branding document.
- Kept the existing repository URL unchanged: `bambuchastudent/kvas-ai-agent`.

## v0.4.0

- Renamed the visible project identity to **Жижа**.
- Reframed the project as a small “cathedral and bazaar” for household kvass and fermentation knowledge.
- Added ready-to-copy sharing messages.
- Added a contribution guide.
- Added a manifesto for the project philosophy.
- Added a dedicated sharing document.

## v0.3.0

- Added anonymized community notes.
- Improved the recipe for the case where there are no rye crackers.
- Added rye flour, malt, Borodinsky/rye bread, and malt extract as flavor and color boosters.
- Clarified that rye flour improves body and flavor but does not replace starter or sugar.
- Clarified that hot weather speeds up fermentation.
- Clarified that primary fermentation should not be sealed tightly; cover it with cloth, gauze, or a loose lid.
- Added multilingual agent instructions: Russian, English, Spanish, and German.

## v0.2.0

- Added dates as an alternative to raisins.
- Clarified that dates should be pitted, softened, mashed into a paste, and added after cooling the wort.

## v0.1.0

- Initial household kvass instructions.
- Added base recipe, white bread recipe, raisins notes, safety checklist, and historical notes.
