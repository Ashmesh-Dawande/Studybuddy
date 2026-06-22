# MAT


An AI-powered tutoring chatbot that explains concepts in **Hinglish** (Hindi + English), **Tanglish** (Tamil + English), **Telegu**, **English** and **French** — the way students actually talk.

Built with **Streamlit** + **Groq AI** (LLaMA 3.3 70B).

**Live app: [multilingualaitutor.streamlit.app](https://multilingualaitutor.streamlit.app/?exam=CAT&section=VARC&language=English&proficiency=Intermediate&mode=chat)**

---

## Setup

1. **Clone the repo**
   ```bash
   https://github.com/Ashmesh-Dawande/Studybuddy.git
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Groq API key**

   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
   Get a free key at [console.groq.com](https://console.groq.com)

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. Open `http://localhost:8501` in your browser.

---


### Architecture

```
User Input (text)
        |
        v
    app.py (Streamlit UI + session state)
        |
        v
    prompts.py (builds system prompt with class/subject/chapter/language)
        |
        v
    config.py (resolves chapters, starter questions, subject lists)
        |
        v
    Groq API (LLaMA 3.3 70B / LLaMA 4 Scout for vision)
        |
        v
    Response rendered in chat / notes / quiz / flashcards
```

