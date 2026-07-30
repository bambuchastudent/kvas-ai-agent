#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).with_name("build-release.py")
text = path.read_text(encoding="utf-8")
old_required = '        f"Версия {ones_count}, потому что в ней единиц вот столько: {ones_count}. Пересчитай:",\n        f\'href="/v{version}/"\','
new_required = '        f"Версия {ones_count}",\n        f\'href="/v{version}/"\',\n        f">v{version}</a>",'
if old_required in text:
    text = text.replace(old_required, new_required, 1)
elif new_required not in text:
    raise RuntimeError("Cannot find release-version verification block")
text = text.replace(
    'raise RuntimeError(f"Landing page misses release 20 content: {missing}")',
    'raise RuntimeError(f"Landing page misses release {ones_count} content: {missing}")',
)
text = text.replace(
    'if game_html.count(\'class="site"\') != 6 or "VERSION 20" not in game_html:',
    'if game_html.count(\'class="site"\') != 6 or f"VERSION {ones_count}" not in game_html:',
)
path.write_text(text, encoding="utf-8")
print("release 26 build verification now checks canonical short and technical versions")
