# Квас 1.0.5

Бренд: **Жижа**.

## Главное изменение

Версия 1.0.5 добавляет явное состояние текущей партии кваса.

ИИ-агент теперь обязан понимать и сохранять:

- текущий этап;
- подтверждённые действия;
- неизвестные данные;
- наблюдения;
- риски;
- следующее безопасное действие;
- данные для передачи другому агенту.

## Состояния процесса

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

## Языки

Версия 1.0.5 включает инструкции для ИИ-агентов на пяти языках:

- русский;
- английский;
- испанский;
- немецкий;
- упрощённый китайский.

Добавлено китайское описание проекта:

```text
README.zh-CN.md
```

## Новые файлы состояния

- `agent-instructions/state-model.md`;
- `agent-instructions/state-model.en.md`;
- `agent-instructions/state-model.es.md`;
- `agent-instructions/state-model.de.md`;
- `agent-instructions/state-model.zh-CN.md`;
- `agent-instructions/state.schema.json`;
- `agent-instructions/state-example.json`.

Китайская инструкция агента:

```text
agent-instructions/kvas-agent.zh-CN.md
```

## Правила состояния

- состояние обновляется только по подтверждённым словам пользователя;
- неизвестные значения остаются `null`;
- агент не считает совет выполненным без подтверждения;
- опасные наблюдения не стираются при смене этапа;
- данные разных партий не смешиваются;
- полный JSON показывается по просьбе или при передаче другому агенту.

## Формат ответа агента

```text
Сейчас: текущее состояние партии.
Следующий шаг: одно конкретное действие.
После этого сообщи: что проверить и написать.
```

## Безопасность

Добавлены системные флаги:

```text
sealed_primary_fermentation
bottle_overpressure
```

Состояние немедленно меняется на `discard` при подтверждении плесени, слизи, цветных пятен, гнилого, ацетонового, мясного или канализационного запаха.

## Передача между агентами

Передаются:

1. краткое человеческое резюме;
2. JSON состояния;
3. последнее подтверждённое действие;
4. следующее безопасное действие;
5. неизвестные поля.

## Telegram

Страница версии:

```text
https://bambuchastudent.github.io/kvas-ai-agent/v1.0.5/
```

Заголовок карточки:

```text
Квас Жижа для ИИ-агента
```

В описание добавлены состояние партии, передача между ИИ-агентами и поддержка пяти языков.

## Пакет

```bash
npm run package
```

Результат:

```text
dist/kvas-1.0.5.zip
dist/kvas-1.0.5.tar.gz
```

В архивы включены:

```text
README.zh-CN.md
agent-instructions/kvas-agent.zh-CN.md
agent-instructions/state-model.zh-CN.md
```

## GitHub Release

Публикацией занимается workflow:

```text
.github/workflows/release.yml
```

Он проверяет согласованность версии, наличие китайской документации, собирает архивы и создаёт или обновляет релиз.

```text
Tag: v1.0.5
Title: Квас 1.0.5 — stateful AI agent
```
