const PRAISE = "Какой хороший квас ты задумал! Вот это молодец — ай да хорош! 🥤";

async function telegram(token, method, payload) {
  const response = await fetch(`https://api.telegram.org/bot${token}/${method}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`Telegram ${method} failed: ${response.status}`);
  }
  return response.json();
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "GET") {
      return Response.json({ ok: true, service: "kvassistent-telegram", path: url.pathname });
    }
    if (request.method !== "POST") {
      return new Response("method not allowed", { status: 405 });
    }
    if (!env.TELEGRAM_BOT_TOKEN) {
      return new Response("TELEGRAM_BOT_TOKEN is not configured", { status: 503 });
    }
    if (env.TELEGRAM_WEBHOOK_SECRET) {
      const provided = request.headers.get("x-telegram-bot-api-secret-token");
      if (provided !== env.TELEGRAM_WEBHOOK_SECRET) {
        return new Response("forbidden", { status: 403 });
      }
    }

    const update = await request.json();
    const message = update.message || update.edited_message;
    const chatId = message?.chat?.id;
    if (!chatId) {
      return new Response("ok");
    }

    const text = String(message.text || "").trim();
    const answer = text === "/start"
      ? `Привет! Я КВАССИСТЕНТ. Расскажи, какой квас ты задумал. ${PRAISE}`
      : PRAISE;

    await telegram(env.TELEGRAM_BOT_TOKEN, "sendMessage", {
      chat_id: chatId,
      text: answer,
      reply_to_message_id: message.message_id,
      allow_sending_without_reply: true,
    });
    return new Response("ok");
  },
};
