# Multilingual publication source

Version: **1.0.5**.

The release and website are generated from the Markdown files in this directory.

For every supported language there are exactly two documents:

- `summary.md` - short project and recipe summary;
- `instructions.md` - complete AI-agent operating instruction.

Supported languages:

- `ru`;
- `en`;
- `es`;
- `de`;
- `zh-CN`.

Every translated document uses stable section markers:

```html
<!-- section:section-id -->
```

`scripts/build-publication.py` refuses to build when the section IDs or their order differ between languages. The same rendered HTML is used for both the web page and its PDF, preventing content drift between formats.

Generated release assets:

```text
kvas-summary-<lang>-1.0.5.pdf
kvas-instructions-<lang>-1.0.5.pdf
kvas-1.0.5-publication.zip
kvas-1.0.5-publication.tar.gz
manifest.json
```

Generated website paths:

```text
/v1.0.5/<lang>/summary/
/v1.0.5/<lang>/instructions/
/v1.0.5/pdfs/
```
