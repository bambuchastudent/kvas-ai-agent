#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).with_name("apply_release_v26.py")
text = path.read_text(encoding="utf-8")
replacements = {
    "    'ACCESSIBILITY_CSS = r\"\"\"': 'ACCESSIBILITY_CSS = rf\"\"\"',\n": "",
    "    '/* kvassistent-safe-interactions-v25 */': '/* kvassistent-safe-interactions-v{ONES} */',\n": "    '/* kvassistent-safe-interactions-v25 */': '/* kvassistent-safe-interactions */',\n",
    "    'marker = \"kvassistent-safe-interactions-v25\"':\n        'marker = f\"kvassistent-safe-interactions-v{ONES}\"',\n": "    'marker = \"kvassistent-safe-interactions-v25\"':\n        'marker = \"kvassistent-safe-interactions\"',\n",
    "    '\"kvassistent-safe-interactions-v25\"':\n        'f\"kvassistent-safe-interactions-v{ONES}\"',\n": "    '\"kvassistent-safe-interactions-v25\"':\n        '\"kvassistent-safe-interactions\"',\n",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"Missing apply-v26 source fragment: {old!r}")
    text = text.replace(old, new)
path.write_text(text, encoding="utf-8")
print("fixed apply_release_v26.py: CSS marker is version-independent")
