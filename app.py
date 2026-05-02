import streamlit as st
import os
from huggingface_hub import InferenceClient

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(page_title="Skill Advisor AI", page_icon="🚀", layout="wide")

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("❌ Please set your Hugging Face token")
    st.stop()

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=HF_TOKEN
)

# -----------------------
# SIDEBAR (NEW 🔥)
# -----------------------
st.sidebar.title("⚙️ Customize Advice")

level = st.sidebar.selectbox("📊 Skill Level", ["Beginner", "Intermediate", "Advanced"])

goal = st.sidebar.selectbox("🎯 Goal", [
    "Freelancing",
    "Job",
    "Remote Job",
    "Startup",
    "Side Hustle"
])

region = st.sidebar.selectbox("🌍 Market Focus", [
    "Pakistan",
    "Global",
    "Both"
])

time_commitment = st.sidebar.selectbox("⏳ Time per Week", [
    "5-10 hours",
    "10-20 hours",
    "20+ hours"
])

# -----------------------
# MAIN UI
# -----------------------
st.title("🚀 Skill Advisor AI Pro")
st.markdown("### Turn any skill into a **clear roadmap + career plan**")

# Suggestions
st.markdown("💡 *Try:* Python, AI, Cyber Security, UI/UX, Video Editing")

skill = st.text_input("🔍 Enter Skill", placeholder="e.g. AI, Web Development")

# -----------------------
# PROMPT
# -----------------------
def build_prompt(skill):
    return f"""
You are an expert career advisor.

Skill: {skill}
Level: {level}
Goal: {goal}
Market: {region}
Time Commitment: {time_commitment}

Give structured output:

### 📍 Roadmap
(step-by-step, with timeline)

### ⏱️ Time Required

### 💰 Salary Range (Pakistan + Global)

### 🌍 Scope

### 🎓 Best Platforms

### 💼 Career Opportunities

### ⚠️ Drawbacks

### 🔥 Pro Tips (unique insights)

Keep it practical and modern.
"""

# -----------------------
# GENERATE
# -----------------------
def generate_response(skill):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a smart, practical career advisor."},
                {"role": "user", "content": build_prompt(skill)}
            ],
            max_tokens=900,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# -----------------------
# BUTTON
# -----------------------
if st.button("🚀 Generate Smart Plan"):
    if skill.strip():

        with st.spinner("🧠 AI is building your roadmap..."):
            result = generate_response(skill)

        # -----------------------
        # TABS (NEW 🔥)
        # -----------------------
        tab1, tab2, tab3 = st.tabs(["📘 Full Plan", "⚡ Quick Insights", "📥 Export"])

        with tab1:
            st.markdown(result)

        with tab2:
            st.success("⚡ Key Insight")
            st.write(f"👉 {skill} is best for **{goal}** with {time_commitment} weekly effort.")

            st.info("💡 Tip: Consistency beats intensity.")

        with tab3:
            st.download_button(
                label="📄 Download Plan",
                data=result,
                file_name=f"{skill}_plan.txt"
            )

            st.code(result)

    else:
        st.warning("⚠️ Please enter a skill")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.caption("💡 Built for Hackathon Winning 🚀")
