# Как делиться проектом в Telegram

## Основная ссылка

```text
https://bambuchastudent.github.io/kvas-ai-agent/v1.0.5/
```

Страница содержит выбор языка, веб-версии summary и instructions, а также ссылки на соответствующие PDF.

## Готовое сообщение

```text
Квас Жижа для ИИ-агента

Одинаковые краткие описания и инструкции в PDF и на веб-страницах на русском, английском, испанском, немецком и китайском.

https://bambuchastudent.github.io/kvas-ai-agent/v1.0.5/
```

## Языковые страницы

```text
https://bambuchastudent.github.io/kvas-ai-agent/v1.0.5/ru/summary/
https://bambuchastudent.github.io/kvas-ai-agent/v1.0.5/en/summary/
https://bambuchastudent.github.io/kvas-ai-agent/v1.0.5/es/summary/
https://bambuchastudent.github.io/kvas-ai-agent/v1.0.5/de/summary/
https://bambuchastudent.github.io/kvas-ai-agent/v1.0.5/zh-CN/summary/
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
/assets/kvas-zhizha-ai-agent-1.0.5.jpg
```

## Публикация

Единый workflow:

```text
.github/workflows/publish.yml
```

Он одновременно:

1. собирает одинаковые материалы на пяти языках;
2. создаёт и проверяет 10 PDF;
3. обновляет GitHub Release `v1.0.5`;
4. публикует 10 веб-страниц через GitHub Pages.

Содержимое PDF и веб-страницы создаётся из одного HTML, поэтому форматы не расходятся.
