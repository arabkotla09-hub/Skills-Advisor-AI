import streamlit as st
import os
from huggingface_hub import InferenceClient

# -----------------------
# CONFIG & SETTINGS
# -----------------------
st.set_page_config(page_title="Skill Advisor AI Pro+", page_icon="🚀", layout="wide")

# Theme / Custom CSS for Dark Mode consistency
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #31333f; }
    div.stButton > button:first-child {
        background-color: #ff4b4b; color: white; border-radius: 8px; width: 100%; height: 3em; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------
# AUTHENTICATION
# -----------------------
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("❌ HF_TOKEN not found. Please set it in your environment variables.")
    st.stop()

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=HF_TOKEN
)

# -----------------------
# SIDEBAR CONTROLS
# -----------------------
with st.sidebar:
    st.title("⚙️ Personalization")
    level = st.selectbox("📊 Current Level", ["Beginner", "Intermediate", "Advanced"])
    goal = st.selectbox("🎯 Career Goal", ["Freelancing", "Job", "Remote Job", "Startup", "Side Hustle"])
    region = st.selectbox("🌍 Target Market", ["Pakistan", "Global", "Both"])
    time_commitment = st.selectbox("⏳ Time/Week", ["5-10 hours", "10-20 hours", "20+ hours"])
    st.divider()
    st.info("💡 **Pro Tip:** Focus on building a portfolio. Theory alone won't get you hired in 2026.")

# -----------------------
# MAIN UI
# -----------------------
st.title("🚀 Skill Advisor AI Pro+")
st.markdown("### AI-powered **career roadmap + market intelligence**")

skill_input = st.text_input("🔍 What skill do you want to master?", placeholder="e.g. LLM Engineering, Cyber Security, Cloud Architecture")

# -----------------------
# LOGIC & PROMPT
# -----------------------
def generate_roadmap(skill):
    prompt = f"""
    You are a world-class, brutally honest career strategist. 
    Analyze the following:
    Skill: {skill} | Level: {level} | Goal: {goal} | Market: {region} | Time: {time_commitment}

    Provide a highly structured report in Markdown:
    ### 📍 Phase-by-Phase Roadmap
    (Step-by-step with a realistic timeline)
    
    ### 🌍 Market Intelligence
    (Is demand growing or declining? AI displacement risk?)
    
    ### 💰 Salary Benchmarks
    (Specific ranges for Pakistan vs. Global)
    
    ### 🎓 Curated Learning Path
    (Provide REAL resources: Coursera, Udemy, and YouTube search terms)
    
    ### ⚠️ The Hard Truth (Risk Level)
    (Saturation, difficulty, or industry shifts)
    
    ### ⭐ Skill Rating
    (Score out of 10 based on future-proofing)
    
    ### 🔥 Expert Pro Tips
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional career advisor who gives practical, no-nonsense advice."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# -----------------------
# EXECUTION
# -----------------------
if st.button("Generate Advanced Career Plan"):
    if skill_input.strip():
        with st.spinner("🧠 Analyzing market data and skill trajectories..."):
            report = generate_roadmap(skill_input)
            
            # -----------------------
            # OUTPUT TABS
            # -----------------------
            tab1, tab2, tab3 = st.tabs(["📘 Full Report", "📊 Market Metrics", "📥 Export"])

            with tab1:
                st.markdown(report)

            with tab2:
                col1, col2, col3 = st.columns(3)
                col1.metric("Market Demand", "High 🔥")
                col2.metric("Difficulty", level)
                col3.metric("Goal Path", goal)
                
                st.write("---")
                st.subheader("Quick Success Checklist")
                st.checkbox("Build 3 Portfolio Projects")
                st.checkbox("Optimize LinkedIn for this skill")
                st.checkbox("Network with 5 industry pros")

            with tab3:
                st.download_button(
                    label="📄 Download Full Report (.txt)",
                    data=report,
                    file_name=f"{skill_input}_roadmap.txt",
                    mime="text/plain"
                )
                st.info("You can copy the raw text below for your Notion or Obsidian notes.")
                st.code(report, language="markdown")
    else:
        st.warning("⚠️ Please enter a skill first!")

st.divider()
st.caption("🚀 Built for Hackathon Domination | Powered by Llama 3")
