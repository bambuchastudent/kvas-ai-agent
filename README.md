# Квас

**Квас** — открытая база знаний про воспроизводимый домашний квас.

**Бренд проекта: «Жижа».**  
Квас — название. Жижа — характер.

**Текущая версия: 1.0.5**

Языки:

- Русский — этот README;
- [简体中文](README.zh-CN.md).

## Поделиться в Telegram

Отправляй эту ссылку:

**[Квас Жижа для ИИ-агента](https://bambuchastudent.github.io/kvas-ai-agent/v1.0.5/)**

Готовый текст:

```text
Квас Жижа для ИИ-агента

Открытая база знаний про воспроизводимый домашний квас: простой рецепт в граммах, безопасность, состояние текущей партии, журнал и инструкции для ИИ-агентов на русском, английском, испанском, немецком и китайском.

https://bambuchastudent.github.io/kvas-ai-agent/v1.0.5/
```

Подробнее: [`docs/telegram-sharing.md`](docs/telegram-sharing.md).

## Что главное в 1.0.5

ИИ-агент теперь обязан вести **явное состояние партии**.

Он должен знать:

- какой сейчас этап;
- что уже подтверждено пользователем;
- какие данные неизвестны;
- есть ли риск;
- какое одно действие делать следующим;
- что передать другому агенту.

Главные файлы состояния:

- [`agent-instructions/state-model.md`](agent-instructions/state-model.md)
- [`agent-instructions/state.schema.json`](agent-instructions/state.schema.json)
- [`agent-instructions/state-example.json`](agent-instructions/state-example.json)

Состояния процесса:

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

Агент не должен выдумывать температуру, время, ингредиенты и выполненные действия. Неизвестное остаётся `null`.

## Самый простой рецепт на 3 литра

### Что нужно

- вода — 3 л;
- полностью сухие сухари — 180–220 г;
- лучше: 150 г белых + 50–70 г ржаных или Бородинских;
- если хлеб только подсохший — 250–300 г;
- сахар или панела — 100–120 г;
- солод — 20–30 г, если есть;
- или ржаная мука — 10–20 г;
- первая партия:
  - свежие дрожжи — 2–3 г;
  - или сухие — 0,5–1 г;
- следующие партии:
  - 500 мл старого кваса/отжима;
  - или 3–5 ст. л. осадка.

### Как делать

1. Поджарь хлеб до тёмно-золотистого цвета. Не сжигай.
2. Залей кипятком.
3. Оставь на 4–8 часов.
4. Процеди.
5. Для брожения оставь жидкость, а не хлебную кашу.
6. Добавь 100–120 г сахара или панели.
7. Остуди до 25–35°C.
8. Добавь дрожжи или старый квас/осадок.
9. Накрой тканью, марлей или неплотной крышкой.
10. Оставь на 8–12 часов; на жаре проверяй с 6 часов.
11. При нормальном запахе и пузырьках разливай в пластиковые бутылки.
12. На 0,5 л добавь 3 изюминки или 1/2 ч. л. сахара.
13. Догазируй 2–6 часов.
14. Как бутылка стала твёрдой — сразу в холодильник.
15. Охлаждай минимум 8 часов.

## Почему нужен сахар

Хлеб содержит в основном крахмал. Дрожжи не превращают его в сахар сами по себе.

В пиве крахмал превращают ферменты солода во время затирания. В простом хлебном квасе полноценного затирания обычно нет, поэтому добавленная сладость делает брожение, газ и вкус предсказуемее.

Панела заменяет белый сахар примерно 1:1 и даёт более тёмный цвет и паточный вкус.

Мальтоза подходит для брожения, но не заменяет полный вкус и ферменты солода.

## Если получилась густая хлебная каша

Это хлебный затор, а не готовый квас.

1. Процеди ещё раз.
2. Оставь только жидкость.
3. Если жидкость слишком густая — разбавь кипячёной водой.
4. Сладость добавляй уже в итоговую жидкость.
5. В следующей партии уменьши сухари.

Фото-примеры: [`docs/photo-examples.md`](docs/photo-examples.md).

## Когда всё вылить

Установи состояние `discard` и не используй партию, если есть:

- плесень;
- пушистый налёт;
- цветные пятна;
- слизь;
- запах гнили;
- запах ацетона;
- запах мяса или канализации.

Полный чеклист: [`safety/fermentation-checklist.md`](safety/fermentation-checklist.md).

## Как отвечает ИИ-агент

Каждый практический ответ должен иметь три части:

```text
Сейчас: текущее состояние партии.
Следующий шаг: одно конкретное действие.
После этого сообщи: что проверить и написать.
```

Полный JSON состояния показывается только по просьбе или при передаче другому агенту.

## Для ИИ-агентов

Основные инструкции:

- Русский: [`agent-instructions/kvas-agent.md`](agent-instructions/kvas-agent.md)
- English: [`agent-instructions/kvas-agent.en.md`](agent-instructions/kvas-agent.en.md)
- Español: [`agent-instructions/kvas-agent.es.md`](agent-instructions/kvas-agent.es.md)
- Deutsch: [`agent-instructions/kvas-agent.de.md`](agent-instructions/kvas-agent.de.md)
- 简体中文: [`agent-instructions/kvas-agent.zh-CN.md`](agent-instructions/kvas-agent.zh-CN.md)

Модели состояния:

- Русский: [`agent-instructions/state-model.md`](agent-instructions/state-model.md)
- English: [`agent-instructions/state-model.en.md`](agent-instructions/state-model.en.md)
- Español: [`agent-instructions/state-model.es.md`](agent-instructions/state-model.es.md)
- Deutsch: [`agent-instructions/state-model.de.md`](agent-instructions/state-model.de.md)
- 简体中文: [`agent-instructions/state-model.zh-CN.md`](agent-instructions/state-model.zh-CN.md)

ИИ-агент обязан:

- обновлять состояние только по подтверждённым данным;
- не считать совет выполненным без подтверждения;
- сохранять опасные признаки;
- не смешивать разные партии;
- передавать JSON состояния, последнее действие, следующий шаг и неизвестные поля;
- менять только один параметр между тестовыми партиями.

## Воспроизводимость

Записывай:

- вид, состояние и вес хлеба;
- вид и вес сладости;
- солод или муку;
- дрожжи или старый квас;
- температуры;
- время каждого этапа;
- запах, пузырьки и густоту;
- время в бутылках;
- вкус и газированность.

- полный протокол: [`recipes/kvas-reproducible.md`](recipes/kvas-reproducible.md)
- журнал партии: [`docs/batch-log-template.md`](docs/batch-log-template.md)

## Репозиторий

```text
https://github.com/bambuchastudent/kvas-ai-agent
```

Правила участия: [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Сборка пакета

```bash
npm run package
```

Результат:

```text
dist/kvas-1.0.5.zip
dist/kvas-1.0.5.tar.gz
```

GitHub Actions:

- **Build package** — собирает архивы;
- **Deploy Telegram share page** — публикует страницу для Telegram-карточки.

## Главные файлы

```text
README.md
README.zh-CN.md
agent-instructions/kvas-agent.md
agent-instructions/kvas-agent.zh-CN.md
agent-instructions/state-model.md
agent-instructions/state-model.zh-CN.md
agent-instructions/state.schema.json
agent-instructions/state-example.json
recipes/kvas-reproducible.md
docs/batch-log-template.md
docs/telegram-sharing.md
share/index.html
.github/workflows/package.yml
.github/workflows/pages.yml
release/RELEASE-1.0.5.md
```
