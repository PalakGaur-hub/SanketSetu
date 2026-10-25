
const API_BASE = "http://127.0.0.1:5000";



const GESTURE_TRANSLATIONS = {
    "Dog": ["कुत्ता", "Chien"],
    "loud": ["ज़ोरदार", "Fort"],
    "Mean": ["मतलब", "Signifier"],
    "Plane": ["हवाई जहाज़", "Avion"],
    "Car": ["कार", "Voiture"],
    "rich": ["अमीर", "Riche"],
    "Truck": ["ट्रक", "Camion"],
    "poor": ["गरीब", "Pauvre"],
    "Attack": ["हमला", "Attaque"],
    "Bicycle": ["साइकिल", "Vélo"],
    "thick": ["मोटा", "Épais"],
    "Bus": ["बस", "Bus"],
    "Boat": ["नाव", "Bateau"],
    "expensive": ["महँगा", "Cher"],
    "cheap": ["सस्ता", "Bon marché"],
    "train ticket": ["ट्रेन का टिकट", "Billet de train"],
    "Transportation": ["परिवहन", "Transport"],
    "flat": ["समतल", "Plat"],
    "City": ["शहर", "Ville"],
    "curved": ["घुमावदार", "Courbé"],
    "House": ["घर", "Maison"],
    "male": ["पुरुष", "Masculin"],
    "Cat": ["बिल्ली", "Chat"],
    "quiet": ["शांत", "Calme"],
    "Street or Road": ["सड़क", "Rue ou route"],
    "female": ["महिला", "Féminin"],
    "Train Station": ["रेलवे स्टेशन", "Gare"],
    "tight": ["कसा हुआ", "Serré"],
    "Restaurant": ["रेस्तराँ", "Restaurant"],
    "loose": ["ढीला", "Lâche"],
    "Court": ["अदालत", "Tribunal"],
    "high": ["ऊँचा", "Haut"],
    "School": ["विद्यालय", "École"],
    "low": ["नीचा", "Bas"],
    "Office": ["कार्यालय", "Bureau"],
    "soft": ["नरम", "Doux"],
    "University": ["विश्वविद्यालय", "Université"],
    "hard": ["कठोर", "Dur"],
    "Park": ["पार्क", "Parc"],
    "deep": ["गहरा", "Profond"],
    "Store or Shop": ["दुकान", "Magasin"],
    "shallow": ["उथला", "Peu profond"],
    "Library": ["पुस्तकालय", "Bibliothèque"],
    "clean": ["साफ़", "Propre"],
    "Fish": ["मछली", "Poisson"],
    "happy": ["खुश", "Heureux / Heureuse"],
    "Hospital": ["अस्पताल", "Hôpital"],
    "dirty": ["गंदा", "Sale"],
    "Temple": ["मंदिर", "Temple"],
    "strong": ["मज़बूत", "Fort"],
    "Market": ["बाज़ार", "Marché"],
    "weak": ["कमज़ोर", "Faible"],
    "India": ["भारत", "Inde"],
    "dead": ["मृत", "Mort"],
    "Ground": ["मैदान", "Terrain"],
    "alive": ["जीवित", "Vivant"],
    "Bank": ["बैंक", "Banque"],
    "heavy": ["भारी", "Lourd"],
    "Location": ["स्थान", "Lieu"],
    "light": ["हल्का", "Léger"],
    "Hat": ["टोपी", "Chapeau"],
    "Dress": ["पोशाक", "Robe"],
    "Suit": ["सूट", "Costume"],
    "famous": ["प्रसिद्ध", "Célèbre"],
    "Bird": ["पक्षी", "Oiseau"],
    "sad": ["उदास", "Triste"],
    "I": ["मैं", "Je"],
    "Skirt": ["स्कर्ट", "Jupe"],
    "Shirt": ["कमीज़", "Chemise"],
    "you": ["तुम / आप", "Tu / Vous"],
    "T-Shirt": ["टी-शर्ट", "T-shirt"],
    "he": ["वह (पुरुष)", "Il"],
    "Pant": ["पतलून", "Pantalon"],
    "she": ["वह (महिला)", "Elle"],
    "Shoes": ["जूते", "Chaussures"],
    "it": ["यह / वह", "Il / Elle / Cela"],
    "Pocket": ["जेब", "Poche"],
    "we": ["हम", "Nous"],
    "Clothing": ["कपड़े", "Vêtements"],
    "you (plural)": ["आप सब", "Vous (pluriel)"],
    "Red": ["लाल", "Rouge"],
    "they": ["वे", "Ils / Elles"],
    "Green": ["हरा", "Vert"],
    "Hello": ["नमस्ते", "Bonjour"],
    "Blue": ["नीला", "Bleu"],
    "How are you": ["आप कैसे हैं?", "Comment allez-vous ?"],
    "Beautiful": ["सुंदर", "Beau / Belle"],
    "Cow": ["गाय", "Vache"],
    "Alright": ["ठीक है", "D'accord"],
    "Yellow": ["पीला", "Jaune"],
    "Brown": ["भूरा", "Marron"],
    "Clock": ["घड़ी", "Horloge"],
    "Good Morning": ["सुप्रभात", "Bonjour"],
    "Good afternoon": ["शुभ दोपहर", "Bon après-midi"],
    "Lamp": ["दीपक", "Lampe"],
    "Pink": ["गुलाबी", "Rose"],
    "Fan": ["पंखा", "Ventilateur"],
    "Good evening": ["शुभ संध्या", "Bonsoir"],
    "Orange": ["नारंगी", "Orange"],
    "Black": ["काला", "Noir"],
    "Cell phone": ["मोबाइल फ़ोन", "Téléphone portable"],
    "Good night": ["शुभ रात्रि", "Bonne nuit"],
    "Computer": ["कंप्यूटर", "Ordinateur"],
    "Thank you": ["धन्यवाद", "Merci"],
    "White": ["सफ़ेद", "Blanc"],
    "Grey": ["धूसर", "Gris"],
    "Laptop": ["लैपटॉप", "Ordinateur portable"],
    "Pleased": ["प्रसन्न", "Ravi / Ravie"],
    "Colour": ["रंग", "Couleur"],
    "Screen": ["स्क्रीन", "Écran"],
    "Camera": ["कैमरा", "Appareil photo"],
    "Son": ["बेटा", "Fils"],
    "Daughter": ["बेटी", "Fille"],
    "Television": ["टेलीविज़न", "Télévision"],
    "Mouse": ["माउस", "Souris"],
    "Ugly": ["बदसूरत", "Laid / Laide"],
    "Mother": ["माँ", "Mère"],
    "Radio": ["रेडियो", "Radio"],
    "Father": ["पिता", "Père"],
    "Summer": ["गर्मी", "Été"],
    "Parent": ["माता-पिता", "Parent"],
    "Spring": ["वसंत", "Printemps"],
    "Baby": ["शिशु", "Bébé"],
    "Winter": ["सर्दी", "Hiver"],
    "Fall": ["पतझड़", "Automne"],
    "Man": ["आदमी", "Homme"],
    "Season": ["ऋतु", "Saison"],
    "Woman": ["महिला", "Femme"],
    "Brother": ["भाई", "Frère"],
    "Sunday": ["रविवार", "Dimanche"],
    "Monday": ["सोमवार", "Lundi"],
    "Sister": ["बहन", "Sœur"],
    "Family": ["परिवार", "Famille"],
    "Tuesday": ["मंगलवार", "Mardi"],
    "Grandfather": ["दादा / नाना", "Grand-père"],
    "Wednesday": ["बुधवार", "Mercredi"],
    "Deaf": ["बधिर", "Sourd / Sourde"],
    "Horse": ["घोड़ा", "Cheval"],
    "Grandmother": ["दादी / नानी", "Grand-mère"],
    "Thursday": ["गुरुवार", "Jeudi"],
    "Friday": ["शुक्रवार", "Vendredi"],
    "Husband": ["पति", "Mari"],
    "Saturday": ["शनिवार", "Samedi"],
    "Wife": ["पत्नी", "Épouse"],
    "King": ["राजा", "Roi"],
    "Today": ["आज", "Aujourd'hui"],
    "Queen": ["रानी", "Reine"],
    "Tomorrow": ["कल (आने वाला)", "Demain"],
    "President": ["राष्ट्रपति", "Président / Présidente"],
    "Yesterday": ["कल (बीता हुआ)", "Hier"],
    "Neighbour": ["पड़ोसी", "Voisin / Voisine"],
    "Week": ["सप्ताह", "Semaine"],
    "Boy": ["लड़का", "Garçon"],
    "Month": ["महीना", "Mois"],
    "Girl": ["लड़की", "Fille"],
    "Year": ["वर्ष", "Année"],
    "long": ["लंबा", "Long"],
    "Child": ["बच्चा", "Enfant"],
    "Hour": ["घंटा", "Heure"],
    "short": ["छोटा", "Court"],
    "Animal": ["जानवर", "Animal"],
    "Blind": ["नेत्रहीन", "Aveugle"],
    "Adult": ["वयस्क", "Adulte"],
    "Minute": ["मिनट", "Minute"],
    "tall": ["लंबा", "Grand"],
    "Friend": ["दोस्त", "Ami / Amie"],
    "wide": ["चौड़ा", "Large"],
    "Morning": ["सुबह", "Matin"],
    "Player": ["खिलाड़ी", "Joueur / Joueuse"],
    "narrow": ["संकरा", "Étroit"],
    "Afternoon": ["दोपहर", "Après-midi"],
    "Crowd": ["भीड़", "Foule"],
    "big large": ["बड़ा", "Grand"],
    "Evening": ["शाम", "Soir"],
    "Teacher": ["शिक्षक", "Enseignant / Enseignante"],
    "small little": ["छोटा", "Petit"],
    "Night": ["रात", "Nuit"],
    "Student": ["विद्यार्थी", "Étudiant / Étudiante"],
    "slow": ["धीमा", "Lent"],
    "Lawyer": ["वकील", "Avocat / Avocate"],
    "Time": ["समय", "Temps"],
    "fast": ["तेज़", "Rapide"],
    "Doctor": ["डॉक्टर", "Médecin"],
    "hot": ["गर्म", "Chaud"],
    "Patient": ["मरीज़", "Patient / Patiente"],
    "cold": ["ठंडा", "Froid"],
    "Waiter": ["वेटर", "Serveur / Serveuse"],
    "warm": ["गुनगुना", "Tiède"],
    "Train": ["रेलगाड़ी", "Train"],
    "Secretary": ["सचिव", "Secrétaire"],
    "cool": ["ठंडा", "Frais"],
    "Priest": ["पुजारी", "Prêtre"],
    "new": ["नया", "Nouveau / Nouvelle"],
    "Police": ["पुलिस", "Police"],
    "old": ["पुराना", "Vieux / Vieille"],
    "Soldier": ["सैनिक", "Soldat"],
    "young": ["युवा", "Jeune"],
    "Artist": ["कलाकार", "Artiste"],
    "good": ["अच्छा", "Bon / Bonne"],
    "Author": ["लेखक", "Auteur / Autrice"],
    "bad": ["बुरा", "Mauvais / Mauvaise"],
    "Manager": ["प्रबंधक", "Responsable"],
    "wet": ["गीला", "Mouillé"],
    "Reporter": ["रिपोर्टर", "Reporter"],
    "dry": ["सूखा", "Sec"],
    "Actor": ["अभिनेता", "Acteur / Actrice"],
    "sick": ["बीमार", "Malade"],
    "Job": ["नौकरी", "Emploi"],
    "healthy": ["स्वस्थ", "En bonne santé"],
    "Ex. Monsoon": ["उदाहरण: मानसून", "Ex. mousson"]
};

// Keep your existing getGestureTranslations function,
// but change its return statement to this:
function getGestureTranslations(gestureLabel) {
    const cleanLabel = String(gestureLabel || "")
        .replace(/^\d+\.\s*/, "")
        .trim();

    const translation = GESTURE_TRANSLATIONS[cleanLabel];

    if (!translation) return null;

    return {
        en: cleanLabel,
        hi: translation[0],
        fr: translation[1]
    };
}



function getGestureTranslations(gestureLabel) {
    const cleanLabel = String(gestureLabel || "")
        .replace(/^\d+\.\s*/, "")
        .trim();

    const translation = GESTURE_TRANSLATIONS[cleanLabel];

    if (!translation) return null;

    return {
        en: cleanLabel,
        hi: translation[0],
        fr: translation[1]
    };
}



const detectButton = document.getElementById("detect-button");
const resetButton = document.getElementById("reset-detection");
const sampleSelect = document.getElementById("sample-select");
const gestureName = document.getElementById("gesture-name");
const gestureMeaning = document.getElementById("gesture-meaning");
const confidenceValue = document.getElementById("confidence-value");
const predictionStatus = document.querySelector(".prediction-status");
const historyPanel = document.querySelector(".prediction-history");

// Your test set contains 420 samples: indices 0 through 419.
function populateSamples() {
    if (!sampleSelect) return;

    sampleSelect.innerHTML = "";

    for (let i = 0; i < 420; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.textContent = `Test Sample ${i}`;
        sampleSelect.appendChild(option);
    }

    sampleSelect.value = "0";
}

async function checkBackend() {
    try {
        const response = await fetch(`${API_BASE}/api/status`);
        if (!response.ok) throw new Error("Backend is not responding.");

        const data = await response.json();
        console.log("SanketSetu backend:", data);

        if (predictionStatus) {
            predictionStatus.textContent = "Backend ready";
        }
    } catch (error) {
        console.error("Backend connection failed:", error);

        if (predictionStatus) {
            predictionStatus.textContent = "Backend offline";
        }
    }
}

function addHistory(data) {
    if (!historyPanel) return;

    const empty = historyPanel.querySelector(".history-empty");
    if (empty) empty.remove();

    const item = document.createElement("div");
    item.className = "history-item";

    const predicted = String(data.gesture ?? data.predicted_class ?? "Unknown");
    const expected = String(data.expected_label ?? "Unavailable");
    const isCorrect = predicted === expected;

    const label = document.createElement("strong");
    label.textContent = predicted;

    const detail = document.createElement("span");
    detail.textContent =
        `Sample ${data.sample_index} · ` +
        `${(Number(data.confidence) * 100).toFixed(1)}% confidence`;

    const comparison = document.createElement("span");
    comparison.textContent = `Expected: ${expected}`;

    const result = document.createElement("span");
    result.textContent = data.expected_label == null
        ? "Correctness not available"
        : isCorrect
            ? "Correct prediction"
            : "Incorrect prediction";

    item.append(label, detail, comparison, result);
    historyPanel.prepend(item);
}


async function runSample() {
    const videoUpload = document.getElementById("video-upload");
    const videoFileStatus = document.getElementById("video-file-status");

    const file = videoUpload?.files?.[0];

    if (!file) {
        if (videoFileStatus) {
            videoFileStatus.textContent = "Please choose a video first.";
        }
        return;
    }

    detectButton.disabled = true;
    detectButton.textContent = "Processing...";

    if (videoFileStatus) {
        videoFileStatus.textContent =
            "Extracting landmarks and predicting gesture...";
    }

    try {
        const formData = new FormData();
        formData.append("video", file);

        const response = await fetch(
            `${API_BASE}/api/predict-video`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok || data.status !== "ok") {
            throw new Error(data.message || "Prediction failed.");
        }

        const predicted = data.gesture || "Unknown";

        if (gestureName) {
            gestureName.textContent = predicted;
        }

        if (confidenceValue) {
            confidenceValue.textContent =
                `${(Number(data.confidence) * 100).toFixed(2)}%`;
        }

        if (gestureMeaning) {
            gestureMeaning.textContent =
                `Prediction from ${data.decoded_frames} video frames.`;
        }

        if (predictionStatus) {
            predictionStatus.textContent = "Prediction complete";
        }

        if (videoFileStatus) {
            videoFileStatus.textContent = "Prediction completed!";
        }

        // Show top predictions.
        if (predictionStatus && Array.isArray(data.top_predictions)) {
            predictionStatus.textContent = data.top_predictions
                .map(item =>
                    `${item.gesture}: ${(item.confidence * 100).toFixed(2)}%`
                )
                .join(" | ");
        }

        // Prepare the translation panel.
        let translationPanel =
            document.getElementById("translation-panel");

        if (!translationPanel) {
            translationPanel = document.createElement("div");
            translationPanel.id = "translation-panel";
            translationPanel.style.marginTop = "16px";
            translationPanel.style.padding = "16px";
            translationPanel.style.borderRadius = "12px";
            translationPanel.style.background =
                "rgba(127, 127, 127, 0.08)";
            translationPanel.style.lineHeight = "2";

            const container =
                gestureName?.closest(".prediction-panel") ||
                gestureName?.parentElement;

            container?.appendChild(translationPanel);
        }

        const translations = getGestureTranslations(predicted);

        translationPanel.replaceChildren();

        const heading = document.createElement("h3");
        heading.textContent = "🗺 Gesture Translation";
        translationPanel.appendChild(heading);

        const speechControls = document.createElement("div");
        speechControls.style.display = "flex";
        speechControls.style.gap = "10px";
        speechControls.style.flexWrap = "wrap";
        speechControls.style.marginBottom = "12px";

        [
            { label: "English", code: "en" },
            { label: "हिंदी", code: "hi" },
            { label: "Français", code: "fr" }
        ].forEach(({ label, code }) => {
            const button = document.createElement("button");
            button.type = "button";
            button.textContent = `🗣 ${label}`;
            button.style.padding = "8px 12px";
            button.style.borderRadius = "8px";
            button.style.cursor = "pointer";

            button.addEventListener("click", () => speakGesture(code));
            speechControls.appendChild(button);
        });

        translationPanel.appendChild(speechControls);

        [
            ["English", translations?.en || predicted],
            ["Hindi", translations?.hi || "Translation not available yet"],
            ["French", translations?.fr || "Translation not available yet"]
        ].forEach(([language, phrase]) => {
            const row = document.createElement("p");
            const label = document.createElement("strong");

            label.textContent = `${language}: `;
            row.append(label, document.createTextNode(phrase));
            translationPanel.appendChild(row);
        });

        console.log("Transformer V5.2 video prediction:", data);

    } catch (error) {
        console.error("Video prediction error:", error);

        if (gestureName) {
            gestureName.textContent = "Prediction failed";
        }

        if (gestureMeaning) {
            gestureMeaning.textContent = error.message;
        }

        if (confidenceValue) {
            confidenceValue.textContent = "—";
        }

        if (predictionStatus) {
            predictionStatus.textContent = "Error";
        }

        if (videoFileStatus) {
            videoFileStatus.textContent = error.message;
        }

    } finally {
        detectButton.disabled = false;
        detectButton.textContent = "Run Sample";
    }
}

 
detectButton?.addEventListener("click", runSample);

resetButton?.addEventListener("click", () => {
    if (gestureName) gestureName.textContent = "—";

    if (gestureMeaning) {
        gestureMeaning.textContent =
            "Choose a test sample and click Run Sample.";
    }

    if (confidenceValue) confidenceValue.textContent = "0%";
    if (predictionStatus) predictionStatus.textContent = "Waiting";

    if (historyPanel) {
        historyPanel.innerHTML = `
            <div class="history-empty">
                <span>—</span>
                <p>Your recognized gestures will appear here.</p>
            </div>
        `;
    }
});

populateSamples();
checkBackend();


function speakGesture(language = "en") {
    const gestureName = document.getElementById("gesture-name");
    const translationPanel = document.getElementById("translation-panel");

    if (!gestureName || !window.speechSynthesis) {
        console.error("Text-to-speech is not supported in this browser.");
        return;
    }

    let textToSpeak = gestureName.textContent.trim();

    // Remove the numeric class prefix, e.g. "55. Thank you".
    textToSpeak = textToSpeak.replace(/^\d+\.\s*/, "");

    // Read the selected language's translation from the translation panel.
    const languageLabels = {
        en: "English:",
        hi: "Hindi:",
        fr: "French:"
    };

    if (translationPanel && language !== "en") {
        const rows = translationPanel.querySelectorAll("p");

        for (const row of rows) {
            if (row.textContent.startsWith(languageLabels[language])) {
                textToSpeak = row.textContent
                    .replace(languageLabels[language], "")
                    .trim();
                break;
            }
        }
    }

    if (!textToSpeak || textToSpeak === "—") return;

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(textToSpeak);

    utterance.lang = {
        en: "en-IN",
        hi: "hi-IN",
        fr: "fr-FR"
    }[language] || "en-IN";

    window.speechSynthesis.speak(utterance);
}


const videoUpload = document.getElementById("video-upload");
const videoPreview = document.getElementById("video-preview");
const videoFileStatus = document.getElementById("video-file-status");

videoUpload?.addEventListener("change", () => {
    const file = videoUpload.files?.[0];

    if (!file) {
        videoPreview.removeAttribute("src");
        videoPreview.hidden = true;
        videoFileStatus.textContent = "No video selected.";
        return;
    }

    if (videoPreview.dataset.objectUrl) {
        URL.revokeObjectURL(videoPreview.dataset.objectUrl);
    }

    const videoUrl = URL.createObjectURL(file);

    videoPreview.src = videoUrl;
    videoPreview.dataset.objectUrl = videoUrl;
    videoPreview.hidden = false;

    videoFileStatus.textContent =
        `Selected: ${file.name} (${(file.size / (1024 * 1024)).toFixed(2)} MB)`;
});
