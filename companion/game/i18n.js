export const GAME_LANGUAGE_CODES = Object.freeze(["ru", "en", "es", "de", "zh-CN", "el"]);

export const GAME_I18N = Object.freeze({
  ru: {
    htmlLang: "ru", locale: "ru-RU", pageTitle: "КВАССИСТЕНТ 16 · Глобальные запуски",
    description: "КВАССИСТЕНТ 16: игра с глобусом, шестью континентами и бутылками-ракетами.",
    back: "← НА ГЛАВНУЮ", versionLabel: "ВЕРСИЯ 20", language: "Язык", soundOn: "Звук: вкл.", soundOff: "Звук: выкл.",
    heroLead: "Глобальная игра на сфере — плоская только потому, что экран пока не умеет быть шаром. Запускай бутылки с шести континентов и копи результат локально.",
    statTotal: "Запущено бутылок", statAuto: "Автозапуск", statStorage: "Накопление", statMode: "Режим", autoValue: "10 сек", localValue: "локально", modeValue: "6 континентов",
    nextLaunchPrefix: "Следующий пуск через", nextLaunchSuffix: "сек.", launchNow: "ЗАПУСТИТЬ СЕЙЧАС", pause: "Пауза", resume: "Продолжить", reset: "Сбросить локальный счётчик",
    statsLabel: "Запуски по континентам", maxCarbonationTitle: "Максимальная газированность без обещания 0,0%", gameModeLabel: "Игровой режим:",
    maxCarbonationCopy: "максимум пузырьков. Для реального напитка это означает короткий набор газа в пищевой ПЭТ, частую проверку давления и немедленное охлаждение.",
    sphereTitle: "Сфера, которая выглядит плоской только на экране", sphereCopy: "Шесть точек запуска закреплены на глобусе. Нажми на площадку или дождись автоматического пуска каждые десять секунд.",
    continents: {"north-america":"Северная Америка","south-america":"Южная Америка",europe:"Европа",africa:"Африка",asia:"Азия",oceania:"Океания"},
    shortContinents: {"north-america":"СЕВ. АМЕРИКА","south-america":"ЮЖ. АМЕРИКА",europe:"ЕВРОПА",africa:"АФРИКА",asia:"АЗИЯ",oceania:"ОКЕАНИЯ"},
    launchFrom: name => `Запустить из: ${name}`,
  },
  en: {
    htmlLang: "en", locale: "en-GB", pageTitle: "KVASSISTENT 16 · Global launches",
    description: "KVASSISTENT 16: a globe game with six continents and bottle rockets.",
    back: "← HOME", versionLabel: "VERSION 20", language: "Language", soundOn: "Sound: on", soundOff: "Sound: off",
    heroLead: "A global game on a sphere — flat only because your screen has not learned to be round yet. Launch bottles from six continents and keep the score on this device.",
    statTotal: "Bottles launched", statAuto: "Auto launch", statStorage: "Storage", statMode: "Mode", autoValue: "10 sec", localValue: "local", modeValue: "6 continents",
    nextLaunchPrefix: "Next launch in", nextLaunchSuffix: "sec.", launchNow: "LAUNCH NOW", pause: "Pause", resume: "Resume", reset: "Reset local counter",
    statsLabel: "Launches by continent", maxCarbonationTitle: "Maximum carbonation without claiming 0.0%", gameModeLabel: "Game mode:",
    maxCarbonationCopy: "maximum bubbles. For the real drink, use short conditioning in food-grade PET, frequent pressure checks, and immediate chilling.",
    sphereTitle: "A sphere that only looks flat on a screen", sphereCopy: "Six launch sites are fixed to the globe. Tap a site or wait for the automatic launch every ten seconds.",
    continents: {"north-america":"North America","south-america":"South America",europe:"Europe",africa:"Africa",asia:"Asia",oceania:"Oceania"},
    shortContinents: {"north-america":"N. AMERICA","south-america":"S. AMERICA",europe:"EUROPE",africa:"AFRICA",asia:"ASIA",oceania:"OCEANIA"},
    launchFrom: name => `Launch from ${name}`,
  },
  es: {
    htmlLang: "es", locale: "es-ES", pageTitle: "KVASSISTENT 16 · Lanzamientos globales",
    description: "KVASSISTENT 16: juego con globo, seis continentes y botellas cohete.",
    back: "← INICIO", versionLabel: "VERSIÓN 20", language: "Idioma", soundOn: "Sonido: sí", soundOff: "Sonido: no",
    heroLead: "Un juego global sobre una esfera: solo se ve plano porque la pantalla aún no sabe ser redonda. Lanza botellas desde seis continentes y guarda el resultado en este dispositivo.",
    statTotal: "Botellas lanzadas", statAuto: "Lanzamiento auto", statStorage: "Acumulación", statMode: "Modo", autoValue: "10 s", localValue: "local", modeValue: "6 continentes",
    nextLaunchPrefix: "Siguiente lanzamiento en", nextLaunchSuffix: "s", launchNow: "LANZAR AHORA", pause: "Pausa", resume: "Continuar", reset: "Reiniciar contador local",
    statsLabel: "Lanzamientos por continente", maxCarbonationTitle: "Máxima carbonatación sin prometer 0,0%", gameModeLabel: "Modo de juego:",
    maxCarbonationCopy: "máximas burbujas. Para la bebida real: carbonatación corta en PET alimentario, control frecuente de presión y frío inmediato.",
    sphereTitle: "Una esfera que solo parece plana en la pantalla", sphereCopy: "Hay seis puntos de lanzamiento sobre el globo. Pulsa uno o espera el lanzamiento automático cada diez segundos.",
    continents: {"north-america":"Norteamérica","south-america":"Sudamérica",europe:"Europa",africa:"África",asia:"Asia",oceania:"Oceanía"},
    shortContinents: {"north-america":"NORTEAMÉRICA","south-america":"SUDAMÉRICA",europe:"EUROPA",africa:"ÁFRICA",asia:"ASIA",oceania:"OCEANÍA"},
    launchFrom: name => `Lanzar desde ${name}`,
  },
  de: {
    htmlLang: "de", locale: "de-DE", pageTitle: "KVASSISTENT 16 · Globale Starts",
    description: "KVASSISTENT 16: Globusspiel mit sechs Kontinenten und Flaschenraketen.",
    back: "← STARTSEITE", versionLabel: "VERSION 20", language: "Sprache", soundOn: "Ton: an", soundOff: "Ton: aus",
    heroLead: "Ein globales Spiel auf einer Kugel – flach nur, weil dein Bildschirm noch nicht rund sein kann. Starte Flaschen von sechs Kontinenten und speichere den Zähler lokal.",
    statTotal: "Gestartete Flaschen", statAuto: "Autostart", statStorage: "Speicher", statMode: "Modus", autoValue: "10 Sek.", localValue: "lokal", modeValue: "6 Kontinente",
    nextLaunchPrefix: "Nächster Start in", nextLaunchSuffix: "Sek.", launchNow: "JETZT STARTEN", pause: "Pause", resume: "Fortsetzen", reset: "Lokalen Zähler löschen",
    statsLabel: "Starts nach Kontinent", maxCarbonationTitle: "Maximale Kohlensäure ohne 0,0%-Versprechen", gameModeLabel: "Spielmodus:",
    maxCarbonationCopy: "maximale Blasen. Für das echte Getränk: kurze Karbonisierung in lebensmittelechtem PET, häufige Druckkontrolle und sofortiges Kühlen.",
    sphereTitle: "Eine Kugel, die nur auf dem Bildschirm flach wirkt", sphereCopy: "Sechs Startpunkte liegen auf dem Globus. Tippe auf einen Punkt oder warte auf den automatischen Start alle zehn Sekunden.",
    continents: {"north-america":"Nordamerika","south-america":"Südamerika",europe:"Europa",africa:"Afrika",asia:"Asien",oceania:"Ozeanien"},
    shortContinents: {"north-america":"NORDAMERIKA","south-america":"SÜDAMERIKA",europe:"EUROPA",africa:"AFRIKA",asia:"ASIEN",oceania:"OZEANIEN"},
    launchFrom: name => `Start aus ${name}`,
  },
  "zh-CN": {
    htmlLang: "zh-CN", locale: "zh-CN", pageTitle: "KVASSISTENT 16 · 全球发射",
    description: "KVASSISTENT 16：带有六大洲和瓶子火箭的地球游戏。",
    back: "← 返回主页", versionLabel: "第 16 版", language: "语言", soundOn: "声音：开", soundOff: "声音：关",
    heroLead: "球面全球游戏——看起来是平的，只因为屏幕还没学会变成球。从六大洲发射瓶子，并在本设备保存计数。",
    statTotal: "已发射瓶数", statAuto: "自动发射", statStorage: "保存方式", statMode: "模式", autoValue: "10 秒", localValue: "本地", modeValue: "6 大洲",
    nextLaunchPrefix: "距离下次发射", nextLaunchSuffix: "秒", launchNow: "立即发射", pause: "暂停", resume: "继续", reset: "清除本地计数",
    statsLabel: "各大洲发射次数", maxCarbonationTitle: "最大气泡，但不承诺 0.0%", gameModeLabel: "游戏模式：",
    maxCarbonationCopy: "尽量多的气泡。真实饮品应在食品级 PET 中短时间充气，频繁检查压力，并立即冷藏。",
    sphereTitle: "只在屏幕上看起来是平的球体", sphereCopy: "六个发射点固定在地球上。点击任意发射点，或等待每十秒一次的自动发射。",
    continents: {"north-america":"北美洲","south-america":"南美洲",europe:"欧洲",africa:"非洲",asia:"亚洲",oceania:"大洋洲"},
    shortContinents: {"north-america":"北美洲","south-america":"南美洲",europe:"欧洲",africa:"非洲",asia:"亚洲",oceania:"大洋洲"},
    launchFrom: name => `从${name}发射`,
  },
  el: {
    htmlLang: "el", locale: "el-GR", pageTitle: "KVASSISTENT 16 · Παγκόσμιες εκτοξεύσεις",
    description: "KVASSISTENT 16: παιχνίδι με υδρόγειο, έξι ηπείρους και μπουκάλια-πυραύλους.",
    back: "← ΑΡΧΙΚΗ", versionLabel: "ΕΚΔΟΣΗ 20", language: "Γλώσσα", soundOn: "Ήχος: ναι", soundOff: "Ήχος: όχι",
    heroLead: "Παγκόσμιο παιχνίδι πάνω σε σφαίρα — φαίνεται επίπεδο μόνο επειδή η οθόνη δεν έγινε ακόμη μπάλα. Εκτόξευσε μπουκάλια από έξι ηπείρους και κράτησε το σκορ τοπικά.",
    statTotal: "Μπουκάλια που εκτοξεύτηκαν", statAuto: "Αυτόματη εκτόξευση", statStorage: "Αποθήκευση", statMode: "Λειτουργία", autoValue: "10 δευτ.", localValue: "τοπικά", modeValue: "6 ήπειροι",
    nextLaunchPrefix: "Επόμενη εκτόξευση σε", nextLaunchSuffix: "δευτ.", launchNow: "ΕΚΤΟΞΕΥΣΗ ΤΩΡΑ", pause: "Παύση", resume: "Συνέχεια", reset: "Μηδενισμός τοπικού μετρητή",
    statsLabel: "Εκτοξεύσεις ανά ήπειρο", maxCarbonationTitle: "Μέγιστη ανθράκωση χωρίς υπόσχεση 0,0%", gameModeLabel: "Λειτουργία παιχνιδιού:",
    maxCarbonationCopy: "μέγιστες φυσαλίδες. Για το πραγματικό ποτό: σύντομη ανθράκωση σε PET τροφίμων, συχνός έλεγχος πίεσης και άμεση ψύξη.",
    sphereTitle: "Μια σφαίρα που φαίνεται επίπεδη μόνο στην οθόνη", sphereCopy: "Έξι σημεία εκτόξευσης βρίσκονται πάνω στην υδρόγειο. Πάτησε ένα ή περίμενε την αυτόματη εκτόξευση κάθε δέκα δευτερόλεπτα.",
    continents: {"north-america":"Βόρεια Αμερική","south-america":"Νότια Αμερική",europe:"Ευρώπη",africa:"Αφρική",asia:"Ασία",oceania:"Ωκεανία"},
    shortContinents: {"north-america":"Β. ΑΜΕΡΙΚΗ","south-america":"Ν. ΑΜΕΡΙΚΗ",europe:"ΕΥΡΩΠΗ",africa:"ΑΦΡΙΚΗ",asia:"ΑΣΙΑ",oceania:"ΩΚΕΑΝΙΑ"},
    launchFrom: name => `Εκτόξευση από ${name}`,
  },
});

export function normalizeGameLanguage(value) {
  if (typeof value !== "string") return null;
  const normalized = value.trim().toLowerCase();
  if (normalized === "zh" || normalized.startsWith("zh-")) return "zh-CN";
  return GAME_LANGUAGE_CODES.find(code => code.toLowerCase() === normalized)
    ?? GAME_LANGUAGE_CODES.find(code => normalized.startsWith(`${code.toLowerCase()}-`))
    ?? null;
}

export function resolveGameLanguage(storedLanguage, deviceLanguages = []) {
  const stored = normalizeGameLanguage(storedLanguage);
  if (stored) return stored;
  for (const candidate of deviceLanguages) {
    const resolved = normalizeGameLanguage(candidate);
    if (resolved) return resolved;
  }
  return "en";
}
