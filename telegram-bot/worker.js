const PRAISE = "Какой хороший квас ты задумал! Вот это молодец — ай да хорош! 🥤";
const MAX_MESSAGE = 2000;

function json(data, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
      ...extraHeaders,
    },
  });
}

function clean(value, maxLength) {
  return String(value || "").trim().slice(0, maxLength);
}

function isAllowedOrigin(request) {
  const origin = request.headers.get("origin");
  if (!origin) return true;
  const current = new URL(request.url).origin;
  return origin === current || origin === "https://kvassistent.pages.dev" || /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin);
}

function cors(request) {
  const origin = request.headers.get("origin");
  return {
    "access-control-allow-origin": origin && isAllowedOrigin(request) ? origin : "https://kvassistent.pages.dev",
    "access-control-allow-methods": "GET,POST,OPTIONS",
    "access-control-allow-headers": "content-type,authorization,x-telegram-bot-api-secret-token",
    "access-control-max-age": "86400",
    vary: "Origin",
  };
}

async function telegram(token, method, payload = {}) {
  const response = await fetch(`https://api.telegram.org/bot${token}/${method}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok || data.ok === false) {
    const description = data.description || `HTTP ${response.status}`;
    throw new Error(`Telegram ${method} failed: ${description}`);
  }
  return data;
}

async function botIdentity(env) {
  let username = clean(env.TELEGRAM_PUBLIC_USERNAME, 80).replace(/^@/, "");
  if (!username && env.TELEGRAM_BOT_TOKEN) {
    try {
      const me = await telegram(env.TELEGRAM_BOT_TOKEN, "getMe");
      username = clean(me.result?.username, 80);
    } catch {
      username = "";
    }
  }
  return {
    username: username || null,
    bot_url: username ? `https://t.me/${username}` : null,
  };
}

async function handleStatus(env) {
  const identity = await botIdentity(env);
  const configured = Boolean(
    env.TELEGRAM_BOT_TOKEN &&
    env.TELEGRAM_WEBHOOK_SECRET &&
    env.TELEGRAM_OWNER_CHAT_ID
  );
  return json({
    ok: true,
    service: "kvassistent-telegram",
    configured,
    feedback_ready: Boolean(env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_OWNER_CHAT_ID),
    ...identity,
  });
}

async function handleFeedback(request, env) {
  if (!isAllowedOrigin(request)) {
    return json({ ok: false, error: "Недопустимый источник запроса" }, 403, cors(request));
  }
  if (!env.TELEGRAM_BOT_TOKEN || !env.TELEGRAM_OWNER_CHAT_ID) {
    return json({ ok: false, error: "Telegram ещё не подключён: нужны секреты бота и chat ID автора" }, 503, cors(request));
  }

  const body = await request.json().catch(() => null);
  if (!body || typeof body !== "object") {
    return json({ ok: false, error: "Неверный формат сообщения" }, 400, cors(request));
  }
  if (clean(body.website, 200)) {
    return json({ ok: true, message: PRAISE }, 200, cors(request));
  }

  const name = clean(body.name, 80) || "Анонимный квасовар";
  const contact = clean(body.contact, 180) || "не указан";
  const message = clean(body.message, MAX_MESSAGE);
  if (message.length < 10) {
    return json({ ok: false, error: "Расскажи о квасе хотя бы в десяти символах" }, 400, cors(request));
  }

  const text = [
    "🥤 Новая обратная связь с kvassistent.pages.dev",
    `От: ${name}`,
    `Контакт: ${contact}`,
    "",
    message,
  ].join("\n");

  await telegram(env.TELEGRAM_BOT_TOKEN, "sendMessage", {
    chat_id: env.TELEGRAM_OWNER_CHAT_ID,
    text,
    disable_web_page_preview: true,
  });

  return json({ ok: true, message: `${PRAISE} Сообщение отправлено автору.` }, 200, cors(request));
}

function senderLabel(message) {
  const from = message?.from || {};
  const name = [from.first_name, from.last_name].filter(Boolean).join(" ").trim();
  const username = from.username ? `@${from.username}` : "";
  return [name, username].filter(Boolean).join(" · ") || `chat ${message?.chat?.id || "unknown"}`;
}

async function handleWebhook(request, env) {
  if (!env.TELEGRAM_BOT_TOKEN || !env.TELEGRAM_WEBHOOK_SECRET) {
    return new Response("telegram secrets are not configured", { status: 503 });
  }
  const provided = request.headers.get("x-telegram-bot-api-secret-token");
  if (provided !== env.TELEGRAM_WEBHOOK_SECRET) {
    return new Response("forbidden", { status: 403 });
  }

  const update = await request.json().catch(() => ({}));
  const message = update.message || update.edited_message;
  const chatId = message?.chat?.id;
  if (!chatId) return new Response("ok");

  const text = clean(message.text, MAX_MESSAGE);
  let answer = PRAISE;
  if (text.startsWith("/start")) {
    answer = `Привет! Я КВАССИСТЕНТ. Расскажи, какой квас ты задумал. ${PRAISE}`;
  } else if (text.startsWith("/help")) {
    answer = "Напиши идею, вопрос или проблему с партией. Я поддержу тебя и передам сообщение автору КВАССИСТЕНТА.";
  }

  await telegram(env.TELEGRAM_BOT_TOKEN, "sendMessage", {
    chat_id: chatId,
    text: answer,
    reply_to_message_id: message.message_id,
    allow_sending_without_reply: true,
  });

  if (env.TELEGRAM_OWNER_CHAT_ID && String(chatId) !== String(env.TELEGRAM_OWNER_CHAT_ID)) {
    const ownerText = [
      "🥤 Сообщение боту КВАССИСТЕНТА",
      `От: ${senderLabel(message)}`,
      `Chat ID: ${chatId}`,
      "",
      text || "[сообщение без текста]",
    ].join("\n");
    await telegram(env.TELEGRAM_BOT_TOKEN, "sendMessage", {
      chat_id: env.TELEGRAM_OWNER_CHAT_ID,
      text: ownerText,
      disable_web_page_preview: true,
    });
  }

  return new Response("ok");
}

async function handleSetup(request, env, url) {
  if (!env.TELEGRAM_ADMIN_SECRET) {
    return json({ ok: false, error: "TELEGRAM_ADMIN_SECRET is not configured" }, 503);
  }
  if (request.headers.get("authorization") !== `Bearer ${env.TELEGRAM_ADMIN_SECRET}`) {
    return json({ ok: false, error: "forbidden" }, 403);
  }
  if (!env.TELEGRAM_BOT_TOKEN || !env.TELEGRAM_WEBHOOK_SECRET) {
    return json({ ok: false, error: "Bot token and webhook secret are required" }, 503);
  }

  const webhookUrl = `${url.origin}/api/telegram/webhook`;
  const me = await telegram(env.TELEGRAM_BOT_TOKEN, "getMe");
  await telegram(env.TELEGRAM_BOT_TOKEN, "setMyCommands", {
    commands: [
      { command: "start", description: "Начать разговор о твоём квасе" },
      { command: "help", description: "Как отправить идею или обратную связь" },
    ],
  });
  await telegram(env.TELEGRAM_BOT_TOKEN, "setWebhook", {
    url: webhookUrl,
    secret_token: env.TELEGRAM_WEBHOOK_SECRET,
    allowed_updates: ["message", "edited_message"],
    drop_pending_updates: false,
  });

  const username = clean(me.result?.username, 80);
  return json({
    ok: true,
    webhook_url: webhookUrl,
    username: username || null,
    bot_url: username ? `https://t.me/${username}` : null,
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS" && url.pathname === "/api/telegram/feedback") {
      return new Response(null, { status: 204, headers: cors(request) });
    }
    if (request.method === "GET" && url.pathname === "/api/telegram/status") {
      return handleStatus(env);
    }
    if (request.method === "POST" && url.pathname === "/api/telegram/feedback") {
      return handleFeedback(request, env);
    }
    if (request.method === "POST" && url.pathname === "/api/telegram/webhook") {
      return handleWebhook(request, env);
    }
    if (request.method === "POST" && url.pathname === "/api/telegram/admin/setup") {
      return handleSetup(request, env, url);
    }

    if (env.ASSETS) return env.ASSETS.fetch(request);
    return json({ ok: true, service: "kvassistent-telegram", path: url.pathname });
  },
};
