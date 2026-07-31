# Import streamlit for web UI and time for animation delays
import streamlit as st
import time

# Configure page title as 'Roast My Homework' with fire emoji and centered layout
st.set_page_config(page_title="Roast My Homework", page_icon="🔥", layout="centered")

# Set app header and subheader
st.title("🔥 Roast My Homework!")
st.caption("The sarcastic study buddy that roasts your draft before your teacher does.")

# Create a dropdown for selecting subjects: Science, English, Social Studies
subject = st.selectbox("Select Subject:", ["Science", "English", "Social Studies / History"])

# Create a text area for students to paste their homework draft
user_text = st.text_area(
    "Paste your draft answer or essay below:", 
    height=150, 
    placeholder="e.g., Photosynthesis is when plants take stuff from the sun..."
)

# Create a submit button called 'Roast & Review!'
if st.button("🔥 Roast & Review!"):
    # Check if user input is empty
    if not user_text.strip():
        st.warning("Please paste some draft text first!")
    else:
        # Show a spinner with 'Analyzing your homework for maximum drama...'
        with st.spinner("Analyzing your homework for maximum drama..."):
            time.sleep(1)
        
        # Calculate word count
        word_count = len(user_text.split())
        roasts = []
        feedback = []

        # Rule 1: Check length (if < 15 words add short roast; if > 120 words add long roast)
        if word_count < 15:
            roasts.append("⚠️ **Length Check:** This isn't an answer, it's a text message! Did you run out of ink on your keyboard?")
            feedback.append("• **Expand your idea:** 8th-grade answers usually need at least 3-4 full sentences with key terms.")
        elif word_count > 120:
            roasts.append("📜 **Length Check:** Wow, an entire novel! Are you trying to wear out the teacher's eyes?")
            feedback.append("• **Be concise:** Break giant walls of text into bullet points or clear paragraphs.")

        # Rule 2: Check for subject keywords
        text_lower = user_text.lower()
        if subject == "Science":
            science_keywords = ["energy", "process", "cell", "reaction", "system", "force", "structure", "glucose", "light"]
            found = [kw for kw in science_keywords if kw in text_lower]
            if len(found) < 2:
                roasts.append("🧪 **Science Vibe:** You explained this like a plant written by a potato! Where are the actual scientific terms?")
                feedback.append("• **Add Key Terms:** Include core scientific vocabulary (e.g., *chlorophyll, glucose, chemical reaction, cell wall*).")
            else:
                roasts.append("🧪 **Science Vibe:** Okay, you dropped a few smart words... but don't get arrogant yet!")

        elif subject == "English":
            if "because" not in text_lower and "therefore" not in text_lower:
                roasts.append("📖 **Grammar/Flow:** Your sentences are jumping around faster than a squirrel on caffeine!")
                feedback.append("• **Use Connectors:** Add transition words like *furthermore, because, consequently,* or *for instance*.")

        elif subject == "Social Studies / History":
            if not any(char.isdigit() for char in user_text):
                roasts.append("🏛️ **History Vibe:** Zero dates or years? Are we talking about ancient history or yesterday at lunch?")
                feedback.append("• **Add Specifics:** Mention specific dates, historical figures, or event names.")

        # Rule 3: Check for informal filler words ('stuff', 'things', 'basically')
        filler_words = ["stuff", "things", "like", "basically", "so yeah"]
        if any(f in text_lower for f in filler_words):
            roasts.append("💬 **Vocabulary:** Words like *'stuff'* belong in a playground, not an exam paper!")
            feedback.append("• **Upgrade Vocabulary:** Replace weak words with formal academic vocabulary.")

        # Display roasts in error red boxes and feedback in success green boxes
        st.divider()
        st.subheader("🔥 The Roast")
        for r in roasts:
            st.error(r)
            
        st.subheader("💡 Actual Useful Advice (To get 100%)")
        for f in feedback:
            st.success(f)

        # Show interactive checklist checkboxes and celebration balloons animation
        st.subheader("📝 Pre-Submission Checklist")
        st.checkbox("Fixed generic words (e.g., 'stuff' -> 'light energy')")
        st.checkbox("Checked spelling & punctuation")
        st.checkbox("Included at least 3 subject key terms")

        st.balloons()
