export const GAME_LANGUAGE_CODES = Object.freeze(["ru", "en", "es", "de", "zh-CN", "el"]);

export const GAME_I18N = Object.freeze({
  ru: {
    htmlLang: "ru", locale: "ru-RU", pageTitle: "КВАССИСТЕНТ 29 · Полёт на газации",
    description: "КВАССИСТЕНТ 29: нажми в любую точку сферы и запусти перевёрнутую бутылку на пузырьках газации.",
    back: "← НА ГЛАВНУЮ", versionLabel: "ВЕРСИЯ 29", language: "Язык", soundOn: "Звук: вкл.", soundOff: "Звук: выкл.",
    heroLead: "Нажми куда угодно по сфере. Ближайшая площадка отправит перевёрнутую бутылку кваса в космос на пузырьках газации.",
    statTotal: "Запущено бутылок", statAuto: "Автозапуск", statStorage: "Накопление", statMode: "Режим", autoValue: "10 сек", localValue: "локально", modeValue: "6 континентов",
    nextLaunchPrefix: "Следующий пуск через", nextLaunchSuffix: "сек.", launchNow: "ЗАПУСТИТЬ СЕЙЧАС", pause: "Пауза", resume: "Продолжить", reset: "Сбросить локальный счётчик",
    statsLabel: "Запуски по континентам", maxCarbonationTitle: "Двигатель на газации", gameModeLabel: "Игровой режим:",
    maxCarbonationCopy: "горлышко смотрит назад, крышка откручивается, а вместо огня летят пузырьки. Для настоящего напитка КВАССИСТЕНТ целится в безалкогольный квас до 0,5% об.; точное значение подтверждается только измерением.",
    sphereTitle: "Сфера кликабельна целиком", sphereCopy: "Нажатие в любой точке выбирает ближайший из шести континентов. Рулоны туалетной бумаги раскрываются по бокам как крылья аппарата.",
    tapHint: "Нажми на сферу, площадку или Enter.", globeAria: "Запустить бутылку с ближайшего континента",
    continents: {"north-america":"Северная Америка","south-america":"Южная Америка",europe:"Европа",africa:"Африка",asia:"Азия",oceania:"Океания"},
    shortContinents: {"north-america":"СЕВ. АМЕРИКА","south-america":"ЮЖ. АМЕРИКА",europe:"ЕВРОПА",africa:"АФРИКА",asia:"АЗИЯ",oceania:"ОКЕАНИЯ"},
    launchFrom: name => `Запустить из: ${name}`,
  },
  en: {
    htmlLang: "en", locale: "en-GB", pageTitle: "KVASSISTENT 29 · Carbonation flight",
    description: "KVASSISTENT 29: click anywhere on the globe and launch an inverted kvass bottle on carbonation bubbles.",
    back: "← HOME", versionLabel: "VERSION 29", language: "Language", soundOn: "Sound: on", soundOff: "Sound: off",
    heroLead: "Click anywhere on the sphere. The nearest launch site sends an inverted kvass bottle into space on carbonation bubbles.",
    statTotal: "Bottles launched", statAuto: "Auto launch", statStorage: "Storage", statMode: "Mode", autoValue: "10 sec", localValue: "local", modeValue: "6 continents",
    nextLaunchPrefix: "Next launch in", nextLaunchSuffix: "sec.", launchNow: "LAUNCH NOW", pause: "Pause", resume: "Resume", reset: "Reset local counter",
    statsLabel: "Launches by continent", maxCarbonationTitle: "Carbonation drive", gameModeLabel: "Game mode:",
    maxCarbonationCopy: "the neck points backwards, the cap unscrews, and bubbles replace fire. For the real drink, KVASSISTENT targets non-alcoholic kvass up to 0.5% ABV; only measurement can confirm the exact value.",
    sphereTitle: "The whole sphere is clickable", sphereCopy: "A click anywhere selects the nearest of six continents. Toilet-paper rolls unfold on both sides as the craft wings.",
    tapHint: "Tap the sphere, a launch point, or press Enter.", globeAria: "Launch a bottle from the nearest continent",
    continents: {"north-america":"North America","south-america":"South America",europe:"Europe",africa:"Africa",asia:"Asia",oceania:"Oceania"},
    shortContinents: {"north-america":"N. AMERICA","south-america":"S. AMERICA",europe:"EUROPE",africa:"AFRICA",asia:"ASIA",oceania:"OCEANIA"},
    launchFrom: name => `Launch from ${name}`,
  },
  es: {
    htmlLang: "es", locale: "es-ES", pageTitle: "KVASSISTENT 29 · Vuelo por carbonatación",
    description: "KVASSISTENT 29: pulsa cualquier punto del globo y lanza una botella invertida con burbujas de carbonatación.",
    back: "← INICIO", versionLabel: "VERSIÓN 29", language: "Idioma", soundOn: "Sonido: sí", soundOff: "Sonido: no",
    heroLead: "Pulsa cualquier punto de la esfera. El punto más cercano lanza una botella de kvas invertida al espacio con burbujas de carbonatación.",
    statTotal: "Botellas lanzadas", statAuto: "Lanzamiento auto", statStorage: "Acumulación", statMode: "Modo", autoValue: "10 s", localValue: "local", modeValue: "6 continentes",
    nextLaunchPrefix: "Siguiente lanzamiento en", nextLaunchSuffix: "s", launchNow: "LANZAR AHORA", pause: "Pausa", resume: "Continuar", reset: "Reiniciar contador local",
    statsLabel: "Lanzamientos por continente", maxCarbonationTitle: "Motor de carbonatación", gameModeLabel: "Modo de juego:",
    maxCarbonationCopy: "el cuello apunta hacia atrás, la tapa se desenrosca y las burbujas sustituyen al fuego. Para la bebida real, KVASSISTENT busca kvas sin alcohol de hasta 0,5% vol.; solo una medición confirma el valor exacto.",
    sphereTitle: "Toda la esfera es pulsable", sphereCopy: "Una pulsación selecciona el continente más cercano. Dos rollos de papel higiénico se despliegan como alas del aparato.",
    tapHint: "Pulsa la esfera, un punto o Enter.", globeAria: "Lanzar una botella desde el continente más cercano",
    continents: {"north-america":"Norteamérica","south-america":"Sudamérica",europe:"Europa",africa:"África",asia:"Asia",oceania:"Oceanía"},
    shortContinents: {"north-america":"NORTEAMÉRICA","south-america":"SUDAMÉRICA",europe:"EUROPA",africa:"ÁFRICA",asia:"ASIA",oceania:"OCEANÍA"},
    launchFrom: name => `Lanzar desde ${name}`,
  },
  de: {
    htmlLang: "de", locale: "de-DE", pageTitle: "KVASSISTENT 29 · Flug durch Karbonisierung",
    description: "KVASSISTENT 29: Tippe irgendwo auf den Globus und starte eine umgedrehte Kwasflasche mit Karbonisierungsblasen.",
    back: "← STARTSEITE", versionLabel: "VERSION 29", language: "Sprache", soundOn: "Ton: an", soundOff: "Ton: aus",
    heroLead: "Tippe irgendwo auf die Kugel. Der nächste Startpunkt schickt eine umgedrehte Kwasflasche mit Karbonisierungsblasen ins All.",
    statTotal: "Gestartete Flaschen", statAuto: "Autostart", statStorage: "Speicher", statMode: "Modus", autoValue: "10 Sek.", localValue: "lokal", modeValue: "6 Kontinente",
    nextLaunchPrefix: "Nächster Start in", nextLaunchSuffix: "Sek.", launchNow: "JETZT STARTEN", pause: "Pause", resume: "Fortsetzen", reset: "Lokalen Zähler löschen",
    statsLabel: "Starts nach Kontinent", maxCarbonationTitle: "Karbonisierungsantrieb", gameModeLabel: "Spielmodus:",
    maxCarbonationCopy: "der Flaschenhals zeigt nach hinten, der Deckel schraubt sich ab und Blasen ersetzen Feuer. Für das echte Getränk zielt KVASSISTENT auf alkoholfreien Kwas bis 0,5 Vol.-%; nur eine Messung bestätigt den genauen Wert.",
    sphereTitle: "Die ganze Kugel ist anklickbar", sphereCopy: "Ein Klick wählt den nächsten der sechs Kontinente. Toilettenpapierrollen entfalten sich seitlich als Flügel.",
    tapHint: "Kugel, Startpunkt oder Enter drücken.", globeAria: "Flasche vom nächsten Kontinent starten",
    continents: {"north-america":"Nordamerika","south-america":"Südamerika",europe:"Europa",africa:"Afrika",asia:"Asien",oceania:"Ozeanien"},
    shortContinents: {"north-america":"NORDAMERIKA","south-america":"SÜDAMERIKA",europe:"EUROPA",africa:"AFRIKA",asia:"ASIEN",oceania:"OZEANIEN"},
    launchFrom: name => `Start aus ${name}`,
  },
  "zh-CN": {
    htmlLang: "zh-CN", locale: "zh-CN", pageTitle: "KVASSISTENT 29 · 气泡推进飞行",
    description: "KVASSISTENT 29：点击地球任意位置，用碳酸气泡发射倒置的格瓦斯瓶。",
    back: "← 返回主页", versionLabel: "第 29 版", language: "语言", soundOn: "声音：开", soundOff: "声音：关",
    heroLead: "点击球体任意位置。最近的发射点会用碳酸气泡把倒置的格瓦斯瓶送入太空。",
    statTotal: "已发射瓶数", statAuto: "自动发射", statStorage: "保存方式", statMode: "模式", autoValue: "10 秒", localValue: "本地", modeValue: "6 大洲",
    nextLaunchPrefix: "距离下次发射", nextLaunchSuffix: "秒", launchNow: "立即发射", pause: "暂停", resume: "继续", reset: "清除本地计数",
    statsLabel: "各大洲发射次数", maxCarbonationTitle: "碳酸气泡推进器", gameModeLabel: "游戏模式：",
    maxCarbonationCopy: "瓶口朝后，瓶盖旋开，气泡代替火焰。真实饮品以不超过 0.5% 酒精度的无酒精格瓦斯为目标；准确数值只能通过测量确认。",
    sphereTitle: "整个球体都可点击", sphereCopy: "任意点击都会选择最近的大洲。两卷卫生纸在两侧展开，成为飞行器的机翼。",
    tapHint: "点击球体、发射点或按 Enter。", globeAria: "从最近的大洲发射瓶子",
    continents: {"north-america":"北美洲","south-america":"南美洲",europe:"欧洲",africa:"非洲",asia:"亚洲",oceania:"大洋洲"},
    shortContinents: {"north-america":"北美洲","south-america":"南美洲",europe:"欧洲",africa:"非洲",asia:"亚洲",oceania:"大洋洲"},
    launchFrom: name => `从${name}发射`,
  },
  el: {
    htmlLang: "el", locale: "el-GR", pageTitle: "KVASSISTENT 29 · Πτήση με ανθράκωση",
    description: "KVASSISTENT 29: πάτησε οπουδήποτε στην υδρόγειο και εκτόξευσε ένα ανεστραμμένο μπουκάλι κβας με φυσαλίδες ανθράκωσης.",
    back: "← ΑΡΧΙΚΗ", versionLabel: "ΕΚΔΟΣΗ 29", language: "Γλώσσα", soundOn: "Ήχος: ναι", soundOff: "Ήχος: όχι",
    heroLead: "Πάτησε οπουδήποτε στη σφαίρα. Το κοντινότερο σημείο στέλνει ένα ανεστραμμένο μπουκάλι κβας στο διάστημα με φυσαλίδες ανθράκωσης.",
    statTotal: "Μπουκάλια που εκτοξεύτηκαν", statAuto: "Αυτόματη εκτόξευση", statStorage: "Αποθήκευση", statMode: "Λειτουργία", autoValue: "10 δευτ.", localValue: "τοπικά", modeValue: "6 ήπειροι",
    nextLaunchPrefix: "Επόμενη εκτόξευση σε", nextLaunchSuffix: "δευτ.", launchNow: "ΕΚΤΟΞΕΥΣΗ ΤΩΡΑ", pause: "Παύση", resume: "Συνέχεια", reset: "Μηδενισμός τοπικού μετρητή",
    statsLabel: "Εκτοξεύσεις ανά ήπειρο", maxCarbonationTitle: "Κινητήρας ανθράκωσης", gameModeLabel: "Λειτουργία παιχνιδιού:",
    maxCarbonationCopy: "ο λαιμός κοιτάζει πίσω, το καπάκι ξεβιδώνει και οι φυσαλίδες αντικαθιστούν τη φωτιά. Για το πραγματικό ποτό, το KVASSISTENT στοχεύει σε μη αλκοολούχο κβας έως 0,5%· μόνο μέτρηση επιβεβαιώνει την ακριβή τιμή.",
    sphereTitle: "Όλη η σφαίρα είναι πατήσιμη", sphereCopy: "Κάθε πάτημα επιλέγει την κοντινότερη από έξι ηπείρους. Ρολά χαρτιού υγείας ανοίγουν στα πλάγια ως φτερά.",
    tapHint: "Πάτησε τη σφαίρα, ένα σημείο ή Enter.", globeAria: "Εκτόξευση μπουκαλιού από την κοντινότερη ήπειρο",
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
