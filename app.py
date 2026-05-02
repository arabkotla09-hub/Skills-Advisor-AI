import streamlit as st
import os
from huggingface_hub import InferenceClient

# Secure token (ensure this is set in your environment variables)
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize the client
# The model and provider now require the conversational/chat interface
# Change from v0.2 to v0.3 (or use Llama-3)
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.3", 
    token=HF_TOKEN
)
# Page config
st.set_page_config(page_title="Skill Advisor AI", page_icon="🚀", layout="centered")

# Title
st.title("🚀 Skill Advisor AI")
st.markdown("Get a **complete roadmap + career guidance** for any skill")

# Input
skill = st.text_input("🔍 Enter Skill / Course Name", placeholder="e.g. Cyber Security, Python, Graphic Design")

# Prompt Template
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

# Fixed generate function using chat_completion
@st.cache_data(show_spinner=False)
def generate_response(skill):
    try:
        # Switching to chat_completion fixes the "Supported task: conversational" error
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a professional career advisor with deep knowledge of the Pakistani and international job markets."},
                {"role": "user", "content": build_prompt(skill)}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        # Extracting the content from the response object
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Button Logic
if st.button("🚀 Generate Advice"):
    if skill.strip():
        with st.spinner(f"Analyzing {skill}..."):
            result = generate_response(skill)
            st.markdown(result)
    else:
        st.warning("⚠️ Please enter a skill")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Hugging Face")
