#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).with_name("finalize-release.py")
text = path.read_text(encoding="utf-8")
old = '''    if "</head>" not in text:
        raise RuntimeError(f"HTML page has no closing head: {path}")
    text = text.replace("</head>", metadata + "</head>", 1)
'''
new = '''    if "</head>" not in text:
        # Language aliases and other tiny redirect wrappers intentionally have no full head.
        # They do not need social/discovery metadata; their destination page receives it.
        return
    text = text.replace("</head>", metadata + "</head>", 1)
'''
if old in text:
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("redirect wrappers without </head> are now skipped")
elif new in text:
    print("redirect metadata fix already applied")
else:
    raise RuntimeError("Could not find public metadata head guard")

# This script is intentionally idempotent because release CI may replay it.
