import streamlit as st

# Configure page layout
st.set_page_config(page_title="Roast My Homework", page_icon="🤖", layout="centered")

st.title("🤖 Roast My Homework!")
st.caption("The sarcastic study buddy that roasts your draft before your teacher does.")

# Subject Topics Database for 8th-Grade Level
DATABASE = {
    "Science: Photosynthesis": {
        "triggers": ["photosynthesis", "plant", "sun", "sunlight", "leaf", "chlorophyll"],
        "roast": "You explained Photosynthesis like a plant written by a potato! Photosynthetic organisms don't just 'drink sun stuff'—they run a whole cellular factory.",
        "keywords": ["Chlorophyll", "Glucose", "Carbon Dioxide", "Oxygen", "Light Energy"],
        "model_answer": "Photosynthesis is the chemical process where plants use chlorophyll to absorb light energy, converting carbon dioxide and water into glucose and oxygen."
    },
    "Science: Archimedes' Principle & Density": {
        "triggers": ["archimedes", "density", "upthrust", "buoyant", "floating", "water", "bathtub"],
        "roast": "Floating along without a care in the world! You forgot the actual physics—Archimedes didn't run around naked yelling 'Eureka' just for you to skip the equations.",
        "keywords": ["Upthrust / Buoyant Force", "Displaced Fluid", "Volume", "Density ($\rho = m/V$)", "Equilibrium"],
        "model_answer": "Archimedes' principle states that any body completely or partially submerged in a fluid experience an upward buoyant force equal to the weight of the fluid displaced by the body."
    },
    "History: Causes of World War I": {
        "triggers": ["war", "ww1", "franz", "ferdinand", "assassination", "alliance", "history"],
        "roast": "Zero dates, zero treaties! Are we discussing World War I or drama in the cafeteria yesterday?",
        "keywords": ["M.A.I.N. (Militarism, Alliances, Imperialism, Nationalism)", "Archduke Franz Ferdinand", "1914", "Triple Entente", "Central Powers"],
        "model_answer": "The outbreak of World War I in 1914 was triggered by the assassination of Archduke Franz Ferdinand, stemming from long-term tensions in Militarism, Alliances, Imperialism, and Nationalism (M.A.I.N.)."
    },
    "English: Essay Analysis & Structure": {
        "triggers": ["essay", "author", "character", "book", "story", "theme", "metaphor"],
        "roast": "Your sentences are jumping around faster than a squirrel on caffeine! Where are your evidence quotes and transition words?",
        "keywords": ["Thesis Statement", "Textual Evidence", "Tone", "Metaphor/Simile", "Furthermore / Consequently"],
        "model_answer": "The author effectively highlights the central theme through vivid metaphors and character development, supporting the thesis statement with concrete textual evidence."
    }
}

# App Inputs
subject_choice = st.selectbox("📌 Select Subject & Topic", list(DATABASE.keys()))
user_text = st.text_area("✍️ Paste your draft answer or essay below:", height=140, placeholder="Type your answer draft here...")

# Process Button
if st.button("🔥 Roast & Review!"):
    if not user_text.strip():
        st.warning("Please type or paste an answer first!")
    else:
        topic_data = DATABASE[subject_choice]
        text_lower = user_text.lower()
        word_count = len(user_text.split())

        st.markdown("---")
        
        # Section 1: The Dramatic Roast
        st.subheader("🎭 1. The Roast")
        
        if word_count < 8:
            st.error("⚠️ *Roast:* This isn't an answer, it's a text message! Did you run out of ink on your keyboard?")
        else:
            st.error(f"🔥 *Roast:* {topic_data['roast']}")

        # Section 2: Missing Keywords Checklist
        st.subheader("🎯 2. Missing Key Terms (8th-Grade Rubric)")
        
        found_keywords = []
        missing_keywords = []

        for kw in topic_data["keywords"]:
            # Clean keyword for checking
            clean_kw = kw.split("(")[0].strip().lower()
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
                st.write("🎉 *Awesome! You included all key terms!*")

        # Section 3: Suggested Model Answer
        st.subheader("💡 3. Suggested Model Answer")
        st.info(f"**How to upgrade for full marks:**\n\n\"{topic_data['model_answer']}\"")

        st.balloons()

