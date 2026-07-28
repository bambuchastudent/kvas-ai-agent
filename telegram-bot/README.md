# KVASSISTENT Telegram bot

The Telegram integration is a Cloudflare Worker that can also run as a Cloudflare Pages advanced-mode `_worker.js`.

It provides:

- a Telegram webhook;
- friendly replies to every message;
- forwarding of user messages to the project owner;
- a website feedback API used by `/telegram/`;
- a protected setup endpoint that registers the webhook and bot commands;
- no chat-history database.

Default reply:

> Какой хороший квас ты задумал! Вот это молодец — ай да хорош! 🥤

## Required secrets

Never commit these values:

- `TELEGRAM_BOT_TOKEN` — token from BotFather;
- `TELEGRAM_WEBHOOK_SECRET` — random secret used to authenticate Telegram webhook requests;
- `TELEGRAM_OWNER_CHAT_ID` — chat ID that receives website feedback and forwarded bot messages;
- `TELEGRAM_ADMIN_SECRET` — random bearer token protecting the setup endpoint.

Optional public variable:

- `TELEGRAM_PUBLIC_USERNAME` — bot username without `@`; it lets `/telegram/` show a direct link without calling `getMe`.

For the current site, add them to the Cloudflare Pages project as encrypted environment variables. The release copies `worker.js` to `dist/site/_worker.js` and publishes `_routes.json` for `/api/telegram/*`.

## Find the owner chat ID

1. Create the bot with BotFather.
2. Send one message to the bot before installing the webhook.
3. Keep the token in a local environment variable and run locally:

```bash
curl -fsS "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates"
```

Use the value at `result[].message.chat.id` as `TELEGRAM_OWNER_CHAT_ID`.

Do not paste the token into source files, issues, PRs, screenshots, public logs, or chat messages.

## Activate the webhook

After version 19 is deployed and the Cloudflare variables exist, call the protected setup endpoint from your machine:

```bash
curl -fsS -X POST \
  "https://kvassistent.pages.dev/api/telegram/admin/setup" \
  -H "Authorization: Bearer ${TELEGRAM_ADMIN_SECRET}"
```

The endpoint performs `getMe`, installs `/start` and `/help`, and calls `setWebhook` with:

```text
https://kvassistent.pages.dev/api/telegram/webhook
```

Check the public status without exposing secrets:

```bash
curl -fsS "https://kvassistent.pages.dev/api/telegram/status"
```

## Routes

- `GET /api/telegram/status` — safe public status and optional bot link;
- `POST /api/telegram/feedback` — website feedback form;
- `POST /api/telegram/webhook` — Telegram Bot API webhook;
- `POST /api/telegram/admin/setup` — protected webhook and command setup;
- all other requests pass through to Cloudflare Pages static assets when `env.ASSETS` is available.

## Behaviour

- `/start` introduces KVASSISTENT and asks what kvass the user has planned;
- `/help` explains how to send an idea or problem;
- ordinary messages receive the encouraging reply;
- messages are forwarded to `TELEGRAM_OWNER_CHAT_ID`;
- website feedback is also delivered to the owner chat;
- updates without a chat message are acknowledged without sending anything;
- the Worker does not persist chat history.
