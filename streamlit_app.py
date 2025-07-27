import streamlit as st
import openai
import os

# Load your API key from environment variable or directly (for testing only)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Your First Career Experiment", page_icon="💡")

st.title("💡 Your First Career Experiment")
st.subheader("Break the ice with small, low-risk steps toward a new career.")

career_interest = st.text_input("🎯 What career or role are you curious about?", placeholder="e.g. UX Designer, Data Analyst, Sustainability Consultant")

constraint = st.selectbox(
    "⛔ What's holding you back the most?",
    [
        "I don’t have time",
        "I’m scared or unsure",
        "I don’t know anyone in that field",
        "I don’t want to waste effort on the wrong thing"
    ]
)

submit = st.button("Generate My Experiments")

if submit and career_interest:
    with st.spinner("Generating ideas..."):

        prompt = f"""
        You are a friendly and practical AI coach. The user wants to explore a career in {career_interest}.

        They feel stuck because: "{constraint}"

        Suggest 3 specific, low-effort experiments they can try in the next 7 days to explore this path.

        Each experiment should be:
        - Doable in under 1–2 hours
        - Low-risk and non-intimidating
        - Focused on learning or building connections
        - Written in a clear, supportive tone

        Label them 1, 2, 3. End with a short encouragement message.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=500,
            )
            result = response.choices[0].message.content
            st.markdown(result)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
else:
    st.info("Fill in your interest and press the button to get ideas!")

