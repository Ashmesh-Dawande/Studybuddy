import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# API CONFIG
# =========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"

# =========================
# LANGUAGES
# =========================
LANGUAGES = ["English", "Hinglish", "Tanglish", "Telugu", "French"]

# =========================
# PROFICIENCY LEVELS
# =========================
PROFICIENCY_LEVELS = ["Beginner", "Intermediate", "Advanced"]

# =========================
# EXAMS & SECTIONS
# =========================
EXAMS = ["CAT", "GRE", "GMAT", "JEE Mains", "NEET"]

SECTIONS = {
    "CAT": ["VARC", "DILR", "QA"],
    "GRE": ["Verbal Reasoning", "Quantitative Reasoning", "Analytical Writing"],
    "GMAT": ["Verbal", "Quant", "Data Insights"],
    "JEE Mains": ["Physics", "Chemistry", "Mathematics"],
    "NEET": ["Physics", "Chemistry", "Biology"],
}


def get_sections(exam: str):
    return SECTIONS.get(exam, [])


# =========================
# UI TRANSLATIONS
# =========================
UI_TEXT = {
    "English": {
        "welcome": "👋 Welcome to **MAT** — your AI tutor!\n\nYou're preparing for **{exam}** › **{section}**.",
        "try_asking": "**Try asking:**",
        "ask_placeholder": "Ask your doubt...",
        "thinking": "Thinking...",
        "settings": "Settings",
        "tools": "Tools",
        "new_chat": "New Chat",
        "back_to_chat": "Back to Chat",
    },
    "Hinglish": {
        "welcome": "👋 **MAT** mein swagat hai — aapka AI tutor!\n\nAap **{exam}** › **{section}** ki preparation kar rahe ho.",
        "try_asking": "**Yeh poochne ki koshish karo:**",
        "ask_placeholder": "Apna doubt pooch...",
        "thinking": "Soch raha hoon...",
        "settings": "Settings",
        "tools": "Tools",
        "new_chat": "Naya Chat",
        "back_to_chat": "Chat par wapas",
    },
    "Tanglish": {
        "welcome": "👋 **MAT**-ku vaanga — unga AI tutor!\n\nNeenga **{exam}** › **{section}** ku prepare pannreenga.",
        "try_asking": "**Idha try pannunga:**",
        "ask_placeholder": "Unga doubt-a kelunga...",
        "thinking": "Yosikiren...",
        "settings": "Settings",
        "tools": "Tools",
        "new_chat": "Pudhu Chat",
        "back_to_chat": "Chat-ku thirumbu",
    },
    "Telugu": {
        "welcome": "👋 **MAT** కి స్వాగతం — మీ AI ట్యూటర్!\n\nమీరు **{exam}** › **{section}** కోసం సిద్ధం అవుతున్నారు.",
        "try_asking": "**ఇవి అడగండి:**",
        "ask_placeholder": "మీ సందేహం అడగండి...",
        "thinking": "ఆలోచిస్తున్నాను...",
        "settings": "సెట్టింగ్స్",
        "tools": "టూల్స్",
        "new_chat": "కొత్త చాట్",
        "back_to_chat": "చాట్‌కి తిరిగి",
    },
    "French": {
        "welcome": "👋 Bienvenue sur **MAT** — votre tuteur IA !\n\nVous préparez **{exam}** › **{section}**.",
        "try_asking": "**Essayez de demander :**",
        "ask_placeholder": "Posez votre question...",
        "thinking": "Je réfléchis...",
        "settings": "Paramètres",
        "tools": "Outils",
        "new_chat": "Nouveau Chat",
        "back_to_chat": "Retour au chat",
    },
}


def get_ui_text(language: str, key: str) -> str:
    return UI_TEXT.get(language, UI_TEXT["English"]).get(key, UI_TEXT["English"][key])


# =========================
# STARTER QUESTIONS (MULTILINGUAL)
# =========================
STARTER_QUESTIONS = {
    "English": {
        "CAT": {
            "VARC": [
                "Tips to improve Reading Comprehension speed?",
                "Common para jumbles strategy?",
                "How to handle inference-based questions?",
            ],
            "DILR": [
                "How to approach Logical Reasoning sets?",
                "Best DI calculation shortcuts?",
                "How to identify easy sets in DILR?",
            ],
            "QA": [
                "Important formulas for Time & Work?",
                "Quick tricks for Number System?",
                "Best approach for Geometry questions?",
            ],
        },
        "GRE": {
            "Verbal Reasoning": [
                "How to master GRE vocabulary?",
                "Best strategy for Text Completion?",
                "Reading Comprehension tips?",
            ],
            "Quantitative Reasoning": [
                "Important Quant formulas to memorize?",
                "How to approach Data Interpretation?",
                "Tricks for Quantitative Comparison?",
            ],
            "Analytical Writing": [
                "Essay structure for Issue Task?",
                "How to write a strong Argument essay?",
                "Common mistakes in AWA?",
            ],
        },
        "GMAT": {
            "Verbal": [
                "Sentence Correction key rules?",
                "Critical Reasoning shortcuts?",
                "RC strategy for GMAT?",
            ],
            "Quant": [
                "Important GMAT Quant formulas?",
                "Problem Solving vs Data Sufficiency?",
                "Time management in Quant?",
            ],
            "Data Insights": [
                "How to approach Data Insights?",
                "Tips for Multi-Source Reasoning?",
                "Table Analysis shortcuts?",
            ],
        },
        "JEE Mains": {
            "Physics": [
                "Important Mechanics concepts?",
                "How to solve Rotational Motion?",
                "Electrostatics revision tips?",
            ],
            "Chemistry": [
                "Important Organic reactions?",
                "Inorganic Chemistry tricks?",
                "Physical Chemistry must-know formulas?",
            ],
            "Mathematics": [
                "Best Calculus strategy?",
                "Coordinate Geometry shortcuts?",
                "How to solve Probability fast?",
            ],
        },
        "NEET": {
            "Physics": [
                "How to solve Mechanics fast?",
                "Important Modern Physics topics?",
                "Best way to revise Optics?",
            ],
            "Chemistry": [
                "Important Organic concepts?",
                "Inorganic Chemistry shortcuts?",
                "How to revise Periodic Table?",
            ],
            "Biology": [
                "Best way to learn Human Physiology?",
                "Important Genetics concepts?",
                "How to memorize Plant Kingdom?",
            ],
        },
    },
    "Hinglish": {
        "CAT": {
            "VARC": [
                "Reading Comprehension speed kaise badhau?",
                "Para jumbles ka best strategy kya hai?",
                "Inference questions kaise solve karu?",
            ],
            "DILR": [
                "Logical Reasoning sets kaise approach karu?",
                "DI calculation ke shortcuts batao?",
                "Easy sets kaise identify karu DILR mein?",
            ],
            "QA": [
                "Time & Work ke important formulas?",
                "Number System ke quick tricks?",
                "Geometry questions ka best approach?",
            ],
        },
        "GRE": {
            "Verbal Reasoning": [
                "GRE vocabulary kaise master karu?",
                "Text Completion ka best strategy?",
                "Reading Comprehension tips do?",
            ],
            "Quantitative Reasoning": [
                "Important Quant formulas yaad karne hain?",
                "Data Interpretation kaise solve karu?",
                "Quantitative Comparison ke tricks?",
            ],
            "Analytical Writing": [
                "Issue Task ka essay structure?",
                "Strong Argument essay kaise likhu?",
                "AWA mein common mistakes kya hain?",
            ],
        },
        "GMAT": {
            "Verbal": [
                "Sentence Correction ke key rules?",
                "Critical Reasoning ke shortcuts?",
                "GMAT RC ka strategy?",
            ],
            "Quant": [
                "GMAT Quant ke important formulas?",
                "Problem Solving vs Data Sufficiency mein farak?",
                "Quant mein time management kaise karu?",
            ],
            "Data Insights": [
                "Data Insights kaise approach karu?",
                "Multi-Source Reasoning ke tips?",
                "Table Analysis ke shortcuts?",
            ],
        },
        "JEE Mains": {
            "Physics": [
                "Mechanics ke important concepts?",
                "Rotational Motion kaise solve karu?",
                "Electrostatics ke revision tips?",
            ],
            "Chemistry": [
                "Important Organic reactions batao?",
                "Inorganic Chemistry ke tricks?",
                "Physical Chemistry ke must-know formulas?",
            ],
            "Mathematics": [
                "Calculus ka best strategy?",
                "Coordinate Geometry ke shortcuts?",
                "Probability kaise fast solve karu?",
            ],
        },
        "NEET": {
            "Physics": [
                "Mechanics fast kaise solve karu?",
                "Modern Physics ke important topics?",
                "Optics revise karne ka best tarika?",
            ],
            "Chemistry": [
                "Important Organic concepts?",
                "Inorganic Chemistry ke shortcuts?",
                "Periodic Table kaise revise karu?",
            ],
            "Biology": [
                "Human Physiology kaise sikhu?",
                "Genetics ke important concepts?",
                "Plant Kingdom kaise yaad karu?",
            ],
        },
    },
    "Tanglish": {
        "CAT": {
            "VARC": [
                "Reading Comprehension speed eppadi increase pannrathu?",
                "Para jumbles ku enna best strategy?",
                "Inference questions eppadi solve pannrathu?",
            ],
            "DILR": [
                "Logical Reasoning sets eppadi approach pannrathu?",
                "DI calculation shortcuts sollu?",
                "Easy sets eppadi identify pannrathu DILR-la?",
            ],
            "QA": [
                "Time & Work ku important formulas?",
                "Number System ku quick tricks?",
                "Geometry questions ku best approach?",
            ],
        },
        "GRE": {
            "Verbal Reasoning": [
                "GRE vocabulary eppadi master pannrathu?",
                "Text Completion ku best strategy?",
                "Reading Comprehension tips sollu?",
            ],
            "Quantitative Reasoning": [
                "Important Quant formulas enna?",
                "Data Interpretation eppadi solve pannrathu?",
                "Quantitative Comparison tricks?",
            ],
            "Analytical Writing": [
                "Issue Task ku essay structure eppadi?",
                "Strong Argument essay eppadi ezhudhrathu?",
                "AWA-la common mistakes enna?",
            ],
        },
        "GMAT": {
            "Verbal": [
                "Sentence Correction key rules enna?",
                "Critical Reasoning shortcuts sollu?",
                "GMAT RC strategy?",
            ],
            "Quant": [
                "GMAT Quant important formulas?",
                "Problem Solving vs Data Sufficiency vethyasam?",
                "Quant-la time management eppadi?",
            ],
            "Data Insights": [
                "Data Insights eppadi approach pannrathu?",
                "Multi-Source Reasoning tips?",
                "Table Analysis shortcuts?",
            ],
        },
        "JEE Mains": {
            "Physics": [
                "Mechanics important concepts enna?",
                "Rotational Motion eppadi solve pannrathu?",
                "Electrostatics revision tips?",
            ],
            "Chemistry": [
                "Important Organic reactions sollu?",
                "Inorganic Chemistry tricks?",
                "Physical Chemistry must-know formulas?",
            ],
            "Mathematics": [
                "Calculus best strategy?",
                "Coordinate Geometry shortcuts?",
                "Probability fast eppadi solve pannrathu?",
            ],
        },
        "NEET": {
            "Physics": [
                "Mechanics fast eppadi solve pannrathu?",
                "Modern Physics important topics?",
                "Optics revise pannra best way?",
            ],
            "Chemistry": [
                "Important Organic concepts?",
                "Inorganic Chemistry shortcuts?",
                "Periodic Table eppadi revise pannrathu?",
            ],
            "Biology": [
                "Human Physiology eppadi padikkrathu?",
                "Genetics important concepts?",
                "Plant Kingdom eppadi memorize pannrathu?",
            ],
        },
    },
    "Telugu": {
        "CAT": {
            "VARC": [
                "Reading Comprehension వేగాన్ని ఎలా పెంచాలి?",
                "Para jumbles కి best strategy ఏమిటి?",
                "Inference questions ఎలా solve చేయాలి?",
            ],
            "DILR": [
                "Logical Reasoning sets ఎలా approach చేయాలి?",
                "DI calculation shortcuts చెప్పండి?",
                "Easy sets ఎలా identify చేయాలి DILR లో?",
            ],
            "QA": [
                "Time & Work ముఖ్యమైన formulas?",
                "Number System quick tricks?",
                "Geometry questions కి best approach?",
            ],
        },
        "GRE": {
            "Verbal Reasoning": [
                "GRE vocabulary ఎలా master చేయాలి?",
                "Text Completion కి best strategy?",
                "Reading Comprehension tips?",
            ],
            "Quantitative Reasoning": [
                "ముఖ్యమైన Quant formulas?",
                "Data Interpretation ఎలా solve చేయాలి?",
                "Quantitative Comparison tricks?",
            ],
            "Analytical Writing": [
                "Issue Task essay structure?",
                "Strong Argument essay ఎలా రాయాలి?",
                "AWA లో common mistakes?",
            ],
        },
        "GMAT": {
            "Verbal": [
                "Sentence Correction key rules?",
                "Critical Reasoning shortcuts?",
                "GMAT RC strategy?",
            ],
            "Quant": [
                "GMAT Quant ముఖ్యమైన formulas?",
                "Problem Solving vs Data Sufficiency తేడా?",
                "Quant లో time management?",
            ],
            "Data Insights": [
                "Data Insights ఎలా approach చేయాలి?",
                "Multi-Source Reasoning tips?",
                "Table Analysis shortcuts?",
            ],
        },
        "JEE Mains": {
            "Physics": [
                "Mechanics ముఖ్యమైన concepts?",
                "Rotational Motion ఎలా solve చేయాలి?",
                "Electrostatics revision tips?",
            ],
            "Chemistry": [
                "ముఖ్యమైన Organic reactions?",
                "Inorganic Chemistry tricks?",
                "Physical Chemistry must-know formulas?",
            ],
            "Mathematics": [
                "Calculus best strategy?",
                "Coordinate Geometry shortcuts?",
                "Probability ఎలా fast solve చేయాలి?",
            ],
        },
        "NEET": {
            "Physics": [
                "Mechanics fast ఎలా solve చేయాలి?",
                "Modern Physics ముఖ్యమైన topics?",
                "Optics revise చేయడానికి best way?",
            ],
            "Chemistry": [
                "ముఖ్యమైన Organic concepts?",
                "Inorganic Chemistry shortcuts?",
                "Periodic Table ఎలా revise చేయాలి?",
            ],
            "Biology": [
                "Human Physiology ఎలా నేర్చుకోవాలి?",
                "Genetics ముఖ్యమైన concepts?",
                "Plant Kingdom ఎలా గుర్తుంచుకోవాలి?",
            ],
        },
    },
    "French": {
        "CAT": {
            "VARC": [
                "Conseils pour améliorer la vitesse de Reading Comprehension ?",
                "Stratégie pour les para jumbles ?",
                "Comment gérer les questions d'inférence ?",
            ],
            "DILR": [
                "Comment aborder les sets de Logical Reasoning ?",
                "Meilleurs raccourcis de calcul DI ?",
                "Comment identifier les sets faciles en DILR ?",
            ],
            "QA": [
                "Formules importantes pour Time & Work ?",
                "Astuces rapides pour Number System ?",
                "Meilleure approche pour Geometry ?",
            ],
        },
        "GRE": {
            "Verbal Reasoning": [
                "Comment maîtriser le vocabulaire GRE ?",
                "Meilleure stratégie pour Text Completion ?",
                "Conseils pour Reading Comprehension ?",
            ],
            "Quantitative Reasoning": [
                "Formules Quant importantes à mémoriser ?",
                "Comment aborder Data Interpretation ?",
                "Astuces pour Quantitative Comparison ?",
            ],
            "Analytical Writing": [
                "Structure d'essai pour Issue Task ?",
                "Comment écrire un Argument essay solide ?",
                "Erreurs courantes en AWA ?",
            ],
        },
        "GMAT": {
            "Verbal": [
                "Règles clés de Sentence Correction ?",
                "Raccourcis de Critical Reasoning ?",
                "Stratégie RC pour GMAT ?",
            ],
            "Quant": [
                "Formules importantes GMAT Quant ?",
                "Problem Solving vs Data Sufficiency ?",
                "Gestion du temps en Quant ?",
            ],
            "Data Insights": [
                "Comment aborder Data Insights ?",
                "Conseils pour Multi-Source Reasoning ?",
                "Raccourcis pour Table Analysis ?",
            ],
        },
        "JEE Mains": {
            "Physics": [
                "Concepts importants de Mechanics ?",
                "Comment résoudre Rotational Motion ?",
                "Conseils de révision pour Electrostatics ?",
            ],
            "Chemistry": [
                "Réactions Organic importantes ?",
                "Astuces Inorganic Chemistry ?",
                "Formules essentielles Physical Chemistry ?",
            ],
            "Mathematics": [
                "Meilleure stratégie pour Calculus ?",
                "Raccourcis Coordinate Geometry ?",
                "Comment résoudre Probability rapidement ?",
            ],
        },
        "NEET": {
            "Physics": [
                "Comment résoudre Mechanics rapidement ?",
                "Sujets importants de Modern Physics ?",
                "Meilleure façon de réviser Optics ?",
            ],
            "Chemistry": [
                "Concepts Organic importants ?",
                "Raccourcis Inorganic Chemistry ?",
                "Comment réviser Periodic Table ?",
            ],
            "Biology": [
                "Meilleure façon d'apprendre Human Physiology ?",
                "Concepts importants de Genetics ?",
                "Comment mémoriser Plant Kingdom ?",
            ],
        },
    },
}


def get_starter_questions(language, exam, section):
    lang_data = STARTER_QUESTIONS.get(language, STARTER_QUESTIONS["English"])
    return lang_data.get(exam, {}).get(section, [
        "Explain this section overview?",
        "Best preparation strategy?",
        "Top 5 important topics?",
    ])