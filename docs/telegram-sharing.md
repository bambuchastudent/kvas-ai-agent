# Как делиться КВАССИСТЕНТОМ в Telegram

## Основная ссылка

```text
https://kvassistent.pages.dev/v1.1.1/
```

На главной странице сначала показаны лучшие инструкции для людей, затем отдельные разделы для людей и ИИ-агентов.

## Готовое сообщение

```text
ТВОЙ ЛИЧНЫЙ КВАССИСТЕНТ

ИИ управляет приготовлением кваса «Жижа». Ты делаешь его своими руками. Сначала — лучшие короткие действия для человека, затем — состояние и правила управления для ИИ-агента. PDF и веб-страницы на пяти языках.

Версия 1.1.1 · единиц: 3

https://kvassistent.pages.dev/v1.1.1/
```

## Языковые страницы для людей

```text
https://kvassistent.pages.dev/v1.1.1/ru/summary/
https://kvassistent.pages.dev/v1.1.1/en/summary/
https://kvassistent.pages.dev/v1.1.1/es/summary/
https://kvassistent.pages.dev/v1.1.1/de/summary/
https://kvassistent.pages.dev/v1.1.1/zh-CN/summary/
```

## Языковые страницы для ИИ-агентов

Заменить `summary` на `instructions`:

```text
https://kvassistent.pages.dev/v1.1.1/ru/instructions/
```

## Telegram-карточка

Главная страница задаёт:

- `og:title` — **ТВОЙ ЛИЧНЫЙ КВАССИСТЕНТ**;
- описание человеческой и агентской частей;
- `og:image`;
- `og:url`;
- Twitter Card-поля.

Сборщик публикует изображение как:

```text
/assets/kvassistent-1.1.1.jpg
```

## Публикация

Workflow:

```text
.github/workflows/publish.yml
```

Он читает каноническую версию из:

```text
release/version.json
```

И выполняет:

1. сборку одинаковых материалов на пяти языках;
2. создание и проверку 10 PDF;
3. проверку human-first главной страницы;
4. публикацию GitHub Release `v1.1.1`;
5. публикацию 10 веб-страниц в `gh-pages`;
6. проверку Cloudflare Pages.

Содержимое PDF и соответствующей веб-страницы создаётся из одного HTML.
