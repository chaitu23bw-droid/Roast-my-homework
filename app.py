
import streamlit as st
import json
import re
from google import genai
from google.genai import types

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Revision & Flashcard Generator",
    page_icon="📚",
    layout="wide"
)

# --- App Header ---
st.title("📚 AI Study Buddy")
st.subheader("Turn your rough notes into quizzes and smart flashcards in seconds!")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    st.markdown("[Get a Gemini API Key](https://aistudio.google.com/)")
    
    st.markdown("---")
    num_questions = st.slider("Number of Quiz Questions", 3, 10, 5)
    num_cards = st.slider("Number of Flashcards", 3, 10, 5)

# --- Helper Functions ---
def clean_json_response(raw_text):
    """Strips markdown code blocks to safely parse JSON."""
    cleaned = re.sub(r"```json\n|\n```|```", "", raw_text).strip()
    return cleaned

def generate_study_material(notes_text, api_key, num_q, num_fc):
    """Calls Gemini 2.5 Flash to generate structured JSON for quizzes and flashcards."""
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert AI tutor. Analyze the following notes and generate structured study materials.
    
    NOTES:
    {notes_text}
    
    Task 1: Generate {num_q} multiple-choice questions (MCQs) for a revision test.
    Task 2: Generate {num_fc} flashcards explaining key concepts simply.
    
    Return the response ONLY as a strict JSON object with the following schema:
    {{
        "quiz": [
            {{
                "id": 1,
                "question": "Question text",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": "Option A",
                "explanation": "Brief explanation why this is correct."
            }}
        ],
        "flashcards": [
            {{
                "concept": "Concept/Term Name",
                "explanation": "Clear, concise explanation based on notes."
            }}
        ]
    }}
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.3
        )
    )
    
    return json.loads(clean_json_response(response.text))

# --- Input Area ---
st.markdown("### 📝 Provide Your Notes")
tab_text, tab_file = st.tabs(["Paste Text", "Upload File"])

user_notes = ""

with tab_text:
    user_notes = st.text_area("Paste your study notes or chapter summaries here:", height=200)

with tab_file:
    uploaded_file = st.file_uploader("Upload a text file (.txt)", type=["txt"])
    if uploaded_file is not None:
        user_notes = uploaded_file.read().decode("utf-8")

# --- Generation Action ---
if st.button("🚀 Generate Revision Kit", type="primary"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not user_notes.strip():
        st.warning("Please enter or upload some notes first!")
    else:
        with st.spinner("Analyzing notes and generating study tools..."):
            try:
                data = generate_study_material(user_notes, api_key, num_questions, num_cards)
                st.session_state["study_data"] = data
                st.session_state["user_answers"] = {}
                st.session_state["submitted"] = False
                st.success("Study materials generated!")
            except Exception as e:
                st.error(f"Failed to generate material. Error: {str(e)}")

# --- Output Display ---
if "study_data" in st.session_state:
    data = st.session_state["study_data"]
    
    main_tab1, main_tab2 = st.tabs(["✍️ Revision Quiz", "🎴 Concept Flashcards"])
    
    # --- Tab 1: Quiz ---
    with main_tab1:
        st.header("Test Your Knowledge")
        quiz_data = data.get("quiz", [])
        
        with st.form("quiz_form"):
            for idx, q in enumerate(quiz_data):
                st.markdown(f"**Q{idx + 1}: {q['question']}**")
                user_choice = st.radio(
                    f"Select answer for Q{idx+1}:",
                    q["options"],
                    key=f"q_{idx}",
                    index=None
                )
                st.session_state["user_answers"][idx] = user_choice
                st.markdown("---")
            
            submit_quiz = st.form_submit_button("Submit Quiz")
            if submit_quiz:
                st.session_state["submitted"] = True

        if st.session_state.get("submitted", False):
            score = 0
            st.header("📊 Results")
            for idx, q in enumerate(quiz_data):
                user_ans = st.session_state["user_answers"].get(idx)
                correct_ans = q["answer"]
                
                if user_ans == correct_ans:
                    score += 1
                    st.success(f"**Q{idx + 1}: Correct!** ({user_ans})")
                else:
                    st.error(f"**Q{idx + 1}: Incorrect.** Your answer: `{user_ans}` | Correct: `{correct_ans}`")
                
                st.info(f"💡 *Explanation:* {q['explanation']}")
            
            st.metric("Final Score", f"{score} / {len(quiz_data)}")

    # --- Tab 2: Flashcards ---
    with main_tab2:
        st.header("Flashcard Explanations")
        flashcards = data.get("flashcards", [])
        
        col1, col2 = st.columns(2)
        for idx, fc in enumerate(flashcards):
            target_col = col1 if idx % 2 == 0 else col2
            with target_col:
                with st.expander(f"📌 **{fc['concept']}**"):
                    st.write(fc["explanation"])
