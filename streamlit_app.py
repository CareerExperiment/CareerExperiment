import streamlit as st
from transformers import pipeline

# Setup text generation pipeline (distilgpt2 for speed and no API needed)
@st.cache_resource(show_spinner=False)
def get_generator():
    return pipeline("text-generation", model="distilgpt2")

generator = get_generator()

st.set_page_config(page_title="💡 Career Exploration Assistant", page_icon="💡")

st.title("💡 Your Career Exploration Assistant")
st.write("Let's break down your career curiosity into simple, meaningful steps.")

# Step 1: Get career interest
career_interest = st.text_input("🎯 What career or role are you curious about?", placeholder="e.g. UX Designer, Data Analyst")

# Step 2: Identify biggest constraint
constraint = st.selectbox(
    "⛔ What's holding you back the most?",
    [
        "I don’t have time",
        "I’m scared or unsure",
        "I don’t know anyone in that field",
        "I don’t want to waste effort on the wrong thing"
    ]
)

# Step 3: Motivation & resources check - multi-select
motivations = st.multiselect(
    "🌟 What motivates you? (Select all that apply)",
    [
        "Learning new skills",
        "Connecting with people",
        "Making an impact",
        "Finding flexible work",
        "Earning more money",
        "Work-life balance"
    ]
)

resources = st.multiselect(
    "🔧 What resources do you have available? (Select all that apply)",
    [
        "Internet access",
        "Professional network",
        "Free time during evenings/weekends",
        "Financial buffer",
        "Mentor or coach"
    ]
)

submit = st.button("Generate My Low-Risk Career Experiments")

def create_prompt(career, constraint, motivations, resources):
    motivations_str = ", ".join(motivations) if motivations else "no specific motivations"
    resources_str = ", ".join(resources) if resources else "no particular resources"

    prompt = (
        f"You are a friendly and practical career coach AI.\n"
        f"The user is curious about the career: {career}.\n"
        f"They feel stuck because: \"{constraint}\".\n"
        f"Their main motivations are: {motivations_str}.\n"
        f"They currently have these resources: {resources_str}.\n"
        "Suggest 3 specific, simple experiments they can do in the next 7 days to explore this career path.\n"
        "- Each experiment should take 1-2 hours or less.\n"
        "- Low risk and non-intimidating.\n"
        "- Focused on learning or building connections.\n"
        "- Written clearly and supportively.\n"
        "Label them 1, 2, and 3, then end with a short encouragement message."
    )
    return prompt

if submit:
    if not career_interest.strip():
        st.warning("Please enter your career interest before submitting.")
    else:
        prompt = create_prompt(career_interest, constraint, motivations, resources)

        with st.spinner("Generating career experiments..."):
            # Use Hugging Face distilgpt2 generation (text-generation pipeline)
            # We limit output tokens to ~250 for response length
            output = generator(prompt, max_length=250, do_sample=True, temperature=0.8, num_return_sequences=1)
            generated_text = output[0]["generated_text"]

        # Show result
        st.markdown("### Your Low-Risk Career Experiments:")
        # Display generated text removing the prompt prefix (optional)
        # Here just show whole text for transparency
        st.write(generated_text)

else:
    st.info("Fill in your career interest and select options, then press the button to get your personalized experiments!")
