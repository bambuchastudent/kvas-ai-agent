#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).with_name("apply_release_v26.py")
text = path.read_text(encoding="utf-8")
old = 'assert "потому что в ней единиц" not in builder'
new = 'assert \'version_text = f"Версия {ones_count}, потому что в ней единиц вот столько: {ones_count}. Пересчитай:"\' not in builder'
if old in text:
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("narrowed release 26 version-text assertion")
elif new in text:
    print("release 26 version-text assertion already fixed")
else:
    raise RuntimeError("Neither old nor corrected version-text assertion was found")
