# Квас 1.0.5

Бренд: **Жижа**.

## Состав релиза

Релиз 1.0.5 - это одинаково структурированные инструкции и краткие описания на пяти языках, опубликованные одновременно в PDF и на веб-страницах.

Языки:

- русский (`ru`);
- английский (`en`);
- испанский (`es`);
- немецкий (`de`);
- упрощённый китайский (`zh-CN`).

Для каждого языка создаются два документа:

1. `summary` - краткое описание проекта, базовый рецепт, состояние и безопасность;
2. `instructions` - операционная инструкция для ИИ-агента.

## PDF-файлы

```text
kvas-summary-ru-1.0.5.pdf
kvas-instructions-ru-1.0.5.pdf
kvas-summary-en-1.0.5.pdf
kvas-instructions-en-1.0.5.pdf
kvas-summary-es-1.0.5.pdf
kvas-instructions-es-1.0.5.pdf
kvas-summary-de-1.0.5.pdf
kvas-instructions-de-1.0.5.pdf
kvas-summary-zh-CN-1.0.5.pdf
kvas-instructions-zh-CN-1.0.5.pdf
```

## Архивы релиза

```text
manifest.json
kvas-1.0.5-publication.zip
kvas-1.0.5-publication.tar.gz
kvas-1.0.5-website.zip
kvas-1.0.5-website.tar.gz
```

`publication` содержит PDF и исходные Markdown-файлы. `website` содержит полностью собранный статический сайт, который можно открыть или разместить отдельно даже при недоступности GitHub Pages.

## Веб-страницы

Главная страница:

```text
https://bambuchastudent.github.io/kvas-ai-agent/v1.0.5/
```

Для каждого языка публикуются:

```text
/v1.0.5/<lang>/summary/
/v1.0.5/<lang>/instructions/
```

PDF также доступны через сайт:

```text
/v1.0.5/pdfs/
```

## Гарантия одинаковой структуры

Исходные документы находятся в `publication/`.

Каждая секция содержит стабильный идентификатор:

```html
<!-- section:section-id -->
```

Сборщик `scripts/build-publication.py` сравнивает набор и порядок секций между всеми языками. При любом расхождении сборка завершается ошибкой.

Веб-страница и соответствующий PDF создаются из одного и того же HTML. Это исключает расхождение содержания между форматами.

## Проверка PDF

Pipeline проверяет:

- наличие всех 10 PDF;
- количество страниц через `pdfinfo`;
- возможность отрендерить первую страницу через `pdftoppm`;
- наличие шрифтов Noto для кириллицы, латиницы и китайского;
- наличие всех 10 веб-страниц;
- наличие manifest и архивов.

## Состояние ИИ-агента

В инструкции сохранена явная модель состояния:

```text
planning
bread_preparation
infusion
straining
cooling
inoculation
primary_fermentation
ready_to_bottle
bottling
bottle_conditioning
chilling
ready
discard
unknown
```

Неизвестные значения остаются `null`. Этап меняется только после подтверждения пользователя.

## Безопасность

Сохранены флаги:

```text
sealed_primary_fermentation
bottle_overpressure
```

При плесени, пушистом налёте, цветных пятнах, слизи, запахе гнили, ацетона, мяса или канализации партия переводится в `discard`.

## Pipeline

Единый workflow:

```text
.github/workflows/publish.yml
```

Он:

1. собирает и проверяет публикацию;
2. обновляет тег `v1.0.5` на проверенный commit;
3. создаёт или обновляет GitHub Release;
4. загружает все PDF и архивы;
5. публикует сайт в ветку `gh-pages`;
6. дополнительно пытается выполнить GitHub Pages Actions deployment.

GitHub Release создаётся независимо от результата Pages deployment, поэтому PDF и архив сайта появляются в любом случае.

## Заголовок релиза

```text
Квас 1.0.5 - PDFs and multilingual website
```
