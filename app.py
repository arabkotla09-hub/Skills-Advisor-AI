import streamlit as st
import os
from huggingface_hub import InferenceClient

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Skill Advisor AI", page_icon="🚀")

# Load token safely
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("❌ Hugging Face token not found. Please set HF_TOKEN in environment variables.")
    st.stop()

# Initialize client
client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",  # More stable than Mistral sometimes
    token=HF_TOKEN
)

# -------------------------
# UI
# -------------------------
st.title("🚀 Skill Advisor AI")
st.markdown("Get a **complete roadmap + career guidance** for any skill")

skill = st.text_input(
    "🔍 Enter Skill / Course Name",
    placeholder="e.g. Cyber Security, Python, Graphic Design"
)

# -------------------------
# PROMPT
# -------------------------
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

# -------------------------
# GENERATE RESPONSE
# -------------------------
def generate_response(skill):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional career advisor."},
                {"role": "user", "content": build_prompt(skill)}
            ],
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"

# -------------------------
# BUTTON
# -------------------------
if st.button("🚀 Generate Advice"):
    if skill.strip():
        with st.spinner(f"Analyzing {skill}..."):
            result = generate_response(skill)
            st.markdown(result)
    else:
        st.warning("⚠️ Please enter a skill")

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Hugging Face")
