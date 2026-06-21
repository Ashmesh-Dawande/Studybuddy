
import streamlit as st
from groq import Groq
import json
import re
import random
from config import (
    GROQ_API_KEY,
    MODEL_NAME,
    LANGUAGES,
    PROFICIENCY_LEVELS,
    EXAMS,
    get_sections,
    get_starter_questions,
    get_ui_text,
)
from prompts import get_system_prompt

# =========================
# APP SETUP
# =========================
st.set_page_config(
    page_title="MAT - Multilingual AI Tutor",
    page_icon="M",
    layout="wide",
)

if not GROQ_API_KEY:
    st.error("Missing GROQ_API_KEY. Add it to your .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# =========================
# THEME / CSS (Light + Dark compatible)
# =========================
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1280px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    .mat-header {
        padding: 28px;
        border-radius: 20px;
        background: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.15);
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
    }

    .mat-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        color: var(--text-color);
        line-height: 1.2;
    }

    .mat-subtitle {
        color: var(--text-color);
        opacity: 0.78;
        font-size: 1rem;
        margin-bottom: 0;
    }

    .meta-container {
        margin-top: 15px;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    .meta-pill {
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(120, 120, 120, 0.12);
        border: 1px solid rgba(120, 120, 120, 0.15);
        font-size: 0.85rem;
        color: var(--text-color);
    }

    .page-card {
        padding: 22px;
        border-radius: 18px;
        background: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.12);
        margin-top: 10px;
        margin-bottom: 14px;
    }

    .section-heading {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-color);
        margin-bottom: 6px;
    }

    .section-subtext {
        color: var(--text-color);
        opacity: 0.72;
        margin-bottom: 18px;
        font-size: 0.95rem;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.10);
    }

    .stSelectbox {
        margin-bottom: 10px;
    }

    .stSelectbox label {
        font-weight: 600;
    }

    .stButton > button,
    .stDownloadButton > button,
    .stForm button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        min-height: 44px !important;
        width: 100% !important;
    }

    .stSelectbox > div > div,
    .stTextInput > div > div > input,
    .stTextArea textarea,
    [data-baseweb="select"] > div {
        border-radius: 10px !important;
    }

    [data-testid="stChatMessage"] {
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.15);
        padding: 10px;
        background: var(--secondary-background-color);
    }

    .custom-card {
        padding: 18px;
        border-radius: 16px;
        background: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.12);
        margin-bottom: 10px;
    }

    .stProgress > div > div > div > div {
        background: var(--primary-color);
    }

    .streamlit-expanderHeader {
        font-weight: 600;
    }

    .starter-note {
        color: var(--text-color);
        opacity: 0.75;
        margin: 4px 0 12px 0;
    }

    @media (max-width: 900px) {
        .mat-title {
            font-size: 1.6rem;
        }
        .block-container {
            padding-top: 0.8rem;
        }
        .page-card {
            padding: 18px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# QUERY PARAM HELPERS (persist settings on refresh)
# =========================
def qp_get(name: str, default: str) -> str:
    value = st.query_params.get(name, default)
    if isinstance(value, list):
        return value[0] if value else default
    return value


def safe_choice(value: str, options, default: str) -> str:
    return value if value in options else default


initial_exam = safe_choice(qp_get("exam", EXAMS[0]), EXAMS, EXAMS[0])
initial_sections = get_sections(initial_exam)
initial_section = safe_choice(qp_get("section", initial_sections[0]), initial_sections, initial_sections[0])
initial_language = safe_choice(qp_get("language", LANGUAGES[0]), LANGUAGES, LANGUAGES[0])
initial_proficiency = safe_choice(qp_get("proficiency", PROFICIENCY_LEVELS[1]), PROFICIENCY_LEVELS, PROFICIENCY_LEVELS[1])
initial_mode = safe_choice(qp_get("mode", "chat"), ["chat", "notes", "quiz", "flashcards"], "chat")


def sync_query_params():
    st.query_params["exam"] = st.session_state.exam
    st.query_params["section"] = st.session_state.section
    st.query_params["language"] = st.session_state.language
    st.query_params["proficiency"] = st.session_state.proficiency
    st.query_params["mode"] = st.session_state.mode


# =========================
# SESSION STATE
# =========================
defaults = {
    "exam": initial_exam,
    "section": initial_section,
    "language": initial_language,
    "proficiency": initial_proficiency,
    "messages": [],
    "mode": initial_mode,
    "notes_content": None,
    "quiz_data": None,
    "quiz_answers": {},
    "quiz_submitted": False,
    "flashcard_data": None,
    "flashcard_idx": 0,
    "flashcard_flipped": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# keep URL synced on every load/rerun
sync_query_params()


def reset_tools():
    st.session_state.notes_content = None
    st.session_state.quiz_data = None
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False
    st.session_state.flashcard_data = None
    st.session_state.flashcard_idx = 0
    st.session_state.flashcard_flipped = False


def t(key: str) -> str:
    return get_ui_text(st.session_state.language, key)


def get_clean_welcome_text() -> str:
    language = st.session_state.language
    exam = st.session_state.exam
    section = st.session_state.section

    welcome_map = {
        "English": f"Welcome to **MAT**. You are currently preparing for **{exam}** in **{section}**.",
        "Hinglish": f"Welcome to **MAT**. Aap abhi **{exam}** ke **{section}** section ki preparation kar rahe hain.",
        "Tanglish": f"Welcome to **MAT**. Neenga ippo **{exam}** oda **{section}** section-ku prepare pannreenga.",
        "Telugu": f"Welcome to **MAT**. మీరు ప్రస్తుతం **{exam}** లో **{section}** కోసం సిద్ధమవుతున్నారు.",
        "French": f"Bienvenue sur **MAT**. Vous préparez actuellement **{exam}** pour la section **{section}**.",
    }
    return welcome_map.get(language, welcome_map["English"])


def get_try_asking_text() -> str:
    text_map = {
        "English": "Suggested questions:",
        "Hinglish": "Suggested questions:",
        "Tanglish": "Suggested questions:",
        "Telugu": "Suggested questions:",
        "French": "Questions suggérées :",
    }
    return text_map.get(st.session_state.language, text_map["English"])


def get_scope_refusal() -> str:
    exam = st.session_state.exam
    section = st.session_state.section
    language = st.session_state.language
    refusals = {
        "English": f"I can help only with **{exam} - {section}** related preparation in this chat. Please ask a question related to this exam section.",
        "Hinglish": f"Main is chat mein sirf **{exam} - {section}** se related preparation mein help kar sakta hoon. Kripya isi exam section se related question poochhiye.",
        "Tanglish": f"Indha chat-la naan **{exam} - {section}** related preparation-ku mattum help pannuven. Dayavu se indha exam section related question kelunga.",
        "Telugu": f"ఈ chat లో నేను **{exam} - {section}** కు సంబంధించిన preparation లో మాత్రమే సహాయం చేస్తాను. దయచేసి ఈ exam section కి సంబంధించిన ప్రశ్న అడగండి.",
        "French": f"Je peux aider uniquement pour la préparation liée à **{exam} - {section}** dans cette discussion. Veuillez poser une question liée à cette section de l'examen.",
    }
    return refusals.get(language, refusals["English"])


def get_greeting_response() -> str:
    exam = st.session_state.exam
    section = st.session_state.section
    language = st.session_state.language
    greetings = {
        "English": f"Hello. I am ready to help with **{exam} - {section}**. Ask any concept, formula, shortcut, strategy, or practice question from this section.",
        "Hinglish": f"Hello. Main **{exam} - {section}** mein help karne ke liye ready hoon. Is section se concept, formula, shortcut, strategy ya practice question poochhiye.",
        "Tanglish": f"Hello. Naan **{exam} - {section}**-la help panna ready-a irukken. Indha section-lendhu concept, formula, shortcut, strategy illena practice question kelunga.",
        "Telugu": f"Hello. నేను **{exam} - {section}** లో సహాయం చేయడానికి సిద్ధంగా ఉన్నాను. ఈ section నుంచి concept, formula, shortcut, strategy లేదా practice question అడగండి.",
        "French": f"Bonjour. Je suis prêt à aider pour **{exam} - {section}**. Posez une question sur un concept, une formule, une stratégie ou un exercice de cette section.",
    }
    return greetings.get(language, greetings["English"])


def is_simple_greeting(user_input: str) -> bool:
    text = user_input.strip().lower()
    return text in {
        "hi", "hello", "hey", "hii", "hola", "bonjour", "vanakkam", "namaste", "thanks", "thank you"
    }


def page_card_start(title: str, subtitle: str = ""):
    st.markdown('<div class="page-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-heading">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-subtext">{subtitle}</div>', unsafe_allow_html=True)


def page_card_end():
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# LANGUAGE-AWARE SPINNERS
# =========================
def spinner_text() -> str:
    return t("thinking")


# =========================
# GROQ CALLS
# =========================
def groq_chat(messages, temperature=0.7, max_tokens=1200):
    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"API error: {e}"


def is_exam_related(user_input: str) -> bool:
    try:
        prompt = (
            "You are a strict classifier. Return only YES or NO. "
            f"Check whether the user's message is directly related to preparation for the exam '{st.session_state.exam}' "
            f"and the section '{st.session_state.section}'. "
            "Treat conceptual doubts, formulas, shortcuts, revision, exam strategies, and practice questions for that section as relevant. "
            "Treat coding, general chat, current affairs unrelated to this exam section, entertainment, and any other unrelated topic as NOT relevant. "
            f"User message: {user_input}"
        )
        result = groq_chat(
            [
                {"role": "system", "content": "Return only YES or NO."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=5,
        )
        return result.strip().upper().startswith("YES")
    except Exception:
        lower = user_input.lower()
        exam_keywords = [st.session_state.exam.lower(), st.session_state.section.lower(), "formula", "shortcut", "question", "practice", "revision", "concept"]
        return any(k in lower for k in exam_keywords)


def get_response(user_input: str) -> str:
    if is_simple_greeting(user_input):
        return get_greeting_response()

    if not is_exam_related(user_input):
        return get_scope_refusal()

    system_prompt = get_system_prompt(
        st.session_state.language,
        st.session_state.exam,
        st.session_state.section,
        st.session_state.proficiency,
    )
    scoped_prompt = (
        system_prompt
        + "\n\nIMPORTANT: Answer only questions related to the selected exam and section. "
        + "If a question is outside the selected exam and section, politely refuse and redirect the user back to the selected syllabus."
    )

    messages = [{"role": "system", "content": scoped_prompt}]
    for msg in st.session_state.messages[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_input})
    return groq_chat(messages)


def call_api_json(prompt: str):
    system = get_system_prompt(
        st.session_state.language,
        st.session_state.exam,
        st.session_state.section,
        st.session_state.proficiency,
    )
    content = groq_chat(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.35,
        max_tokens=1800,
    )
    try:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    return None


# =========================
# TOOLS (MULTILINGUAL)
# =========================
def generate_notes():
    lang = st.session_state.language
    exam = st.session_state.exam
    section = st.session_state.section
    lang_instruct = {
        "English": "in clear English",
        "Hinglish": "in Hinglish (Hindi + English mix)",
        "Tanglish": "in Tanglish (Tamil + English mix)",
        "Telugu": "in Telugu with key terms in English",
        "French": "in French",
    }.get(lang, "in English")

    prompt = (
        f"Create a concise revision cheat sheet for {exam} - {section} {lang_instruct}. "
        "Include: key concepts, important formulas/rules, common traps, "
        "must-remember points, and 3 exam tips. "
        "Use clear headings and bullet points. Keep it scannable."
    )
    return groq_chat(
        [
            {"role": "system", "content": get_system_prompt(lang, exam, section, st.session_state.proficiency)},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
        max_tokens=1800,
    )


def generate_quiz():
    lang = st.session_state.language
    exam = st.session_state.exam
    section = st.session_state.section
    lang_instruct = {
        "English": "Questions and explanations in English.",
        "Hinglish": "Questions in English but explanations in Hinglish (Hindi + English mix).",
        "Tanglish": "Questions in English but explanations in Tanglish (Tamil + English mix).",
        "Telugu": "Questions in English but explanations in Telugu.",
        "French": "Questions and explanations in French.",
    }.get(lang, "Questions in English.")

    prompt = (
        f"Create exactly 5 MCQ questions for {exam} - {section}. "
        f"{lang_instruct} "
        "Return ONLY valid JSON in this format:\n"
        '{"questions":[{"q":"...","options":{"A":"...","B":"...","C":"...","D":"..."},'
        '"answer":"A","explanation":"brief explanation"}]}'
    )
    data = call_api_json(prompt)
    return data.get("questions", []) if data else None


def generate_flashcards():
    lang = st.session_state.language
    exam = st.session_state.exam
    section = st.session_state.section
    lang_instruct = {
        "English": "in English",
        "Hinglish": "with answers in Hinglish (Hindi + English mix)",
        "Tanglish": "with answers in Tanglish (Tamil + English mix)",
        "Telugu": "with answers in Telugu",
        "French": "in French",
    }.get(lang, "in English")

    prompt = (
        f"Create exactly 8 revision flashcards for {exam} - {section} {lang_instruct}. "
        "Return ONLY valid JSON in this format:\n"
        '{"flashcards":[{"front":"term or question","back":"answer or definition"}]}'
    )
    data = call_api_json(prompt)
    return data.get("flashcards", []) if data else None


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown(f"### {t('settings')}")

    if st.button(f"{t('new_chat')}", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.session_state.mode = "chat"
        reset_tools()
        sync_query_params()
        st.rerun()

    selected_language = st.selectbox(
        "Language",
        LANGUAGES,
        index=LANGUAGES.index(st.session_state.language),
        help="Select your preferred tutoring language",
    )
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        reset_tools()
        sync_query_params()
        st.rerun()

    selected_exam = st.selectbox("Exam", EXAMS, index=EXAMS.index(st.session_state.exam))
    if selected_exam != st.session_state.exam:
        st.session_state.exam = selected_exam
        st.session_state.section = get_sections(selected_exam)[0]
        st.session_state.messages = []
        reset_tools()
        sync_query_params()
        st.rerun()

    sections_list = get_sections(st.session_state.exam)
    selected_section = st.selectbox(
        "Section",
        sections_list,
        index=sections_list.index(st.session_state.section)
    )
    if selected_section != st.session_state.section:
        st.session_state.section = selected_section
        st.session_state.messages = []
        reset_tools()
        sync_query_params()
        st.rerun()

    selected_proficiency = st.selectbox(
        "Proficiency",
        PROFICIENCY_LEVELS,
        index=PROFICIENCY_LEVELS.index(st.session_state.proficiency),
    )
    if selected_proficiency != st.session_state.proficiency:
        st.session_state.proficiency = selected_proficiency
        reset_tools()
        sync_query_params()
        st.rerun()

    st.divider()
    st.markdown("### Study Tools")

    tool_labels = ["Chat", "Notes", "Quiz", "Flashcards"]
    mode_index = ["chat", "notes", "quiz", "flashcards"].index(st.session_state.mode)
    selected_tool = st.selectbox("Select Tool", tool_labels, index=mode_index)

    mode_map = {
        "Chat": "chat",
        "Notes": "notes",
        "Quiz": "quiz",
        "Flashcards": "flashcards",
    }

    new_mode = mode_map[selected_tool]
    if new_mode != st.session_state.mode:
        st.session_state.mode = new_mode

        if new_mode == "notes":
            st.session_state.notes_content = None
        elif new_mode == "quiz":
            st.session_state.quiz_data = None
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
        elif new_mode == "flashcards":
            st.session_state.flashcard_data = None
            st.session_state.flashcard_idx = 0
            st.session_state.flashcard_flipped = False

        sync_query_params()
        st.rerun()

    st.divider()
    st.caption("Built with Streamlit + Groq AI")


# =========================
# HEADER
# =========================
st.markdown(
    f"""
    <div class="mat-header">
        <div class="mat-title">MAT - Multilingual AI Tutor</div>
        <div class="mat-subtitle">
            Personalized exam preparation assistant for competitive exams.
        </div>
        <div class="meta-container">
            <div class="meta-pill">Language: {st.session_state.language}</div>
            <div class="meta-pill">Exam: {st.session_state.exam}</div>
            <div class="meta-pill">Section: {st.session_state.section}</div>
            <div class="meta-pill">Level: {st.session_state.proficiency}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================
# RENDER MODES
# =========================
def render_notes():
    page_card_start("Quick Notes", "Generate concise revision notes for the selected exam section.")

    if st.session_state.notes_content is None:
        with st.spinner(spinner_text()):
            st.session_state.notes_content = generate_notes()

    st.markdown(st.session_state.notes_content)
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "Download Notes",
            data=st.session_state.notes_content or "",
            file_name=f"{st.session_state.exam}_{st.session_state.section}_notes.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with c2:
        if st.button("Regenerate", use_container_width=True):
            st.session_state.notes_content = None
            st.rerun()

    page_card_end()


def render_quiz():
    page_card_start("Quiz", "Test your preparation with five exam-focused multiple-choice questions.")

    if st.session_state.quiz_data is None:
        with st.spinner(spinner_text()):
            qs = generate_quiz()
            if qs:
                st.session_state.quiz_data = qs
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
            else:
                st.error("Couldn't generate quiz. Please try again.")
                if st.button("Retry"):
                    st.rerun()
                page_card_end()
                return

    qs = st.session_state.quiz_data

    if not st.session_state.quiz_submitted:
        with st.form("quiz_form"):
            for i, q in enumerate(qs):
                st.markdown(f"**Q{i+1}. {q['q']}**")
                options = [f"{k}) {v}" for k, v in q["options"].items()]
                choice = st.radio(
                    f"q_{i}",
                    options,
                    key=f"radio_{i}",
                    index=None,
                    label_visibility="collapsed",
                )
                if choice:
                    st.session_state.quiz_answers[i] = choice[0]
                st.markdown("")
            if st.form_submit_button("Submit Quiz", use_container_width=True, type="primary"):
                st.session_state.quiz_submitted = True
                st.rerun()
    else:
        correct = sum(
            1
            for i, q in enumerate(qs)
            if st.session_state.quiz_answers.get(i) == q["answer"]
        )
        total = len(qs)
        pct = int((correct / total) * 100) if total else 0
        st.markdown(f"## Score: {correct}/{total} ({pct}%)")
        st.progress(pct / 100 if total else 0)
        st.divider()
        for i, q in enumerate(qs):
            ua = st.session_state.quiz_answers.get(i, "—")
            ca = q["answer"]
            ok = ua == ca
            tag = "Correct" if ok else "Incorrect"
            with st.expander(f"{tag} - Q{i+1}. {q['q']}"):
                st.markdown(f"**Your answer:** {ua}) {q['options'].get(ua, 'Not answered')}")
                st.markdown(f"**Correct answer:** {ca}) {q['options'][ca]}")
                if q.get("explanation"):
                    st.info(q["explanation"])
        st.divider()
        if st.button("Generate New Quiz", use_container_width=True):
            st.session_state.quiz_data = None
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.rerun()

    page_card_end()


def render_flashcards():
    page_card_start("Flashcards", "Revise key concepts using interactive flashcards.")

    if st.session_state.flashcard_data is None:
        with st.spinner(spinner_text()):
            cards = generate_flashcards()
            if cards:
                st.session_state.flashcard_data = cards
                st.session_state.flashcard_idx = 0
                st.session_state.flashcard_flipped = False
            else:
                st.error("Couldn't generate flashcards. Please try again.")
                if st.button("Retry"):
                    st.rerun()
                page_card_end()
                return

    cards = st.session_state.flashcard_data
    idx = st.session_state.flashcard_idx
    total = len(cards)
    card = cards[idx]

    st.caption(f"Card {idx + 1} of {total}")
    st.progress((idx + 1) / total if total else 0)

    if not st.session_state.flashcard_flipped:
        st.markdown(
            f"""
            <div class="custom-card">
                <h4 style="margin-top: 0;">Question</h4>
                <div>{card['front']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Show Answer", use_container_width=True, type="primary"):
            st.session_state.flashcard_flipped = True
            st.rerun()
    else:
        st.markdown(
            f"""
            <div class="custom-card">
                <h4 style="margin-top: 0;">Answer</h4>
                <div>{card['back']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Show Question", use_container_width=True):
            st.session_state.flashcard_flipped = False
            st.rerun()

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Previous", use_container_width=True, disabled=(idx == 0)):
            st.session_state.flashcard_idx -= 1
            st.session_state.flashcard_flipped = False
            st.rerun()
    with c2:
        if st.button("Next", use_container_width=True, disabled=(idx == total - 1)):
            st.session_state.flashcard_idx += 1
            st.session_state.flashcard_flipped = False
            st.rerun()
    with c3:
        if st.button("Shuffle", use_container_width=True):
            random.shuffle(st.session_state.flashcard_data)
            st.session_state.flashcard_idx = 0
            st.session_state.flashcard_flipped = False
            st.rerun()

    page_card_end()


def render_chat():
    page_card_start("Tutor Chat", "Ask doubts, concepts, shortcuts, and exam strategy questions for the selected section.")

    if not st.session_state.messages:
        welcome = get_clean_welcome_text()
        st.markdown(f"#### {welcome}")
        st.markdown(f'<div class="starter-note">{get_try_asking_text()}</div>', unsafe_allow_html=True)

        starter_qs = get_starter_questions(
            st.session_state.language,
            st.session_state.exam,
            st.session_state.section,
        )

        for i, q in enumerate(starter_qs):
            if st.button(f"{q}", key=f"starter_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                with st.spinner(spinner_text()):
                    ans = get_response(q)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input(t("ask_placeholder"))
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner(spinner_text()):
                response = get_response(user_input)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    page_card_end()


# =========================
# MODE ROUTING
# =========================
if st.session_state.mode == "notes":
    render_notes()
elif st.session_state.mode == "quiz":
    render_quiz()
elif st.session_state.mode == "flashcards":
    render_flashcards()
else:
    render_chat()
