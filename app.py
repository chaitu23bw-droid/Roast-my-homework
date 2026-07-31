import streamlit as st

# Configure page layout
st.set_page_config(page_title="Roast My Homework", page_icon="🤖", layout="centered")

st.title("🤖 Roast My Homework!")
st.caption("The sarcastic study buddy that roasts your draft before your teacher does.")

# ---------------------------------------------------------
# Knowledge Base for Topics, Keywords, Roasts, & Solutions
# ---------------------------------------------------------
TOPICS_DATABASE = [
    {
        "subject": "Science",
        "topic_name": "Photosynthesis",
        "triggers": ["photosynthesis", "plant", "sun", "sunlight", "chlorophyll", "leaf", "leaves"],
        "roast": "You explained Photosynthesis like a plant written by a potato! Photosynthetic organisms don't just 'drink sun stuff'—they run a complex cellular factory.",
        "keywords": ["Chlorophyll", "Glucose", "Carbon Dioxide", "Oxygen", "Light Energy"],
        "model_answer": "Photosynthesis is the chemical process where plants use chlorophyll to absorb light energy, converting carbon dioxide and water into glucose and oxygen."
    },
    {
        "subject": "Science",
        "topic_name": "Archimedes' Principle & Density",
        "triggers": ["archimedes", "density", "upthrust", "buoyant", "buoyancy", "floating", "displacement", "water displaced"],
        "roast": "Floating along without a care in the world! Archimedes didn't jump out of a bathtub yelling 'Eureka' just for you to skip the actual physics and fluid equations.",
        "keywords": ["Upthrust / Buoyant Force", "Displaced Fluid", "Volume", "Density", "Equilibrium"],
        "model_answer": "Archimedes' principle states that any body completely or partially submerged in a fluid experiences an upward buoyant force equal to the weight of the fluid displaced by the body."
    },
    {
        "subject": "Science",
        "topic_name": "Cell Biology",
        "triggers": ["cell", "mitochondria", "nucleus", "organelle", "dna", "cytoplasm"],
        "roast": "Calling the mitochondrion 'the powerhouse of the cell' is a middle-school meme, not an 8th-grade biology answer!",
        "keywords": ["Mitochondria", "ATP / Energy", "Nucleus", "Cell Membrane", "Cytoplasm"],
        "model_answer": "Cells are the basic structural units of life containing specialized organelles, such as the nucleus for genetic control and mitochondria for cellular respiration and energy production."
    },
    {
        "subject": "History",
        "topic_name": "World War I",
        "triggers": ["war", "ww1", "wwi", "franz", "ferdinand", "alliance", "assassination", "trench"],
        "roast": "Zero dates, zero treaties! Are we discussing World War I or drama in the school cafeteria yesterday?",
        "keywords": ["M.A.I.N. (Militarism, Alliances, Imperialism, Nationalism)", "Archduke Franz Ferdinand", "1914", "Triple Entente", "Central Powers"],
        "model_answer": "The outbreak of World War I in 1914 was triggered by the assassination of Archduke Franz Ferdinand, stemming from long-term tensions in Militarism, Alliances, Imperialism, and Nationalism (M.A.I.N.)."
    },
    {
        "subject": "Math",
        "topic_name": "Pythagorean Theorem & Geometry",
        "triggers": ["pythagoras", "pythagorean", "triangle", "hypotenuse", "angle", "theorem", "right angle"],
        "roast": "You're throwing around numbers like confetti! A geometry proof needs clear step-by-step logic, labelled variables, and the correct theorem.",
        "keywords": ["Right-angled Triangle", "Hypotenuse ($c$)", "$a^2 + b^2 = c^2$", "Legs ($a, b$)"],
        "model_answer": "In any right-angled triangle, the square of the length of the hypotenuse is equal to the sum of the squares of the lengths of the other two sides ($a^2 + b^2 = c^2$)."
    },
    {
        "subject": "English",
        "topic_name": "Essay Structure & Literary Analysis",
        "triggers": ["essay", "author", "character", "book", "theme", "metaphor", "story", "novel", "similes"],
        "roast": "Your ideas are jumping around faster than a squirrel on caffeine! Where is your thesis statement, quote evidence, or transition words?",
        "keywords": ["Thesis Statement", "Textual Evidence", "Tone", "Metaphor/Simile", "Furthermore / Consequently"],
        "model_answer": "The author effectively highlights the central theme through vivid metaphors and character development, supporting the thesis statement with concrete textual evidence."
    }
]

# Fallback generic outputs if no specific triggers match
GENERIC_FALLBACKS = {
    "Science": {
        "topic_name": "General Science Draft",
        "roast": "This reads like a sci-fi fiction draft! You need actual scientific terms, controlled variables, and proper cause-and-effect explanations.",
        "keywords": ["Hypothesis", "Variables (Independent/Dependent)", "Scientific Vocabulary", "Observation / Empirical Evidence"],
        "model_answer": "State the scientific concept using precise terminology, clearly defining cause-and-effect relationships and measurable parameters."
    },
    "History": {
        "topic_name": "General History Draft",
        "roast": "Sounds like a movie review! History answers require specific dates, historical figures, and clear cause-and-effect arguments.",
        "keywords": ["Historical Context", "Primary Sources", "Timeline / Dates", "Key Figures", "Socio-political Impact"],
        "model_answer": "A complete history response connects historical cause and effect using verified dates, key named individuals, and relevant socio-political context."
    },
    "Math": {
        "topic_name": "General Math Draft",
        "roast": "Where are the steps? Giving an answer without showing formula substitution or step-by-step working is an instant way to lose marks!",
        "keywords": ["Formula", "Variable Substitution", "Units of Measurement", "Step-by-Step Working", "Final Value"],
        "model_answer": "State the governing formula, substitute the given values step-by-step, show full arithmetic working, and specify correct units of measurement."
    },
    "English": {
        "topic_name": "General Essay Draft",
        "roast": "This reads like a casual text message! You need formal academic language, stronger literary terms, and structured paragraphs.",
        "keywords": ["Thesis Statement", "Paragraph Cohesion", "Textual Evidence", "Literary Devices", "Formal Tone"],
        "model_answer": "Structure your essay with a clear thesis statement in the introduction, body paragraphs backed by textual evidence, and transition words to connect arguments."
    }
}

# ---------------------------------------------------------
# User Interface Inputs
# ---------------------------------------------------------

# 1. Subject Selector
selected_subject = st.selectbox("📌 Select Subject Category", ["Auto-Detect Subject", "Science", "Math", "History", "English"])

# 2. Input Box
user_text = st.text_area("✍️ Paste your draft answer or essay below:", height=150, placeholder="Paste or type any draft sentence here...")

# 3. Process Button
if st.button("🔥 Roast & Review!"):
    if not user_text.strip():
        st.warning("Please type or paste an answer first!")
    else:
        text_lower = user_text.lower()
        word_count = len(user_text.split())

        # Step A: Identify/Detect Topic and Subject
        matched_entry = None

        # Search database for matching keyword triggers
        for entry in TOPICS_DATABASE:
            if selected_subject != "Auto-Detect Subject" and entry["subject"] != selected_subject:
                continue
            if any(trigger in text_lower for trigger in entry["triggers"]):
                matched_entry = entry
                break

        # If no specific topic matched, fall back to selected subject or default to Science
        if not matched_entry:
            fallback_subject = selected_subject if selected_subject != "Auto-Detect Subject" else "Science"
            matched_entry = GENERIC_FALLBACKS[fallback_subject]
            matched_entry["subject"] = fallback_subject

        st.markdown("---")

        # Display Detected Metadata
        st.caption(f"**Detected Category:** {matched_entry['subject']} $\rightarrow$ *{matched_entry['topic_name']}*")

        # --- Section 1: The Dramatic Roast ---
        st.subheader("🎭 1. The Roast")
        if word_count < 8:
            st.error("⚠️ *Roast:* This isn't an answer, it's a text message! Did you run out of ink on your keyboard?")
        else:
            st.error(f"🔥 *Roast:* {matched_entry['roast']}")

        # --- Section 2: Key Terms Check ---
        st.subheader("🎯 2. Missing Key Terms (8th-Grade Rubric)")
        
        found_keywords = []
        missing_keywords = []

        for kw in matched_entry["keywords"]:
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
                st.write("*None detected yet!*")

        with col2:
            st.markdown("**❌ Missing Terms Needed:**")
            if missing_keywords:
                for mk in missing_keywords:
                    st.write(f"- **{mk}**")
            else:
                st.write("🎉 *Awesome! You included all recommended key terms!*")

        # --- Section 3: Model Suggested Answer ---
        st.subheader("💡 3. Suggested Model Answer")
        st.info(f"**How to upgrade this draft for full marks:**\n\n\"{matched_entry['model_answer']}\"")

        st.balloons()
