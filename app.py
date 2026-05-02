import streamlit as st
import os
from huggingface_hub import InferenceClient

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(
    page_title="Skill Advisor AI Pro",
    page_icon="🚀",
    layout="wide"
)

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("❌ Please set HF_TOKEN in environment variables")
    st.stop()

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=HF_TOKEN
)

# -----------------------
# THEME SWITCH (FIXED)
# -----------------------
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }

        .stTextInput input {
            background-color: #262730;
            color: white;
        }

        .stSelectbox div, .stRadio div {
            background-color: #262730;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# -----------------------
# SIDEBAR CONTROLS
# -----------------------
st.sidebar.title("⚙️ Customize")

level = st.sidebar.selectbox(
    "📊 Skill Level",
    ["Beginner", "Intermediate", "Advanced"]
)

goal = st.sidebar.selectbox(
    "🎯 Goal",
    ["Freelancing", "Job", "Remote Job", "Startup", "Side Hustle"]
)

region = st.sidebar.selectbox(
    "🌍 Market",
    ["Pakistan", "Global", "Both"]
)

time_commitment = st.sidebar.selectbox(
    "⏳ Time/Week",
    ["5-10 hours", "10-20 hours", "20+ hours"]
)

# -----------------------
# MAIN UI
# -----------------------
st.title("🚀 Skill Advisor AI Pro+")
st.markdown("### AI-powered career roadmap + market intelligence")

skill = st.text_input("🔍 Enter Skill", placeholder="e.g. AI, Cyber Security")

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
Time: {time_commitment}

Provide structured output:

### 📍 Roadmap
(step-by-step with timeline)

### 🌍 Scope & Future Demand

### 💰 Salary Range
(Pakistan + Global)

### 🎓 Best Courses & Resources
Include real links (Coursera, Udemy, YouTube, Free resources)

### ⚠️ Risk Level

### 💼 Career Opportunities

### ⏱️ Time to Job Ready

### ⭐ Skill Rating (out of 10)

### 🔥 Pro Tips

Be practical, honest, and realistic.
"""

# -----------------------
# AI RESPONSE
# -----------------------
def generate_response(skill):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a brutally honest and practical career advisor."
                },
                {
                    "role": "user",
                    "content": build_prompt(skill)
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"

# -----------------------
# GENERATE BUTTON
# -----------------------
if st.button("🚀 Generate Advanced Plan"):
    if skill.strip():

        with st.spinner("🧠 AI analyzing skill + market trends..."):
            result = generate_response(skill)

        tab1, tab2, tab3, tab4 = st.tabs([
            "📘 Full Report",
            "⚡ Insights",
            "📊 Skill Score",
            "📥 Export"
        ])

        # FULL REPORT
        with tab1:
            st.markdown(result)

        # INSIGHTS
        with tab2:
            st.success("⚡ Quick Summary")

            st.write(f"""
- 🎯 Goal: {goal}  
- 📊 Level: {level}  
- 🌍 Market: {region}  
- ⏳ Time: {time_commitment}
            """)

            st.info("💡 Tip: Build real projects instead of only learning theory.")

        # SCORE
        with tab3:
            st.metric("📈 Demand", "High")
            st.metric("💰 Earning Potential", "High")
            st.metric("⚠️ Risk", "Medium")
            st.progress(80)

        # EXPORT
        with tab4:
            st.download_button(
                "📄 Download Report",
                data=result,
                file_name=f"{skill}_report.txt"
            )

            st.code(result)

    else:
        st.warning("⚠️ Please enter a skill")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.caption("🚀 Built for Hackathon Domination")Goal: {goal}
Market: {region}
Time: {time_commitment}

Provide structured output:

### 📍 Roadmap
(step-by-step with timeline)

### 🌍 Scope & Future Demand
(is it growing or declining?)

### 💰 Salary Range
(Pakistan + Global)

### 🎓 Best Courses & Resources
Give REAL clickable links from:
- Coursera
- Udemy
- YouTube
- Free resources

### ⚠️ Risk Level
(Low / Medium / High + explanation)

### 💼 Career Opportunities

### ⏱️ Time to Job Ready

### ⭐ Skill Rating
(rate out of 10 based on future potential)

### 🔥 Pro Tips
(unique insights)

Keep it practical and honest.
"""

# -----------------------
# GENERATE RESPONSE
# -----------------------
def generate_response(skill):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a brutally honest and practical career advisor."},
                {"role": "user", "content": build_prompt(skill)}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# -----------------------
# BUTTON ACTION
# -----------------------
if st.button("🚀 Generate Advanced Plan"):
    if skill.strip():

        with st.spinner("🧠 AI analyzing market + skill..."):
            result = generate_response(skill)

        # -----------------------
        # TABS UI 🔥
        # -----------------------
        tab1, tab2, tab3, tab4 = st.tabs([
            "📘 Full Report",
            "⚡ Insights",
            "📊 Skill Score",
            "📥 Export"
        ])

        # FULL REPORT
        with tab1:
            st.markdown(result)

        # QUICK INSIGHTS
        with tab2:
            st.success("⚡ Quick Summary")

            st.write(f"""
- 🎯 Best for: **{goal}**
- 📊 Level: **{level}**
- 🌍 Market: **{region}**
- ⏳ Time Commitment: **{time_commitment}**
            """)

            st.info("💡 Tip: Focus on projects + consistency to stand out.")

        # SKILL SCORE
        with tab3:
            st.metric("📈 Demand", "High")
            st.metric("💰 Earning Potential", "High")
            st.metric("⚠️ Risk", "Medium")

            st.progress(80)

        # EXPORT
        with tab4:
            st.download_button(
                "📄 Download Report",
                data=result,
                file_name=f"{skill}_report.txt"
            )

            st.code(result)

    else:
        st.warning("⚠️ Please enter a skill")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.caption("🚀 Built for Hackathon Domination")
