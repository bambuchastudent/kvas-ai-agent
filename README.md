# Квас

**Квассистент — ваш личный помощник по приготовлению кваса.**

[Открыть Квассистент](https://kvassistent.pages.dev/)

**Квас** - открытая база знаний про воспроизводимый домашний квас.

**Бренд: «Жижа».**  
**Версия: 1.1.0.**

В версии 1.1.0 главная страница получила живой золотистый фон с пузырьками и подготовленную галерею реальных успешных напитков сообщества. Добавить свою партию можно через GitHub.

## Что представляет собой релиз 1.1.0

Релиз состоит из одинаково структурированных материалов на пяти языках:

- русский;
- английский;
- испанский;
- немецкий;
- упрощённый китайский.

Для каждого языка автоматически собираются:

1. краткое описание и базовый рецепт;
2. инструкция для ИИ-агента;
3. PDF краткого описания;
4. PDF инструкции;
5. две соответствующие веб-страницы.

Итого релиз содержит **10 PDF-файлов и 10 веб-страниц**.

- [GitHub Release v1.1.0](https://github.com/bambuchastudent/kvas-ai-agent/releases/tag/v1.1.0)
- [Веб-версия 1.1.0](https://kvassistent.pages.dev/v1.1.0/)

## Веб-версия

Главная страница версии:

**https://kvassistent.pages.dev/v1.1.0/**

Структура ссылок:

```text
/v1.1.0/<lang>/summary/
/v1.1.0/<lang>/instructions/
/v1.1.0/pdfs/
/v1.1.0/#gallery
```

Коды языков:

```text
ru
en
es
de
zh-CN
```

## PDF-файлы релиза

```text
kvas-summary-ru-1.1.0.pdf
kvas-instructions-ru-1.1.0.pdf
kvas-summary-en-1.1.0.pdf
kvas-instructions-en-1.1.0.pdf
kvas-summary-es-1.1.0.pdf
kvas-instructions-es-1.1.0.pdf
kvas-summary-de-1.1.0.pdf
kvas-instructions-de-1.1.0.pdf
kvas-summary-zh-CN-1.1.0.pdf
kvas-instructions-zh-CN-1.1.0.pdf
```

Дополнительно публикуются:

```text
manifest.json
kvas-1.1.0-publication.zip
kvas-1.1.0-publication.tar.gz
kvas-1.1.0-website.zip
kvas-1.1.0-website.tar.gz
```

Архивы `publication` содержат PDF и исходные Markdown-файлы. Архивы `website` содержат полностью собранный статический сайт.

## Как обеспечивается одинаковая структура

Исходные материалы находятся в `publication/`.

У каждой переведённой секции есть стабильный идентификатор:

```html
<!-- section:section-id -->
```

Сборка останавливается, если:

- отсутствует язык;
- отсутствует summary или instructions;
- порядок секций отличается;
- версия не равна 1.1.0;
- PDF не создаётся;
- PDF не открывается рендерером;
- веб-страница отсутствует.

Один и тот же HTML используется и для веб-страницы, и для PDF, поэтому содержание форматов не расходится.

## Состояние ИИ-агента

ИИ-агент хранит явное состояние партии:

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

Агент не должен выдумывать температуру, время, ингредиенты и выполненные действия. Неизвестные значения остаются `null`.

Основные файлы:

- [`agent-instructions/state-model.md`](agent-instructions/state-model.md)
- [`agent-instructions/state.schema.json`](agent-instructions/state.schema.json)
- [`agent-instructions/state-example.json`](agent-instructions/state-example.json)

## Базовый рецепт на 3 литра

- вода - 3 л;
- полностью сухие сухари - 180-220 г;
- лучше: 150 г белых + 50-70 г ржаных или Бородинских;
- сахар или панела - 100-120 г;
- солод - 20-30 г или ржаная мука - 10-20 г;
- свежие дрожжи - 2-3 г или сухие - 0,5-1 г.

Короткий процесс:

1. Поджарить хлеб до тёмно-золотистого цвета.
2. Залить кипятком и настоять 4-8 часов.
3. Процедить и оставить только жидкость.
4. Добавить сладость и остудить до 25-35°C.
5. Добавить закваску.
6. Бродить 8-12 часов под тканью или неплотной крышкой.
7. При нормальном запахе и пузырьках разлить в пластиковые бутылки.
8. Догазировать 2-6 часов.
9. Как бутылка стала твёрдой - сразу убрать в холодильник.
10. Охлаждать минимум 8 часов.

## Безопасность

Основное брожение нельзя закрывать герметично.

Партию нужно вылить при:

- плесени;
- пушистом налёте;
- цветных пятнах;
- слизи;
- запахе гнили;
- запахе ацетона;
- запахе мяса или канализации.

## Исходные публикации

```text
publication/ru/summary.md
publication/ru/instructions.md
publication/en/summary.md
publication/en/instructions.md
publication/es/summary.md
publication/es/instructions.md
publication/de/summary.md
publication/de/instructions.md
publication/zh-CN/summary.md
publication/zh-CN/instructions.md
```

## Сборка

```bash
python -m pip install -r requirements-publication.txt
python scripts/build-publication-safe.py
```

Или через npm:

```bash
npm run package
```

Результат создаётся в `dist/`.

## CI/CD

Основной workflow:

```text
.github/workflows/publish.yml
```

Он выполняет полный цикл:

1. проверяет структуру переводов;
2. устанавливает шрифты Noto, включая китайские;
3. собирает 10 PDF и 10 веб-страниц;
4. проверяет PDF через `pdfinfo` и `pdftoppm`;
5. обновляет тег `v1.1.0`;
6. прикладывает все PDF и архивы к GitHub Release;
7. публикует сайт в ветку `gh-pages`;
8. Cloudflare Pages автоматически разворачивает эту ветку;
9. workflow проверяет опубликованную русскую страницу на `kvassistent.pages.dev`.

Проверка уже опубликованных материалов:

```text
.github/workflows/verify-live.yml
```

Она проверяет все 10 PDF в GitHub Release, все языковые веб-страницы и PDF на сайте.

## Репозиторий

https://github.com/bambuchastudent/kvas-ai-agent
