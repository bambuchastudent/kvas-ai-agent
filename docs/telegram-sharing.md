# Как делиться проектом в Telegram

## Основная ссылка

```text
https://kvassistent.pages.dev/v1.0.6/
```

Страница содержит выбор языка, веб-версии summary и instructions, а также ссылки на соответствующие PDF.

## Готовое сообщение

```text
Квас Жижа для ИИ-агента

Одинаковые краткие описания и инструкции в PDF и на веб-страницах на русском, английском, испанском, немецком и китайском.

https://kvassistent.pages.dev/v1.0.6/
```

## Языковые страницы

```text
https://kvassistent.pages.dev/v1.0.6/ru/summary/
https://kvassistent.pages.dev/v1.0.6/en/summary/
https://kvassistent.pages.dev/v1.0.6/es/summary/
https://kvassistent.pages.dev/v1.0.6/de/summary/
https://kvassistent.pages.dev/v1.0.6/zh-CN/summary/
```

Для инструкции заменить `summary` на `instructions`.

## Telegram-карточка

Главная страница задаёт:

- `og:title`;
- `og:description`;
- `og:image`;
- `og:url`;
- Twitter Card-поля.

Исходное изображение хранится частями:

```text
share/assets/card-1.0.4.b64.part01
...
share/assets/card-1.0.4.b64.part10
```

Сборщик восстанавливает JPEG и публикует его как:

```text
/assets/kvas-zhizha-ai-agent-1.0.6.jpg
```

## Публикация

Единый workflow:

```text
.github/workflows/publish.yml
```

Он одновременно:

1. собирает одинаковые материалы на пяти языках;
2. создаёт и проверяет 10 PDF;
3. обновляет GitHub Release `v1.0.6`;
4. публикует 10 веб-страниц в ветку `gh-pages`;
5. Cloudflare Pages автоматически разворачивает ветку на `kvassistent.pages.dev`.

Содержимое PDF и веб-страницы создаётся из одного HTML, поэтому форматы не расходятся.
