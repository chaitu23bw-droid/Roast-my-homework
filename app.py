import streamlit as st

# Configure page title and header
st.set_page_config(page_title="Roast My Homework", page_icon="🔥", layout="centered")
st.title("🔥 Roast My Homework!")
st.caption("The sarcastic study buddy that roasts your draft before your teacher does.")

# Input fields
subject = st.selectbox("Select Subject", ["Science", "English", "History / Social Studies"])
user_text = st.text_area("Paste your draft answer or essay below:", height=150)

# Submit button logic
if st.button("🔥 Roast & Review!"):
    if not user_text.strip():
        st.warning("Please paste some draft text first!")
    else:
        st.subheader("🔥 The Roast")
        text_lower = user_text.lower()
        word_count = len(user_text.split())

        # 1. Length Check
        if word_count < 10:
            st.error("⚠️ Length Check: This isn't an answer, it's a text message! Did you run out of ink on your keyboard?")
        elif word_count > 120:
            st.error("📜 Length Check: Wow, an entire novel! Are you trying to wear out the teacher's eyes?")
        else:
            st.success("✅ Length looking pretty good!")

        # 2. Topic & Keyword Specific Roasts
        if subject == "Science":
            if "archimedes" in text_lower or "density" in text_lower or "upthrust" in text_lower:
                st.warning("🧪 Science Vibe: Floating along fine, but where are Archimedes' actual calculations or buoyant force equations?")
            elif "photosynthesis" in text_lower or "plant" in text_lower:
                st.warning("🌱 Science Vibe: You mentioned plants, but you're missing key terms like chlorophyll, glucose, or light reactions!")
            else:
                st.info("🧪 Science Vibe: Needs more core scientific terms (e.g., cell, reaction, force, structure).")

        elif subject == "English":
            if "because" not in text_lower and "therefore" not in text_lower:
                st.warning("📖 English Vibe: Your sentences are jumping around! Add transition words like 'furthermore' or 'consequently'.")
            else:
                st.success("📖 English Vibe: Good sentence transitions used!")

        elif subject == "History / Social Studies":
            if not any(char.isdigit() for char in user_text):
                st.warning("🏛️ History Vibe: Zero dates or years? Are we talking about ancient history or yesterday at lunch?")
            else:
                st.success("🏛️ History Vibe: Nice inclusion of specific dates or figures!")

        # 3. Filler Word Check
        filler_words = ["stuff", "things", "basically", "so yeah"]
        if any(f in text_lower for f in filler_words):
            st.error("💬 Vocabulary: Words like 'stuff' or 'things' belong on the playground, not in an exam paper!")

        # Pre-Submission Checklist
        st.divider()
        st.subheader("📝 Pre-Submission Checklist")
        st.checkbox("Fixed generic words (e.g., 'stuff' ➔ 'buoyancy / light energy')")
        st.checkbox("Checked spelling & punctuation")
        st.checkbox("Included at least 3 subject-specific key terms")

        st.balloons()
