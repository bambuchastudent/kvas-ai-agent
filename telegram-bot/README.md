# KVASSISTENT Telegram bot

A minimal Cloudflare Worker webhook bot for friendly feedback about a planned kvass batch.

Default reply:

> Какой хороший квас ты задумал! Вот это молодец — ай да хорош! 🥤

## Secrets

Never commit the Telegram token.

Configure these Worker secrets:

- `TELEGRAM_BOT_TOKEN` — required token from BotFather.
- `TELEGRAM_WEBHOOK_SECRET` — recommended random secret used to validate Telegram webhook requests.

Example with Wrangler:

```bash
wrangler secret put TELEGRAM_BOT_TOKEN
wrangler secret put TELEGRAM_WEBHOOK_SECRET
```

## Deploy

Create or select a Cloudflare Worker and deploy `worker.js` as its module entry point. The Worker needs no database and stores no chat history.

After deployment, register the webhook, replacing the placeholders locally:

```bash
curl -fsS "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -H 'content-type: application/json' \
  -d "{\"url\":\"https://YOUR-WORKER.workers.dev/\",\"secret_token\":\"${TELEGRAM_WEBHOOK_SECRET}\"}"
```

Do not paste the token into source files, commits, issues, pull requests, screenshots, or public logs.

## Behaviour

- `GET /` returns a small health response.
- `/start` introduces KVASSISTENT and asks what kvass the user has planned.
- Any ordinary text receives the encouraging reply.
- Updates without a chat message are acknowledged without sending anything.
