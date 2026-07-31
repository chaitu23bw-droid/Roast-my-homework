import streamlit as st

# Configure page layout
st.set_page_config(page_title="Roast My Homework", page_icon="🤖", layout="centered")

st.title("🤖 Roast My Homework!")
st.caption("The sarcastic study buddy that roasts your draft before your teacher does.")

# Subject Knowledge Base
SUBJECT_DATA = {
    "Science": [
        {
            "triggers": ["photosynthesis", "plant", "sun", "sunlight", "chlorophyll", "leaf"],
            "roast": "You explained Photosynthesis like a plant written by a potato! Photosynthetic organisms don't just 'drink sun stuff'—they run a complex cellular factory.",
            "keywords": ["Chlorophyll", "Glucose", "Carbon Dioxide", "Oxygen", "Light Energy"],
            "model_answer": "Photosynthesis is the chemical process where plants use chlorophyll to absorb light energy, converting carbon dioxide and water into glucose and oxygen."
        },
        {
            "triggers": ["archimedes", "density", "upthrust", "buoyant", "floating", "water", "displacement"],
            "roast": "Floating along without a care in the world! Archimedes didn't jump out of a bathtub yelling 'Eureka' just for you to skip the actual physics and equations.",
            "keywords": ["Upthrust / Buoyant Force", "Displaced Fluid", "Volume", "Density", "Equilibrium"],
            "model_answer": "Archimedes' principle states that any body completely or partially submerged in a fluid experiences an upward buoyant force equal to the weight of the fluid displaced by the body."
        },
        {
            "triggers": ["cell", "mitochon", "nucleus", "organelle", "dna"],
            "roast": "Calling the mitochondrion 'the powerhouse of the cell' is a middle-school meme, not an 8th-grade biology answer!",
            "keywords": ["Mitochondria", "ATP / Energy", "Nucleus", "Cell Membrane", "Cytoplasm"],
            "model_answer": "Cells are the basic structural units of life containing organelles like the nucleus for genetic control and mitochondria for generating cellular energy."
        }
    ],
    "History": [
        {
            "triggers": ["war", "ww1", "wwi", "franz", "ferdinand", "alliance", "assassination"],
            "roast": "Zero dates, zero treaties! Are we discussing World War I or drama in the school cafeteria yesterday?",
            "keywords": ["M.A.I.N. (Militarism, Alliances, Imperialism, Nationalism)", "Archduke Franz Ferdinand", "1914", "Triple Entente", "Central Powers"],
            "model_answer": "The outbreak of World War I in 1914 was triggered by the assassination of Archduke Franz Ferdinand, stemming from long-term tensions in Militarism, Alliances, Imperialism, and Nationalism."
        }
    ],
    "English": [
        {
            "triggers": ["essay", "author", "character", "book", "theme", "metaphor", "story"],
            "roast": "Your ideas are jumping around faster than a squirrel on caffeine! Where is your thesis statement, quote evidence, or transition words?",
            "keywords": ["Thesis Statement", "Textual Evidence", "Tone", "Metaphor/Simile", "Furthermore / Consequently"],
            "model_answer": "The author effectively highlights the central theme through vivid metaphors and character development, supporting the thesis statement with concrete textual evidence."
        }
    ],
    "Math": [
        {
            "triggers": ["pythagoras", "triangle", "hypotenuse", "angle", "theorem"],
            "roast": "You're throwing around numbers like confetti! A geometry proof needs clear step-by-step logic and labelled variables.",
            "keywords": ["Right-angled Triangle", "Hypotenuse ($c$)", "$a^2 + b^2 = c^2$", "Legs ($a, b$)"],
            "model_answer": "In any right-angled triangle, the square of the length of the hypotenuse is equal to the sum of the squares of the lengths of the other two sides ($a^2 + b^2 = c^2$)."
        }
    ]
}

# General Fallback Roasts by Subject (Used if no specific topic triggers match)
FALLBACK_DATA = {
    "Science": {
        "roast": "You wrote this like a fantasy novel! Where is the core scientific vocabulary, variables, or chemical process?",
        "keywords": ["Hypothesis", "Independent Variable", "Dependent Variable", "Scientific Vocabulary", "Observation"],
        "model_answer": "Ensure your answer clearly states the scientific concept using precise terminology, cause-and-effect structure, and measurable outcomes."
    },
    "History": {
        "roast": "Sounds like an opinion piece! History requires specific dates, key historical figures, and clear cause-and-effect arguments.",
        "keywords": ["Historical Context", "Primary Source", "Timeline / Dates", "Key Figures", "Socio-political Impact"],
        "model_answer": "A strong history response connects cause and effect using specific dates, named historical figures, and relevant context."
    },
    "English": {
        "roast": "This reads like a casual text message! You need stronger literary terms and clear sentence transitions.",
        "keywords": ["Analysis", "Literary Devices", "Textual Evidence", "Sentence Structure", "Cohesion"],
        "model_answer": "Structure your essay response with a clear introduction, supporting evidence from the text, and transition words to connect arguments."
    },
    "Math": {
        "roast": "Where are the steps? Giving an answer without showing formula substitution is an instant way to lose marks!",
        "keywords": ["Formula", "Substitution", "Units of Measurement", "Step-by-Step Logic", "Final Value"],
        "model_answer": "State the governing formula, substitute the given values clearly, show step-by-step working, and include appropriate units."
    }
}

# --- App Interface ---

# 1. Subject Selection
selected_subject = st.selectbox("📌 Select Subject", list(SUBJECT_DATA.keys()))

# 2. User Input Area
user_text = st.text_area("✍️ Paste your draft answer or essay below:", height=140, placeholder="Type your answer draft here...")

# 3. Processing Logic
if st.button("🔥 Roast & Review!"):
    if not user_text.strip():
        st.warning("Please type or paste an answer first!")
    else:
        text_lower = user_text.lower()
        word_count = len(user_text.split())

        # Match specific topic within the selected subject
        matched_topic = None
        for topic in SUBJECT_DATA[selected_subject]:
            if any(trigger in text_lower for trigger in topic["triggers"]):
                matched_topic = topic
                break
        
        # Use fallback if no specific keywords match
        if not matched_topic:
            matched_topic = FALLBACK_DATA[selected_subject]

        st.markdown("---")

        # --- Section 1: The Roast ---
        st.subheader("🎭 1. The Roast")
        if word_count < 8:
            st.error("⚠️ *Roast:* This isn't an answer, it's a text message! Did you run out of ink on your keyboard?")
        else:
            st.error(f"🔥 *Roast:* {matched_topic['roast']}")

        # --- Section 2: Keywords Check ---
        st.subheader("🎯 2. Keyword Check (8th-Grade Rubric)")
        
        found_keywords = []
        missing_keywords = []

        for kw in matched_topic["keywords"]:
            clean_kw = kw.split("(")[0].replace("$", "").strip().lower()
            if clean_kw in text_lower:
                found_keywords.append(kw)
            else:
                missing_keywords.append(kw)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ Included Terms:**")
            if found_keywords:
                for fk in found_keywords:
                    st.write(f"- {fk}")
            else:
                st.write("*None detected!*")

        with col2:
            st.markdown("**❌ Missing Terms Needed:**")
            if missing_keywords:
                for mk in missing_keywords:
                    st.write(f"- **{mk}**")
            else:
                st.write("🎉 *Awesome! You included all recommended key terms!*")

        # --- Section 3: Suggested Correct Answer ---
        st.subheader("💡 3. Suggested Model Answer")
        st.info(f"**How to rewrite for full marks:**\n\n\"{matched_topic['model_answer']}\"")

        st.balloons()
