#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).with_name("apply_release_v25.py")
text = path.read_text(encoding="utf-8")
old_open = "    return f'''<script id=\"kvass-language-data\" type=\"application/json\">{safe_json}</script>"
new_open = "    return f\"\"\"<script id=\"kvass-language-data\" type=\"application/json\">{safe_json}</script>"
old_close = "</script>'''\n'''\ntext = text[:start] + new_function + text[end:]"
new_close = "</script>\"\"\"\n'''\ntext = text[:start] + new_function + text[end:]"
if old_open not in text:
    raise RuntimeError("Cannot find nested quote opening")
if old_close not in text:
    raise RuntimeError("Cannot find nested quote closing")
text = text.replace(old_open, new_open, 1).replace(old_close, new_close, 1)
path.write_text(text, encoding="utf-8")
print("Fixed nested quotes in apply_release_v25.py")
