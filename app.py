import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import json
import time
import re


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY is missing in your .env file.")
    st.stop()


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(api_key=API_KEY)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MythoTales AI",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================================
       MAIN BACKGROUND
       ========================================= */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(255, 190, 215, 0.38),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(205, 180, 240, 0.30),
                transparent 32%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(245, 205, 230, 0.22),
                transparent 35%
            ),
            #fff7fb;
    }


    /* =========================================
       MAIN CONTAINER
       ========================================= */

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }


    /* =========================================
       HEADER
       ========================================= */

    .main-title {
        text-align: center;
        font-size: 44px;
        font-weight: 800;
        color: #17131a;
        margin-top: 5px;
        margin-bottom: 4px;
        letter-spacing: 0.5px;
    }


    .subtitle {
        text-align: center;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 4px;
        color: #79527f;
        margin-bottom: 24px;
    }


    /* =========================================
       SECTION TITLES
       ========================================= */

    .section-title {
        text-align: center;
        font-size: 28px;
        font-weight: 750;
        color: #4a3155;
        margin-top: 25px;
        margin-bottom: 6px;
    }


    .section-text {
        text-align: center;
        color: #806e7d;
        font-size: 14px;
        margin-bottom: 22px;
    }


    /* =========================================
       CENTER CONTENT
       ========================================= */

    .center-content {
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }


    /* =========================================
       STORY CARD
       ========================================= */

    .story-card {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(185, 135, 190, 0.25);
        border-radius: 20px;
        padding: 24px;
        margin-top: 20px;
        margin-bottom: 22px;

        box-shadow:
            0 6px 22px rgba(120, 70, 130, 0.08);
    }


    .story-title {
        font-size: 26px;
        font-weight: 750;
        color: #53345e;
        margin-bottom: 12px;
    }


    .scene-text {
        font-size: 16px;
        line-height: 1.8;
        color: #403740;
    }


    /* =========================================
       QUIZ CARD
       ========================================= */

    .quiz-card {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(185, 135, 190, 0.24);
        border-radius: 18px;
        padding: 20px;
        margin-top: 14px;
        margin-bottom: 16px;

        box-shadow:
            0 5px 18px rgba(120, 70, 130, 0.06);
    }


    /* =========================================
       BUTTONS
       ========================================= */

    div.stButton > button {
        border-radius: 12px;
        font-weight: 650;
        min-height: 42px;
        border: 1px solid rgba(130, 80, 145, 0.25);
    }


    div.stButton > button:hover {
        border-color: rgba(130, 80, 145, 0.55);
    }


    /* =========================================
       INPUTS
       ========================================= */

    div[data-baseweb="select"] > div {
        border-radius: 11px;
    }


    textarea {
        border-radius: 12px !important;
    }


    input {
        border-radius: 11px !important;
    }


    /* =========================================
       LABELS
       ========================================= */

    label {
        color: #514052 !important;
        font-weight: 650 !important;
    }


    /* =========================================
       DIVIDER
       ========================================= */

    hr {
        border: none;
        border-top: 1px solid rgba(150, 105, 160, 0.16);
        margin-top: 25px;
        margin-bottom: 25px;
    }


    /* =========================================
       FOOTER
       ========================================= */

    .footer {
        text-align: center;
        color: #8b748c;
        font-size: 12px;
        margin-top: 40px;
        padding: 15px;
    }


    /* =========================================
       SUCCESS / WARNING
       ========================================= */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🪷 MythoTales ✨</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">DISCOVER • VISUALIZE • UNDERSTAND</div>',
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "story" not in st.session_state:
    st.session_state.story = None

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0


# =========================================================
# NAVIGATION
# =========================================================

nav1, nav2, nav3 = st.columns(3)

with nav1:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"

with nav2:
    if st.button("🧠 Quiz", use_container_width=True):
        st.session_state.page = "Quiz"

with nav3:
    if st.button("🌍 Multiple Languages", use_container_width=True):
        st.session_state.page = "Languages"


st.markdown("---")


# =========================================================
# LANGUAGES
# =========================================================

LANGUAGES = [
    "English",
    "Telugu",
    "Hindi",
    "Tamil",
    "Kannada",
    "Malayalam",
    "Bengali",
    "Marathi"
]


# =========================================================
# GEMINI TEXT GENERATION
# FAST MODEL + MINIMAL THINKING
# =========================================================

def generate_text(prompt):

    last_error = None

    for attempt in range(3):

        try:

            interaction = client.interactions.create(
                model="gemini-3.5-flash-lite",
                input=prompt,
                generation_config={
                    "thinking_level": "minimal"
                }
            )

            result = interaction.output_text

            if result and result.strip():
                return result.strip()

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        except Exception as e:

            last_error = e
            error_text = str(e)

            temporary_error = (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
                or "timeout" in error_text.lower()
                or "timed out" in error_text.lower()
            )

            if temporary_error:

                if attempt < 2:
                    time.sleep(1.5 * (attempt + 1))
                    continue

            raise e

    raise RuntimeError(
        f"Gemini is temporarily unavailable.\n\n{last_error}"
    )


# =========================================================
# CLEAN GEMINI JSON RESPONSE
# =========================================================

def clean_json_response(raw):

    if not raw:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    raw = raw.strip()

    # Remove markdown code fences
    raw = re.sub(
        r"^```(?:json)?\s*",
        "",
        raw,
        flags=re.IGNORECASE
    )

    raw = re.sub(
        r"\s*```$",
        "",
        raw
    )

    raw = raw.strip()

    # Try direct JSON first
    try:
        return json.loads(raw)

    except json.JSONDecodeError:
        pass

    # Find JSON object inside response
    start = raw.find("{")
    end = raw.rfind("}")

    if start != -1 and end != -1:

        json_text = raw[start:end + 1]

        try:
            return json.loads(json_text)

        except json.JSONDecodeError:
            pass

    raise RuntimeError(
        "Gemini returned an invalid JSON response."
    )


# =========================================================
# CREATE MYTHOLOGY STORY
# =========================================================

def create_story(topic, language):

    prompt = f"""
Create a mythology story about the following topic:

{topic}

Write the complete story in:
{language}

Return ONLY valid JSON.
Do not use markdown.
Do not use code fences.
Do not include image prompts.
Do not include HTML.

Use exactly this structure:

{{
  "title": "Story title",
  "introduction": "Short introduction",
  "scenes": [
    {{
      "title": "Scene 1 title",
      "story": "Scene 1 story"
    }},
    {{
      "title": "Scene 2 title",
      "story": "Scene 2 story"
    }},
    {{
      "title": "Scene 3 title",
      "story": "Scene 3 story"
    }},
    {{
      "title": "Scene 4 title",
      "story": "Scene 4 story"
    }}
  ]
}}

Important rules:

1. Exactly 4 scenes.
2. Every scene must contain a title and story.
3. Keep each scene concise and meaningful.
4. Make the story engaging and easy to understand.
5. Respect traditional mythology.
6. Do not invent major facts when the mythology is well known.
7. Do not include anything outside the JSON.
"""

    raw = generate_text(prompt)

    return clean_json_response(raw)


# =========================================================
# CREATE QUIZ
# =========================================================

def create_quiz(topic, language):

    prompt = f"""
Create a mythology quiz about:

{topic}

Language:
{language}

Return ONLY valid JSON.
Do not use markdown.
Do not use code fences.

Use exactly this structure:

{{
  "questions": [
    {{
      "question": "Question",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Correct option",
      "explanation": "Short explanation"
    }}
  ]
}}

Rules:

1. Exactly 5 questions.
2. Exactly 4 options for every question.
3. Only one correct answer.
4. Questions must be related to the topic.
5. Use {language}.
6. Keep questions educational.
7. Keep explanations short.
8. Do not include anything outside the JSON.
"""

    raw = generate_text(prompt)

    return clean_json_response(raw)


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "Home":

    st.markdown(
        '<div class="section-title">Discover Mythological Stories</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-text">'
        'Enter any mythology, deity, epic, legend or question.'
        '</div>',
        unsafe_allow_html=True
    )


    # Centered input area
    left, center, right = st.columns([1, 2, 1])

    with center:

        topic = st.text_area(
            "✨ What would you like to explore?",
            placeholder="Example: Tell me the story of Lord Krishna",
            height=85,
            key="topic_input"
        )

        language = st.selectbox(
            "🌍 Select Language",
            LANGUAGES,
            index=0,
            key="home_language"
        )

        generate = st.button(
            "🪷 Generate My Story",
            use_container_width=True
        )


    # Generate story
    if generate:

        if not topic.strip():

            st.warning(
                "Please enter a mythology topic first."
            )

        else:

            with st.spinner(
                "✨ Creating your mythology story..."
            ):

                try:

                    story = create_story(
                        topic,
                        language
                    )

                    # Validate scenes
                    scenes = story.get("scenes", [])

                    if len(scenes) < 4:

                        st.error(
                            "The AI did not generate 4 scenes. Please try again."
                        )

                    else:

                        st.session_state.story = story

                except Exception as e:

                    st.error(
                        "Unable to generate the story."
                    )

                    st.code(str(e))


    # Display generated story
    if st.session_state.story:

        story = st.session_state.story

        st.markdown(
            '<div class="story-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="story-title">'
            f'🪷 {story.get("title", "Mythological Story")}'
            f'</div>',
            unsafe_allow_html=True
        )

        introduction = story.get(
            "introduction",
            ""
        )

        if introduction:

            st.markdown(
                f'<div class="scene-text">{introduction}</div>',
                unsafe_allow_html=True
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        # Scenes
        scenes = story.get("scenes", [])

        for index, scene in enumerate(scenes[:4]):

            scene_title = scene.get(
                "title",
                f"Scene {index + 1}"
            )

            scene_story = scene.get(
                "story",
                ""
            )

            st.markdown(
                f"### 🌸 Scene {index + 1}: {scene_title}"
            )

            st.write(scene_story)

            if index < 3:
                st.markdown("---")


# =========================================================
# QUIZ PAGE
# =========================================================

elif st.session_state.page == "Quiz":

    st.markdown(
        '<div class="section-title">🧠 Mythology Quiz</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-text">'
        'Test your knowledge of mythology.'
        '</div>',
        unsafe_allow_html=True
    )


    # Same width as Home input
    left, center, right = st.columns([1, 2, 1])

    with center:

        quiz_topic = st.text_input(
            "✨ Enter a mythology topic",
            placeholder="Example: Lord Ganesha",
            key="quiz_topic"
        )

        quiz_language = st.selectbox(
            "🌍 Quiz Language",
            LANGUAGES,
            key="quiz_language"
        )

        create_quiz_button = st.button(
            "🧠 Generate Quiz",
            use_container_width=True
        )


    # Generate quiz
    if create_quiz_button:

        if not quiz_topic.strip():

            st.warning(
                "Please enter a topic first."
            )

        else:

            with st.spinner(
                "✨ Creating your quiz..."
            ):

                try:

                    quiz = create_quiz(
                        quiz_topic,
                        quiz_language
                    )

                    questions = quiz.get(
                        "questions",
                        []
                    )

                    if len(questions) < 5:

                        st.error(
                            "The AI did not generate 5 questions. Please try again."
                        )

                    else:

                        st.session_state.quiz = quiz
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_score = 0

                except Exception as e:

                    st.error(
                        "Unable to generate quiz."
                    )

                    st.code(str(e))


    # Display quiz
    if st.session_state.quiz:

        quiz = st.session_state.quiz

        answers = {}

        left, center, right = st.columns([1, 2, 1])

        with center:

            for index, question in enumerate(
                quiz.get("questions", [])[:5]
            ):

                st.markdown(
                    '<div class="quiz-card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"**Q{index + 1}. "
                    f"{question.get('question', '')}**"
                )

                options = question.get(
                    "options",
                    []
                )

                answers[index] = st.radio(
                    "Choose your answer:",
                    options,
                    key=f"quiz_answer_{index}"
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


            submit_quiz = st.button(
                "✅ Submit Quiz",
                use_container_width=True
            )


        # Check answers
        if submit_quiz:

            score = 0

            for index, question in enumerate(
                quiz.get("questions", [])[:5]
            ):

                if (
                    answers.get(index)
                    == question.get("answer")
                ):
                    score += 1

            st.session_state.quiz_score = score
            st.session_state.quiz_submitted = True


        # Show result
        if st.session_state.get(
            "quiz_submitted",
            False
        ):

            score = st.session_state.quiz_score

            if score == 5:

                st.success(
                    "🎉 Excellent! Your Score: 5 / 5"
                )

                st.balloons()

            elif score >= 3:

                st.success(
                    f"👏 Good job! Your Score: {score} / 5"
                )

            else:

                st.info(
                    f"📚 Keep learning! Your Score: {score} / 5"
                )


            left, center, right = st.columns(
                [1, 2, 1]
            )

            with center:

                st.markdown(
                    "### 📖 Answers & Explanations"
                )

                for index, question in enumerate(
                    quiz.get("questions", [])[:5]
                ):

                    st.write(
                        f"**{index + 1}. "
                        f"Correct answer:** "
                        f"{question.get('answer', '')}"
                    )

                    st.write(
                        question.get(
                            "explanation",
                            ""
                        )
                    )

                    if index < 4:
                        st.markdown("---")


# =========================================================
# MULTIPLE LANGUAGES PAGE
# =========================================================

elif st.session_state.page == "Languages":

    st.markdown(
        '<div class="section-title">🌍 Multiple Languages</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-text">'
        'Explore mythology in your preferred language.'
        '</div>',
        unsafe_allow_html=True
    )


    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown(
            "### Available Languages"
        )

        for language in LANGUAGES:

            st.markdown(
                f"""
                <div class="story-card"
                     style="text-align:center;
                            padding:14px;
                            margin-top:10px;
                            margin-bottom:10px;">
                    <b>{language}</b>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="footer">'
    '🪷 MythoTales AI • Explore mythology through technology'
    '</div>',
    unsafe_allow_html=True
)