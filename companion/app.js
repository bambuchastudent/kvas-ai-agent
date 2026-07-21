import { addCheckin, agentHandoff, assessBatch, decisionTrace, latestCheckin, makeBatch } from "./engine.js";
import { normalizeConsent, resolvePreferredLanguage } from "./preferences.js";

const STORAGE_KEY = "kvassistent-live-batch-v1";
const LANGUAGE_KEY = "kvassistent-language";
const CONSENT_KEY = "kvassistent-consent-v1";

const strings = {
  ru: {
    featureName:"Живая партия",language:"Язык",privacyPill:"Без аккаунта · данные остаются на устройстве",kicker:"Твой квас. Один честный check-in за раз.",headline:"Узнай, что делать с банкой <em>прямо сейчас.</em>",lead:"Температура, запах и поверхность превращаются в следующий безопасный шаг — без догадок и облачной слежки.",startTitle:"Заведи живую партию",demoButton:"Загрузить демо 28°C ↗",batchName:"Название",volume:"Объём, л",sugar:"Добавленный сахар, г",startedAt:"Начало брожения",temperature:"Температура жидкости, °C",closure:"Чем закрыта банка",sealCloth:"Ткань / марля",sealLoose:"Неплотная крышка",sealTight:"Плотная крышка",sunlight:"Банка стоит на прямом солнце",startButton:"Начать сопровождение",liveBatch:"Живая партия",elapsed:"Прошло",temperatureShort:"Жидкость",nextCheck:"Следующая проверка",localTime:"по местному времени",journeyTitle:"Путь партии",phaseFerment:"Брожение",phaseTaste:"Проба",phaseFinish:"Холод",checkinTitle:"Что видно сейчас?",surface:"Поверхность",surfaceClear:"Чистая",surfaceFoam:"Обычная пена",surfaceMold:"Плесень / пушок",surfaceSlime:"Слизь / нити",smell:"Запах",smellBread:"Хлебный",smellSour:"Приятно кислый",smellAlcohol:"Спиртовой",smellRotten:"Гнилой",smellChemical:"Химический",taste:"Вкус",tasteUnknown:"Не пробовал(а)",tasteSweet:"Сладкий",tasteBalanced:"Сбалансированный",tasteSour:"Кислый",notes:"Заметка",notesPlaceholder:"Например: пузырьки стали активнее",saveCheckin:"Сохранить check-in",history:"История",shareAI:"Поделиться с ИИ ↗",briefTitle:"Почему такой совет?",briefIntro:"Короткая трассировка решения: что увидел помощник и чего он не знает.",briefToggleOpen:"Раскрыть объяснение",briefToggleClose:"Скрыть объяснение",briefSignalTemperature:"Температура",briefSignalSurface:"Поверхность",briefSignalSmell:"Запах",briefSignalClosure:"Крышка",briefSignalSunlight:"Солнце",briefSignalTiming:"Время",briefStatusGood:"спокойно",briefStatusWatch:"внимание",briefStatusDanger:"действуй",briefStatusStop:"стоп",briefUnknowns:"Что остаётся неизвестным",briefUnknownCopy:"Это бытовая оценка, не лабораторный диагноз.",briefShare:"Скопировать AI safety brief ↗",briefCopied:"Safety brief скопирован для ИИ",briefYes:"да",briefNo:"нет",unknown_microbiological_safety:"микробиологическая безопасность",localTitle:"Только твоя кухня",localCopy:"Состояние хранится в этом браузере. Экспортируй JSON, если хочешь сохранить или передать его ИИ-агенту.",reset:"Удалить эту партию",footer:"Бытовой помощник, не лаборатория",checkins:n=>`${n} check-in`,hours:n=>`${Math.round(n)} ч`,phase_ferment:"Основное брожение",phase_taste:"Время наблюдать и пробовать",phase_finish:"Завершить или охладить",verdict_on_track:"Всё идёт спокойно",verdict_watch:"Наблюдай внимательнее",verdict_act_now:"Действуй сейчас",verdict_ready:"Можно завершать",verdict_stop:"Партию безопаснее выбросить",action_continue:"Оставь в тени под тканью или неплотной крышкой. Вернись к следующей проверке.",action_discard:"Не пробуй и не пытайся спасти партию. Утилизируй содержимое и вымой ёмкость.",action_release_pressure:"Плотная крышка при брожении создаёт давление. Не направляй ёмкость на лицо; осторожно сними давление и используй ткань или неплотную крышку.",action_move_and_cool:"Убери банку с солнца и переставь в прохладу. Измерь жидкость снова примерно через час.",action_strain_and_chill:"Запах, поверхность и вкус выглядят нормально. Процеди и охлади; при розливе учитывай давление.",action_shade_check_soon:"Держи только в тени и проверь снова через 4 часа — при этой температуре всё идёт быстрее.",action_check_soon:"Брожение ускорено. Проверь запах, поверхность и вкус через 6 часов.",action_warm_gently:"Процесс идёт медленно. Переставь в более тёплое место без прямого солнца.",action_taste_and_assess:"Пора проверить вкус, запах и поверхность. Если вкус уже сбалансирован — процеди и охлади.",issue_direct_sunlight:"прямое солнце",issue_temperature_fast:"быстрый режим",issue_temperature_hot:"перегрев",issue_temperature_stop:"35°C или выше",issue_temperature_slow:"слишком холодно",issue_tight_seal:"герметичная крышка",issue_extended_warm:"слишком долго в тепле",issue_warm_too_long:"долго в тепле",issue_surface_mold:"плесень",issue_surface_slime:"слизь",issue_smell_rotten:"гнилой запах",issue_smell_chemical:"химический запах",noIssues:"опасных признаков нет",now:"сейчас",done:"готово",saved:"Check-in сохранён",copied:"Состояние скопировано для ИИ",exported:"JSON экспортирован",confirmReset:"Удалить партию и всю локальную историю?",historyLine:(surface,smell)=>`${surface} · ${smell}`,journey:(phase,progress)=>`${phase} · ориентировочно ${progress}% пути`,temp_normal:"спокойный режим",temp_fast:"проверяй чаще",temp_hot:"нужно охладить",temp_slow:"идёт медленно",demoName:"Демо: банка на солнце"
  },
  en: {
    featureName:"Live batch",language:"Language",privacyPill:"No account · data stays on this device",kicker:"Your kvass. One honest check-in at a time.",headline:"Know what your jar needs <em>right now.</em>",lead:"Temperature, smell, and surface become one clear safety-first action — without guesswork or cloud tracking.",startTitle:"Start a live batch",demoButton:"Load the 28°C demo ↗",batchName:"Batch name",volume:"Volume, L",sugar:"Added sugar, g",startedAt:"Fermentation started",temperature:"Liquid temperature, °C",closure:"Jar closure",sealCloth:"Cloth / gauze",sealLoose:"Loose lid",sealTight:"Tight lid",sunlight:"The jar is in direct sunlight",startButton:"Start guidance",liveBatch:"Live batch",elapsed:"Elapsed",temperatureShort:"Liquid",nextCheck:"Next check",localTime:"local time",journeyTitle:"Batch journey",phaseFerment:"Ferment",phaseTaste:"Taste",phaseFinish:"Chill",checkinTitle:"What do you see now?",surface:"Surface",surfaceClear:"Clear",surfaceFoam:"Normal foam",surfaceMold:"Mold / fuzz",surfaceSlime:"Slime / strings",smell:"Smell",smellBread:"Bready",smellSour:"Pleasantly sour",smellAlcohol:"Alcohol-like",smellRotten:"Rotten",smellChemical:"Chemical",taste:"Taste",tasteUnknown:"Not tasted",tasteSweet:"Sweet",tasteBalanced:"Balanced",tasteSour:"Sour",notes:"Note",notesPlaceholder:"For example: bubbles are more active",saveCheckin:"Save check-in",history:"History",shareAI:"Share with AI ↗",briefTitle:"Why this advice?",briefIntro:"A short decision trace: what the companion saw and what it cannot know.",briefToggleOpen:"Show explanation",briefToggleClose:"Hide explanation",briefSignalTemperature:"Temperature",briefSignalSurface:"Surface",briefSignalSmell:"Smell",briefSignalClosure:"Closure",briefSignalSunlight:"Sunlight",briefSignalTiming:"Timing",briefStatusGood:"calm",briefStatusWatch:"watch",briefStatusDanger:"act",briefStatusStop:"stop",briefUnknowns:"What remains unknown",briefUnknownCopy:"This is household guidance, not a laboratory diagnosis.",briefShare:"Copy AI safety brief ↗",briefCopied:"Safety brief copied for AI",briefYes:"yes",briefNo:"no",unknown_microbiological_safety:"microbiological safety",localTitle:"Your kitchen only",localCopy:"The batch stays in this browser. Export JSON to keep it or hand it to an AI agent.",reset:"Delete this batch",footer:"A household guide, not a laboratory",checkins:n=>`${n} check-in${n===1?"":"s"}`,hours:n=>`${Math.round(n)} h`,phase_ferment:"Primary fermentation",phase_taste:"Observe and taste",phase_finish:"Finish or chill",verdict_on_track:"Everything looks on track",verdict_watch:"Watch this batch closely",verdict_act_now:"Act now",verdict_ready:"Ready to finish",verdict_stop:"Discarding is the safer choice",action_continue:"Keep it shaded under cloth or a loose lid. Return for the next check.",action_discard:"Do not taste or try to rescue it. Discard the contents and wash the container.",action_release_pressure:"A tight lid can build pressure during fermentation. Keep it away from your face, release pressure carefully, then use cloth or a loose lid.",action_move_and_cool:"Move the jar out of sunlight and into a cooler place. Measure the liquid again in about one hour.",action_strain_and_chill:"Smell, surface, and taste look normal. Strain and chill; manage pressure carefully if bottling.",action_shade_check_soon:"Keep it in shade and check again in 4 hours — fermentation moves faster at this temperature.",action_check_soon:"Fermentation is accelerated. Recheck smell, surface, and taste in 6 hours.",action_warm_gently:"The process is slow. Move it somewhere gently warmer, away from direct sun.",action_taste_and_assess:"It is time to check taste, smell, and surface. If balanced, strain and chill.",issue_direct_sunlight:"direct sunlight",issue_temperature_fast:"fast temperature",issue_temperature_hot:"overheating",issue_temperature_stop:"35°C or above",issue_temperature_slow:"too cold",issue_tight_seal:"tight lid",issue_extended_warm:"too long while warm",issue_warm_too_long:"long warm ferment",issue_surface_mold:"mold",issue_surface_slime:"slime",issue_smell_rotten:"rotten smell",issue_smell_chemical:"chemical smell",noIssues:"no danger signs",now:"now",done:"done",saved:"Check-in saved",copied:"AI handoff copied",exported:"JSON exported",confirmReset:"Delete this batch and its local history?",historyLine:(surface,smell)=>`${surface} · ${smell}`,journey:(phase,progress)=>`${phase} · about ${progress}% through`,temp_normal:"calm range",temp_fast:"check more often",temp_hot:"cool it down",temp_slow:"moving slowly",demoName:"Demo: jar in the sun"
  }
};

const baseFallback = {
  es:{featureName:"Lote vivo",privacyPill:"Sin cuenta · los datos quedan en tu dispositivo",kicker:"Tu kvas. Un control honesto cada vez.",headline:"Sabe qué necesita tu frasco <em>ahora mismo.</em>",lead:"Temperatura, olor y superficie se convierten en una acción clara y segura.",startTitle:"Inicia un lote vivo",demoButton:"Cargar demo de 28°C ↗",startButton:"Empezar acompañamiento",liveBatch:"Lote vivo",checkinTitle:"¿Qué ves ahora?",history:"Historial",shareAI:"Compartir con IA ↗",briefTitle:"¿Por qué este consejo?",briefIntro:"Una breve traza: qué vio el asistente y qué no puede saber.",briefToggleOpen:"Ver explicación",briefToggleClose:"Ocultar explicación",briefUnknowns:"Lo que sigue sin saberse",briefUnknownCopy:"Es una guía doméstica, no un diagnóstico de laboratorio.",briefShare:"Copiar resumen de seguridad IA ↗",briefCopied:"Resumen copiado para la IA",localTitle:"Solo tu cocina",reset:"Eliminar este lote",footer:"Ayuda doméstica, no laboratorio"},
  de:{featureName:"Lebendige Charge",privacyPill:"Kein Konto · Daten bleiben auf diesem Gerät",kicker:"Dein Kwas. Ein ehrlicher Check-in nach dem anderen.",headline:"Wisse, was dein Glas <em>jetzt</em> braucht.",lead:"Temperatur, Geruch und Oberfläche werden zu einem klaren, sicheren Schritt.",startTitle:"Charge starten",demoButton:"28°C-Demo laden ↗",startButton:"Begleitung starten",liveBatch:"Lebendige Charge",checkinTitle:"Was siehst du jetzt?",history:"Verlauf",shareAI:"Mit KI teilen ↗",briefTitle:"Warum dieser Rat?",briefIntro:"Eine kurze Spur: Was die Begleitung gesehen hat und nicht wissen kann.",briefToggleOpen:"Erklärung zeigen",briefToggleClose:"Erklärung ausblenden",briefUnknowns:"Was unbekannt bleibt",briefUnknownCopy:"Dies ist eine Haushaltshilfe, keine Labordiagnose.",briefShare:"KI-Sicherheitsbrief kopieren ↗",briefCopied:"Sicherheitsbrief für KI kopiert",localTitle:"Nur deine Küche",reset:"Charge löschen",footer:"Haushaltshilfe, kein Labor"},
  "zh-CN":{featureName:"实时批次",privacyPill:"无需账户 · 数据保留在本设备",kicker:"你的格瓦斯。每次一次诚实检查。",headline:"马上知道罐子<em>现在需要什么。</em>",lead:"温度、气味和表面状态会变成清晰、安全的下一步。",startTitle:"开始实时批次",demoButton:"加载 28°C 演示 ↗",startButton:"开始指导",liveBatch:"实时批次",checkinTitle:"现在看到了什么？",history:"历史",shareAI:"分享给 AI ↗",briefTitle:"为什么这样建议？",briefIntro:"简短的判断轨迹：助手看到了什么，以及它不知道什么。",briefToggleOpen:"展开解释",briefToggleClose:"收起解释",briefUnknowns:"仍然未知的部分",briefUnknownCopy:"这是家庭指导，不是实验室诊断。",briefShare:"复制 AI 安全摘要 ↗",briefCopied:"已复制给 AI",localTitle:"只属于你的厨房",reset:"删除此批次",footer:"家庭助手，不是实验室"},
  el:{featureName:"Ζωντανή παρτίδα",language:"Γλώσσα",privacyPill:"Χωρίς λογαριασμό · τα δεδομένα μένουν στη συσκευή",kicker:"Το κβας σου. Ένας ειλικρινής έλεγχος κάθε φορά.",headline:"Μάθε τι χρειάζεται το βάζο σου <em>αυτή τη στιγμή.</em>",lead:"Η θερμοκρασία, η μυρωδιά και η επιφάνεια γίνονται ένα σαφές και ασφαλές επόμενο βήμα.",startTitle:"Ξεκίνα ζωντανή παρτίδα",demoButton:"Φόρτωση demo 28°C ↗",batchName:"Όνομα παρτίδας",volume:"Όγκος, L",sugar:"Πρόσθετη ζάχαρη, g",startedAt:"Έναρξη ζύμωσης",temperature:"Θερμοκρασία υγρού, °C",closure:"Κλείσιμο βάζου",sealCloth:"Ύφασμα / γάζα",sealLoose:"Χαλαρό καπάκι",sealTight:"Σφιχτό καπάκι",sunlight:"Το βάζο είναι σε άμεσο ήλιο",startButton:"Έναρξη καθοδήγησης",liveBatch:"Ζωντανή παρτίδα",elapsed:"Χρόνος",temperatureShort:"Υγρό",nextCheck:"Επόμενος έλεγχος",localTime:"τοπική ώρα",journeyTitle:"Πορεία παρτίδας",phaseFerment:"Ζύμωση",phaseTaste:"Δοκιμή",phaseFinish:"Ψύξη",checkinTitle:"Τι βλέπεις τώρα;",surface:"Επιφάνεια",surfaceClear:"Καθαρή",surfaceFoam:"Κανονικός αφρός",surfaceMold:"Μούχλα / χνούδι",surfaceSlime:"Γλίτσα / ίνες",smell:"Μυρωδιά",smellBread:"Ψωμιού",smellSour:"Ευχάριστα ξινή",smellAlcohol:"Αλκοολική",smellRotten:"Σάπια",smellChemical:"Χημική",taste:"Γεύση",tasteUnknown:"Δεν δοκιμάστηκε",tasteSweet:"Γλυκιά",tasteBalanced:"Ισορροπημένη",tasteSour:"Ξινή",notes:"Σημείωση",notesPlaceholder:"Π.χ. οι φυσαλίδες έγιναν πιο έντονες",saveCheckin:"Αποθήκευση ελέγχου",history:"Ιστορικό",shareAI:"Κοινοποίηση σε AI ↗",briefTitle:"Γιατί αυτή η συμβουλή;",briefIntro:"Τι είδε ο βοηθός και τι δεν μπορεί να γνωρίζει.",briefToggleOpen:"Προβολή εξήγησης",briefToggleClose:"Απόκρυψη εξήγησης",briefUnknowns:"Τι παραμένει άγνωστο",briefUnknownCopy:"Οικιακή καθοδήγηση, όχι εργαστηριακή διάγνωση.",briefShare:"Αντιγραφή σύνοψης ασφαλείας AI ↗",briefCopied:"Η σύνοψη αντιγράφηκε",briefYes:"ναι",briefNo:"όχι",localTitle:"Μόνο η κουζίνα σου",localCopy:"Η παρτίδα μένει σε αυτό το πρόγραμμα περιήγησης. Εξήγαγε JSON για αποθήκευση ή παράδοση σε AI.",reset:"Διαγραφή παρτίδας",footer:"Οικιακός οδηγός, όχι εργαστήριο",verdict_on_track:"Όλα φαίνονται σωστά",verdict_watch:"Παρακολούθησε προσεκτικά",verdict_act_now:"Ενέργησε τώρα",verdict_ready:"Έτοιμο για ολοκλήρωση",verdict_stop:"Ασφαλέστερα να απορριφθεί",action_continue:"Κράτησέ το στη σκιά με ύφασμα ή χαλαρό καπάκι και έλεγξέ το ξανά.",action_discard:"Μην το δοκιμάσεις και μην επιχειρήσεις διάσωση. Απόρριψε το περιεχόμενο και πλύνε το δοχείο.",action_release_pressure:"Το σφιχτό καπάκι δημιουργεί πίεση. Μακριά από το πρόσωπο, εκτόνωσε προσεκτικά και βάλε ύφασμα ή χαλαρό καπάκι.",action_move_and_cool:"Βγάλε το βάζο από τον ήλιο, βάλε το σε δροσερό μέρος και μέτρησε ξανά σε μία ώρα.",action_strain_and_chill:"Η μυρωδιά, η επιφάνεια και η γεύση φαίνονται φυσιολογικές. Σούρωσε και ψύξε.",action_shade_check_soon:"Μόνο στη σκιά και νέος έλεγχος σε 4 ώρες.",action_check_soon:"Η ζύμωση είναι γρήγορη. Έλεγξε ξανά σε 6 ώρες.",action_warm_gently:"Η διαδικασία είναι αργή. Μετέφερε σε λίγο θερμότερο μέρος, χωρίς άμεσο ήλιο.",action_taste_and_assess:"Έλεγξε γεύση, μυρωδιά και επιφάνεια. Αν είναι ισορροπημένο, σούρωσε και ψύξε.",noIssues:"δεν υπάρχουν σημάδια κινδύνου",now:"τώρα",done:"έτοιμο",saved:"Ο έλεγχος αποθηκεύτηκε",copied:"Η κατάσταση αντιγράφηκε για AI",exported:"Το JSON εξήχθη",confirmReset:"Διαγραφή παρτίδας και τοπικού ιστορικού;",demoName:"Demo: βάζο στον ήλιο"}
};
for (const [lang, partial] of Object.entries(baseFallback)) strings[lang] = { ...strings.en, ...partial };

const recipeStrings = {
  ru: {
    recipeKicker:"Первая партия · 3 литра",recipeTitle:"Простой квас без догадок",recipeTime:"около суток + охлаждение",recipeIngredients:"Что нужно",recipeBread:"180–220 г сухарей, лучше часть ржаных",recipeSugar:"100–120 г сахара или панелы",recipeStarter:"2–3 г свежих или 0,5–1 г сухих дрожжей",recipeStep1:"Поджарь сухари до тёмно-золотистого цвета, не сжигай.",recipeStep2:"Залей 3 л кипятка и оставь под неплотной крышкой на 4–8 часов.",recipeStep3:"Процеди: в брожение должна идти жидкость, а не хлебная каша.",recipeStep4:"Добавь сахар и остуди настой до 25–35°C.",recipeStep5:"Добавь дрожжи, накрой тканью или неплотной крышкой и запусти партию ниже.",recipeStep6:"Проверь через 8–12 часов; в жаре — уже через 6 часов.",recipeStep7:"Когда вкус и запах нравятся, процеди ещё раз и охлади минимум на ночь.",recipeSafety:"Плесень, слизь или гнилой/химический запах — не пробуй, партию лучше вылить.",unknown_microbiological_safety:"микробиологическая безопасность",unknown_starter_activity:"активность закваски",
  },
  en: {
    recipeKicker:"First batch · 3 litres",recipeTitle:"Straightforward kvass",recipeTime:"about a day + chilling",recipeIngredients:"What you need",recipeBread:"180–220 g dry crackers; rye is ideal for some of them",recipeSugar:"100–120 g sugar or panela",recipeStarter:"2–3 g fresh or 0.5–1 g dry yeast",recipeStep1:"Toast the crackers dark golden; do not burn them.",recipeStep2:"Pour over 3 L of boiling water and leave under a loose lid for 4–8 hours.",recipeStep3:"Strain it: ferment the liquid, not bread porridge.",recipeStep4:"Add sugar and cool the infusion to 25–35°C.",recipeStep5:"Add yeast, cover with cloth or a loose lid, then start the batch below.",recipeStep6:"Check after 8–12 hours; in heat, start checking after 6 hours.",recipeStep7:"When the taste and smell are right, strain once more and chill overnight.",recipeSafety:"Mold, slime, or a rotten/chemical smell: do not taste it; discard the batch.",unknown_microbiological_safety:"microbiological safety",unknown_starter_activity:"starter activity",
  },
  es: {
    recipeKicker:"Primer lote · 3 litros",recipeTitle:"Kvas sencillo, sin adivinar",recipeTime:"un día aprox. + frío",recipeIngredients:"Qué necesitas",recipeBread:"180–220 g de pan seco; una parte de centeno es ideal",recipeSugar:"100–120 g de azúcar o panela",recipeStarter:"2–3 g de levadura fresca o 0,5–1 g seca",recipeStep1:"Tuesta el pan hasta dorado oscuro, sin quemarlo.",recipeStep2:"Cúbrelo con 3 L de agua hirviendo y déjalo con tapa floja 4–8 horas.",recipeStep3:"Cuela: fermenta el líquido, no una papilla de pan.",recipeStep4:"Añade azúcar y enfría la infusión a 25–35°C.",recipeStep5:"Añade la levadura, cubre con tela o tapa floja e inicia el lote abajo.",recipeStep6:"Revisa tras 8–12 horas; con calor, desde las 6 horas.",recipeStep7:"Cuando el olor y sabor estén bien, cuela otra vez y enfría toda la noche.",recipeSafety:"Moho, baba u olor podrido/químico: no lo pruebes; desecha el lote.",unknown_microbiological_safety:"seguridad microbiológica",unknown_starter_activity:"actividad del cultivo",
  },
  de: {
    recipeKicker:"Erste Charge · 3 Liter",recipeTitle:"Einfacher Kwas ohne Raten",recipeTime:"etwa ein Tag + Kühlen",recipeIngredients:"Was du brauchst",recipeBread:"180–220 g trockene Brotstücke, teils Roggen",recipeSugar:"100–120 g Zucker oder Panela",recipeStarter:"2–3 g frische oder 0,5–1 g Trockenhefe",recipeStep1:"Brot dunkelgolden rösten, aber nicht verbrennen.",recipeStep2:"Mit 3 l kochendem Wasser übergießen und 4–8 Stunden locker abgedeckt stehen lassen.",recipeStep3:"Abseihen: Die Flüssigkeit fermentieren, nicht den Brotbrei.",recipeStep4:"Zucker zugeben und den Aufguss auf 25–35°C abkühlen.",recipeStep5:"Hefe zugeben, mit Tuch oder losem Deckel abdecken und unten die Charge starten.",recipeStep6:"Nach 8–12 Stunden prüfen; bei Hitze schon nach 6 Stunden.",recipeStep7:"Wenn Geruch und Geschmack stimmen, noch einmal abseihen und über Nacht kühlen.",recipeSafety:"Schimmel, Schleim oder faulig/chemischer Geruch: nicht probieren, Charge entsorgen.",unknown_microbiological_safety:"mikrobiologische Sicherheit",unknown_starter_activity:"Aktivität des Starters",
  },
  "zh-CN": {
    recipeKicker:"第一批 · 3 升",recipeTitle:"简单、不靠猜的格瓦斯",recipeTime:"约一天 + 冷藏",recipeIngredients:"需要什么",recipeBread:"180–220 克干面包块，最好有一部分黑麦",recipeSugar:"100–120 克糖或红糖块",recipeStarter:"2–3 克鲜酵母或 0.5–1 克干酵母",recipeStep1:"把面包烤至深金色，不要烤焦。",recipeStep2:"倒入 3 升开水，松盖静置 4–8 小时。",recipeStep3:"过滤：发酵液体，而不是面包糊。",recipeStep4:"加入糖，将浸液冷却到 25–35°C。",recipeStep5:"加入酵母，用布或松盖盖住，然后在下方开始记录批次。",recipeStep6:"8–12 小时后检查；天气热时 6 小时后就开始检查。",recipeStep7:"味道和气味合适后，再过滤一次并冷藏过夜。",recipeSafety:"出现霉菌、黏液或腐败/化学气味：不要尝，丢弃这批。",unknown_microbiological_safety:"微生物安全性",unknown_starter_activity:"发酵种活性",
  },
  el: {
    recipeKicker:"Πρώτη παρτίδα · 3 λίτρα",recipeTitle:"Απλό κβας χωρίς μαντεψιές",recipeTime:"περίπου μία μέρα + ψύξη",recipeIngredients:"Τι χρειάζεσαι",recipeBread:"180–220 g ξερό ψωμί, ιδανικά λίγο σίκαλης",recipeSugar:"100–120 g ζάχαρη ή panela",recipeStarter:"2–3 g φρέσκια ή 0,5–1 g ξηρή μαγιά",recipeStep1:"Φρύξε το ψωμί μέχρι σκούρο χρυσαφί, χωρίς να καεί.",recipeStep2:"Ρίξε 3 L βραστό νερό και άφησέ το 4–8 ώρες με χαλαρό καπάκι.",recipeStep3:"Σούρωσε: ζυμώνουμε το υγρό, όχι τον πολτό ψωμιού.",recipeStep4:"Πρόσθεσε ζάχαρη και κρύωσε το έγχυμα στους 25–35°C.",recipeStep5:"Πρόσθεσε μαγιά, κάλυψε με ύφασμα ή χαλαρό καπάκι και ξεκίνα την παρτίδα.",recipeStep6:"Έλεγξε σε 8–12 ώρες· με ζέστη από τις 6 ώρες.",recipeStep7:"Όταν γεύση και μυρωδιά είναι σωστές, σούρωσε ξανά και ψύξε όλη νύχτα.",recipeSafety:"Μούχλα, γλίτσα ή σάπια/χημική μυρωδιά: μην το δοκιμάσεις, απόρριψε την παρτίδα.",unknown_microbiological_safety:"μικροβιολογική ασφάλεια",unknown_starter_activity:"δραστηριότητα μαγιάς",
  },
};
for (const [lang, additions] of Object.entries(recipeStrings)) strings[lang] = { ...strings[lang], ...additions };

const privacyStrings = {
  ru:{consentKicker:"Твоя кухня — твои данные",consentTitle:"Печенье — к квасу. Cookies — только по делу.",consentCopy:"КВАССИСТЕНТ хранит на устройстве выбранный язык, согласие и состояние партии. PWA также сохраняет файлы для работы без сети. Рекламных и аналитических cookies сейчас нет.",consentDetail:"Полное согласие разрешает необязательные улучшения в будущем. Частичное — оставляет только данные, необходимые для языка, партии и офлайн-режима.",consentEssential:"Согласен, но не полностью",consentAll:"Согласен",consentCheers:"Хрум! И глоток кваса за приватность."},
  en:{consentKicker:"Your kitchen, your data",consentTitle:"Cookies with kvass — only when useful.",consentCopy:"KVASSISTENT stores your language, consent, and batch state on this device. The PWA also caches files for offline use. There are currently no advertising or analytics cookies.",consentDetail:"Full consent allows optional improvements in the future. Partial consent keeps only data needed for language, batch state, and offline mode.",consentEssential:"Agree, essential only",consentAll:"Agree",consentCheers:"Crunch! And a sip of kvass for privacy."},
  es:{consentKicker:"Tu cocina, tus datos",consentTitle:"Cookies con kvas, solo cuando sirven.",consentCopy:"KVASSISTENT guarda en este dispositivo el idioma, el consentimiento y el estado del lote. La PWA también almacena archivos para funcionar sin conexión. Ahora no hay cookies publicitarias ni analíticas.",consentDetail:"El consentimiento completo permite mejoras opcionales futuras. El parcial conserva solo lo necesario para idioma, lote y modo sin conexión.",consentEssential:"Aceptar solo lo esencial",consentAll:"Aceptar",consentCheers:"¡Crac! Y un trago de kvas por la privacidad."},
  de:{consentKicker:"Deine Küche, deine Daten",consentTitle:"Cookies zum Kwas — nur wenn sie nützen.",consentCopy:"KVASSISTENT speichert Sprache, Einwilligung und Chargenstatus auf diesem Gerät. Die PWA speichert außerdem Dateien für den Offlinebetrieb. Werbe- oder Analyse-Cookies gibt es derzeit nicht.",consentDetail:"Volle Zustimmung erlaubt künftig optionale Verbesserungen. Teilweise Zustimmung lässt nur Sprache, Charge und Offlinebetrieb zu.",consentEssential:"Nur notwendige akzeptieren",consentAll:"Akzeptieren",consentCheers:"Knusper! Und ein Schluck Kwas für den Datenschutz."},
  "zh-CN":{consentKicker:"你的厨房，你的数据",consentTitle:"饼干配格瓦斯，Cookie 只做必要的事。",consentCopy:"KVASSISTENT 会在本设备保存语言、同意选项和批次状态。PWA 还会缓存离线文件。目前没有广告或分析 Cookie。",consentDetail:"完全同意允许未来的可选改进；部分同意仅保留语言、批次和离线模式所需数据。",consentEssential:"仅同意必要项",consentAll:"同意",consentCheers:"咔嚓！为隐私喝一口格瓦斯。"},
  el:{consentKicker:"Η κουζίνα σου, τα δεδομένα σου",consentTitle:"Μπισκότο με κβας — cookies μόνο όταν χρειάζονται.",consentCopy:"Το KVASSISTENT αποθηκεύει στη συσκευή τη γλώσσα, τη συγκατάθεση και την κατάσταση παρτίδας. Η PWA αποθηκεύει επίσης αρχεία για λειτουργία εκτός σύνδεσης. Δεν υπάρχουν διαφημιστικά ή αναλυτικά cookies.",consentDetail:"Η πλήρης συγκατάθεση επιτρέπει μελλοντικές προαιρετικές βελτιώσεις. Η μερική κρατά μόνο όσα χρειάζονται για γλώσσα, παρτίδα και offline λειτουργία.",consentEssential:"Συμφωνώ μόνο στα απαραίτητα",consentAll:"Συμφωνώ",consentCheers:"Κρατς! Και μια γουλιά κβας για την ιδιωτικότητα."}
};
for (const [lang, additions] of Object.entries(privacyStrings)) strings[lang] = { ...strings[lang], ...additions };

const discoveryStrings = {
  ru:{nearbyTitle:"Найти квас рядом",nearbyCopy:"Откроем поиск ближайших кафе в картах — только после твоего нажатия.",feedbackLink:"Рассказать о своём напитке"},
  en:{nearbyTitle:"Find kvass nearby",nearbyCopy:"Open a nearby café search in maps — only after you tap.",feedbackLink:"Share your drink"},
  es:{nearbyTitle:"Encontrar kvas cerca",nearbyCopy:"Abrir cafeterías cercanas en el mapa, solo cuando pulses.",feedbackLink:"Comparte tu bebida"},
  de:{nearbyTitle:"Kwas in der Nähe finden",nearbyCopy:"Cafés in der Nähe erst nach deinem Klick in Karten suchen.",feedbackLink:"Dein Getränk teilen"},
  "zh-CN":{nearbyTitle:"查找附近的格瓦斯",nearbyCopy:"仅在你点击后，才会在地图中搜索附近咖啡馆。",feedbackLink:"分享你的饮品"},
  el:{nearbyTitle:"Βρες κβας κοντά σου",nearbyCopy:"Άνοιξε αναζήτηση κοντινών καφέ στον χάρτη — μόνο αφού πατήσεις.",feedbackLink:"Μοιράσου το ποτό σου"}
};
for (const [lang, additions] of Object.entries(discoveryStrings)) strings[lang] = { ...strings[lang], ...additions };
const nearbyQueries = {ru:"квас кафе",en:"kvass cafe",es:"kvas cafetería",de:"Kwas Café","zh-CN":"格瓦斯 咖啡馆",el:"κβας καφέ"};
Object.assign(strings.el, {
  checkins:n=>`${n} έλεγχ${n===1?"ος":"οι"}`,hours:n=>`${Math.round(n)} ώρ.`,
  phase_ferment:"Κύρια ζύμωση",phase_taste:"Παρατήρηση και δοκιμή",phase_finish:"Ολοκλήρωση ή ψύξη",
  briefSignalTemperature:"Θερμοκρασία",briefSignalSurface:"Επιφάνεια",briefSignalSmell:"Μυρωδιά",briefSignalClosure:"Καπάκι",briefSignalSunlight:"Ήλιος",briefSignalTiming:"Χρόνος",
  briefStatusGood:"ήρεμα",briefStatusWatch:"προσοχή",briefStatusDanger:"ενέργεια",briefStatusStop:"στοπ",
  unknown_microbiological_safety:"μικροβιολογική ασφάλεια",unknown_starter_activity:"δραστηριότητα μαγιάς",
  issue_direct_sunlight:"άμεσος ήλιος",issue_temperature_fast:"γρήγορη ζύμωση",issue_temperature_hot:"υπερθέρμανση",issue_temperature_stop:"35°C ή περισσότερο",issue_temperature_slow:"πολύ κρύο",issue_tight_seal:"σφιχτό καπάκι",issue_extended_warm:"πολλές ώρες σε ζέστη",issue_warm_too_long:"παρατεταμένη θερμή ζύμωση",issue_surface_mold:"μούχλα",issue_surface_slime:"γλίτσα",issue_smell_rotten:"σάπια μυρωδιά",issue_smell_chemical:"χημική μυρωδιά",
  historyLine:(surface,smell)=>`${surface} · ${smell}`,journey:(phase,progress)=>`${phase} · περίπου ${progress}%`,
  temp_normal:"ήρεμο εύρος",temp_fast:"συχνοί έλεγχοι",temp_hot:"χρειάζεται ψύξη",temp_slow:"αργή πορεία"
});

let language = resolvePreferredLanguage(localStorage.getItem(LANGUAGE_KEY), navigator.languages ?? [navigator.language]);
let batch = loadBatch();

const $ = selector => document.querySelector(selector);
const setupPanel = $("#setup-panel");
const dashboard = $("#dashboard");
const languageSelect = $("#language");
const consentCard = $("#consent-card");
const cookieToast = $("#cookie-toast");

function t(key, ...args) {
  const value = strings[language][key] ?? strings.en[key] ?? key;
  return typeof value === "function" ? value(...args) : value;
}

function translatePage() {
  document.documentElement.lang = language;
  languageSelect.value = language;
  languageSelect.setAttribute("aria-label", t("language"));
  $("#nearby-kvass").href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(nearbyQueries[language])}`;
  document.querySelectorAll("[data-i18n]").forEach(node => {
    const value = t(node.dataset.i18n);
    if (node.dataset.i18n === "headline") node.innerHTML = value;
    else node.textContent = value;
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(node => node.placeholder = t(node.dataset.i18nPlaceholder));
  render();
}

function showConsentIfNeeded() {
  consentCard.classList.toggle("hidden", Boolean(normalizeConsent(localStorage.getItem(CONSENT_KEY))));
}

function acceptConsent(level) {
  localStorage.setItem(CONSENT_KEY, level);
  consentCard.classList.add("hidden");
  cookieToast.classList.remove("hidden", "celebrate");
  void cookieToast.offsetWidth;
  cookieToast.classList.add("celebrate");
  window.setTimeout(() => cookieToast.classList.add("hidden"), 3000);
}

function loadBatch() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY)); } catch { return null; }
}

function saveBatch() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(batch));
}

function localDateInput(date) {
  const shifted = new Date(date.getTime() - date.getTimezoneOffset() * 60_000);
  return shifted.toISOString().slice(0, 16);
}

function formatTime(iso) {
  return new Intl.DateTimeFormat(language, { hour:"2-digit", minute:"2-digit" }).format(new Date(iso));
}

function formatDateTime(iso) {
  return new Intl.DateTimeFormat(language, { day:"numeric", month:"short", hour:"2-digit", minute:"2-digit" }).format(new Date(iso));
}

function optionText(prefix, value) {
  const key = `${prefix}${value[0].toUpperCase()}${value.slice(1)}`;
  return t(key);
}

function temperatureNote(value) {
  return value >= 31 ? t("temp_hot") : value >= 25 ? t("temp_fast") : value < 18 ? t("temp_slow") : t("temp_normal");
}

function render() {
  if (!batch) {
    setupPanel.classList.remove("hidden"); dashboard.classList.add("hidden");
    return;
  }
  setupPanel.classList.add("hidden"); dashboard.classList.remove("hidden");
  const checkin = latestCheckin(batch);
  const now = new Date();
  const result = assessBatch(batch, now);
  const trace = decisionTrace(batch, now);
  $("#dashboard-name").textContent = batch.name;
  $("#verdict-card").className = `verdict-card ${result.level}`;
  $("#verdict-label").textContent = t(`verdict_${result.verdict}`);
  $("#verdict-action").textContent = t(`action_${result.action}`);
  $("#verdict-detail").textContent = result.issues.length ? result.issues.map(issue => t(`issue_${issue}`)).join(" · ") : t("noIssues");
  $("#issue-list").innerHTML = result.issues.map(issue => `<span class="issue-chip">${escapeHtml(t(`issue_${issue}`))}</span>`).join("");
  $("#last-updated").textContent = formatDateTime(checkin.at);
  $("#elapsed-value").textContent = t("hours", result.hours);
  $("#phase-value").textContent = t(`phase_${result.phase}`);
  $("#temperature-value").textContent = `${checkin.temperatureC}°C`;
  $("#temperature-note").textContent = temperatureNote(checkin.temperatureC);
  $("#next-check-value").textContent = result.nextCheckAt ? formatTime(result.nextCheckAt) : result.ready ? t("done") : t("now");
  $("#journey-copy").textContent = t("journey", t(`phase_${result.phase}`), result.progress);
  $("#progress-bar").style.width = `${result.progress}%`;
  $("#checkin-count").textContent = t("checkins", batch.checkins.length);
  $("#checkin-temperature").value = checkin.temperatureC;
  $("#checkin-surface").value = checkin.surface;
  $("#checkin-smell").value = checkin.smell;
  $("#checkin-taste").value = checkin.taste;
  $("#checkin-seal").value = checkin.seal;
  $("#checkin-sunlight").checked = checkin.sunlight;
  $("#history-list").innerHTML = [...batch.checkins].reverse().slice(0, 8).map(item => `
    <li><span class="history-time">${formatDateTime(item.at)}</span><span class="history-main"><strong>${escapeHtml(t("historyLine", optionText("surface",item.surface), optionText("smell",item.smell)))}</strong><small>${escapeHtml(item.notes || optionText("taste",item.taste))}</small></span><span class="history-temp">${item.temperatureC}°</span></li>`).join("");
  renderBrief(trace);
}

function briefStatus(status) {
  return t(`briefStatus${status[0].toUpperCase()}${status.slice(1)}`);
}

function briefSignalLabel(key) {
  return t(`briefSignal${key[0].toUpperCase()}${key.slice(1)}`);
}

function briefSignalValue(signal) {
  if (signal.key === "temperature") return `${signal.value}°C`;
  if (signal.key === "surface" || signal.key === "smell" || signal.key === "closure") return optionText(signal.key === "closure" ? "seal" : signal.key, signal.value);
  if (signal.key === "sunlight") return signal.value ? t("briefYes") : t("briefNo");
  return t("hours", signal.value);
}

function renderBrief(trace) {
  $("#brief-grid").innerHTML = trace.signals.map(signal => `
    <article class="brief-signal">
      <div class="brief-signal-top"><span>${escapeHtml(briefSignalLabel(signal.key))}</span><span class="brief-signal-status ${signal.status}">${escapeHtml(briefStatus(signal.status))}</span></div>
      <strong class="brief-signal-value">${escapeHtml(briefSignalValue(signal))}</strong>
    </article>`).join("");
  $("#brief-unknown-list").innerHTML = trace.unknowns.map(key => `<li>${escapeHtml(t(`unknown_${key}`))}</li>`).join("");
  const isOpen = $("#brief-toggle").dataset.open === "true";
  $("#brief-content").classList.toggle("hidden", !isOpen);
  $("#brief-toggle").setAttribute("aria-expanded", String(isOpen));
  $("#brief-toggle").textContent = t(isOpen ? "briefToggleClose" : "briefToggleOpen");
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[char]));
}

function showToast(message) {
  const toast = $("#toast"); toast.textContent = message; toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 2200);
}

function formObject(form) {
  const data = Object.fromEntries(new FormData(form));
  data.sunlight = new FormData(form).has("sunlight");
  return data;
}

$("#setup-form").addEventListener("submit", event => {
  event.preventDefault(); batch = makeBatch(formObject(event.currentTarget)); saveBatch(); render(); window.scrollTo({top:0,behavior:"smooth"});
});

$("#checkin-form").addEventListener("submit", event => {
  event.preventDefault(); batch = addCheckin(batch, formObject(event.currentTarget)); saveBatch(); event.currentTarget.elements.notes.value = ""; render(); showToast(t("saved"));
});

function loadDemo() {
  const started = new Date(Date.now() - 26 * 3_600_000);
  batch = makeBatch({name:t("demoName"),volumeL:3,sugarG:110,startedAt:started,temperatureC:28,sunlight:true,seal:"cloth",surface:"clear",smell:"sour",taste:"balanced"});
  saveBatch(); render(); window.scrollTo({top:0,behavior:"smooth"});
}

$("#demo-button").addEventListener("click", loadDemo);

$("#brief-toggle").addEventListener("click", () => {
  const button = $("#brief-toggle");
  const isOpen = button.dataset.open === "true";
  button.dataset.open = String(!isOpen);
  render();
});

async function shareHandoff() {
  const payload = `${batch.name}\n\n${JSON.stringify(agentHandoff(batch), null, 2)}`;
  if (navigator.share) {
    try { await navigator.share({title:batch.name,text:payload}); return; } catch (error) { if (error.name === "AbortError") return; }
  }
  await navigator.clipboard.writeText(payload); showToast(t("copied"));
}

async function shareBrief() {
  const result = assessBatch(batch);
  const trace = decisionTrace(batch);
  const summary = `${t("briefTitle")}\n${t(`verdict_${result.verdict}`)} · ${t(`action_${result.action}`)}\n\n${trace.signals.map(signal => `${briefSignalLabel(signal.key)}: ${briefSignalValue(signal)} (${briefStatus(signal.status)})`).join("\n")}\n\n${t("briefUnknowns")}: ${trace.unknowns.map(key => t(`unknown_${key}`)).join(", ")}`;
  const payload = `${summary}\n\n${JSON.stringify(agentHandoff(batch), null, 2)}`;
  if (navigator.share) {
    try { await navigator.share({title:`${batch.name} · ${t("briefTitle")}`,text:payload}); return; } catch (error) { if (error.name === "AbortError") return; }
  }
  await navigator.clipboard.writeText(payload); showToast(t("briefCopied"));
}

$("#brief-share-button").addEventListener("click", shareBrief);

function exportJson() {
  const blob = new Blob([JSON.stringify({batch,handoff:agentHandoff(batch)},null,2)],{type:"application/json"});
  const link = document.createElement("a"); link.href = URL.createObjectURL(blob); link.download = `${batch.name.replace(/[^\p{L}\p{N}]+/gu,"-").toLowerCase()}.json`; link.click(); URL.revokeObjectURL(link.href); showToast(t("exported"));
}

$("#share-button").addEventListener("click", shareHandoff);
$("#more-button").addEventListener("click", exportJson);
$("#reset-button").addEventListener("click", () => { if (confirm(t("confirmReset"))) { localStorage.removeItem(STORAGE_KEY); batch=null; render(); window.scrollTo({top:0,behavior:"smooth"}); } });
languageSelect.addEventListener("change", event => { language=event.target.value; localStorage.setItem(LANGUAGE_KEY,language); translatePage(); });
document.querySelectorAll("[data-consent]").forEach(button => button.addEventListener("click", () => acceptConsent(button.dataset.consent)));

$("#started-at").value = localDateInput(new Date());
if (!batch && new URLSearchParams(location.search).has("demo")) loadDemo();
translatePage();
showConsentIfNeeded();
if ("serviceWorker" in navigator && location.protocol.startsWith("http")) {
  navigator.serviceWorker.register("sw.js", { updateViaCache:"none" }).then(registration => registration.update()).catch(() => {});
}
