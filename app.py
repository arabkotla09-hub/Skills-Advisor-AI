import streamlit as st
from huggingface_hub import InferenceClient

# Add your token here
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token="YOUR_HF_TOKEN"
)

st.set_page_config(page_title="Skill Advisor AI")

st.title("🚀 Skill Advisor AI")
st.write("Enter any skill or course to get complete guidance")

skill = st.text_input("Enter Skill / Course Name")

def generate_response(skill):
    prompt = f"""
    Analyze the skill: {skill}

    Give structured output:

    1. Roadmap (step-by-step learning path)
    2. Scope (Pakistan + Global)
    3. Best Platforms/Courses
    4. Career Opportunities
    5. Drawbacks
    6. Who should learn this
    7. Who should avoid this
    """

    response = client.text_generation(
        prompt,
        max_new_tokens=500
    )
    return response

if st.button("Generate"):
    if skill:
        with st.spinner("Analyzing..."):
            result = generate_response(skill)
            st.write(result)
    else:
        st.warning("Please enter a skill")