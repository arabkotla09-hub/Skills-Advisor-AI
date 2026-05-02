import streamlit as st
import os
from huggingface_hub import InferenceClient

# Secure token (use environment variable)
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=HF_TOKEN
)

# Page config
st.set_page_config(page_title="Skill Advisor AI", page_icon="🚀", layout="centered")

# Title
st.title("🚀 Skill Advisor AI")
st.markdown("Get a **complete roadmap + career guidance** for any skill")

# Input
skill = st.text_input("🔍 Enter Skill / Course Name")

# Improved prompt
def build_prompt(skill):
    return f"""
You are an expert career advisor.

Analyze the skill: "{skill}"

Give a clean, well-structured answer with headings:

### 📍 Roadmap
(step-by-step learning path)

### 🌍 Scope
(Pakistan + Global demand)

### 🎓 Best Platforms/Courses
(include real platforms like Coursera, Udemy, YouTube)

### 💼 Career Opportunities

### ⚠️ Drawbacks

### 👤 Who should learn this

### 🚫 Who should avoid this

Keep it practical, honest, and beginner-friendly.
"""

# Cache response (faster UX)
@st.cache_data(show_spinner=False)
def generate_response(skill):
    try:
        response = client.text_generation(
            build_prompt(skill),
            max_new_tokens=700,
            temperature=0.7
        )
        return response
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Button
if st.button("🚀 Generate Advice"):
    if skill.strip():
        with st.spinner("Analyzing skill..."):
            result = generate_response(skill)
            st.markdown(result)
    else:
        st.warning("⚠️ Please enter a skill")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Hugging Face")
