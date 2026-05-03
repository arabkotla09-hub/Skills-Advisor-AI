# 🚀 Skills Advisor AI PRO — Upgraded Version
# Modern UI + Theme Switcher + Better UX + Stable Backend

import streamlit as st
import os
import time
from huggingface_hub import InferenceClient

# ───────────────── CONFIG ─────────────────
st.set_page_config(page_title="Skills Advisor AI Pro", page_icon="🚀", layout="wide")

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"
MAX_TOKENS = 1200
TEMPERATURE = 0.7

# ───────────────── THEME SWITCH ─────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"


def apply_theme():
    if st.session_state.theme == "dark":
        bg = "#0e1117"
        card = "#161b22"
        text = "#e6edf3"
    else:
        bg = "#f5f7fb"
        card = "#ffffff"
        text = "#111"

    st.markdown(f"""
    <style>
    .stApp {{ background: {bg}; color: {text}; }}
    .card {{
        background: {card};
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        margin-top: 15px;
    }}
    .big-title {{
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 10px;
    }}
    .sub {{ opacity: 0.7; margin-bottom: 20px; }}
    </style>
    """, unsafe_allow_html=True)


apply_theme()

# ───────────────── SIDEBAR ─────────────────
with st.sidebar:
    st.title("⚙️ Control Panel")

    if st.button("🌗 Toggle Theme"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

    mode = st.selectbox("Mode", [
        "Roadmap",
        "Compare",
        "Market Intel",
        "Skill Suggestion"
    ])

    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
    goal = st.selectbox("Goal", ["Freelancing", "Job", "Startup"])

# ───────────────── CLIENT ─────────────────
@st.cache_resource
def get_client():
    token = os.getenv("HF_TOKEN")
    if not token:
        return None
    return InferenceClient(model=MODEL_ID, token=token, timeout=60)

client = get_client()

if client is None:
    st.error("Set HF_TOKEN first")
    st.stop()

# ───────────────── AI ─────────────────
def ask_ai(prompt):
    try:
        res = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# ───────────────── HEADER ─────────────────
st.markdown('<div class="big-title">🚀 Skills Advisor AI PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">AI-powered career decisions, but smarter.</div>', unsafe_allow_html=True)

# ───────────────── FEATURES ─────────────────

# 1️⃣ ROADMAP
if mode == "Roadmap":
    skill = st.text_input("Enter Skill")

    if st.button("Generate Roadmap"):
        if skill:
            with st.spinner("Building roadmap..."):
                prompt = f"Create a complete roadmap for {skill} for a {level} aiming for {goal}."
                res = ask_ai(prompt)

            st.markdown(f'<div class="card">{res}</div>', unsafe_allow_html=True)

# 2️⃣ COMPARE
elif mode == "Compare":
    a = st.text_input("Skill A")
    b = st.text_input("Skill B")

    if st.button("Compare"):
        if a and b:
            with st.spinner("Analyzing..."):
                res = ask_ai(f"Compare {a} vs {b} for {goal}")

            st.markdown(f'<div class="card">{res}</div>', unsafe_allow_html=True)

# 3️⃣ MARKET
elif mode == "Market Intel":
    skill = st.text_input("Skill")

    if st.button("Analyze Market"):
        if skill:
            with st.spinner("Fetching data..."):
                res = ask_ai(f"Job market analysis for {skill}")

            st.markdown(f'<div class="card">{res}</div>', unsafe_allow_html=True)

# 4️⃣ NEW FEATURE: SKILL SUGGESTION 🔥
elif mode == "Skill Suggestion":
    interest = st.text_input("Your Interest (e.g. AI, Design, Business)")

    if st.button("Suggest Skills"):
        if interest:
            with st.spinner("Finding best skills..."):
                res = ask_ai(f"Suggest top 5 high-income skills for someone interested in {interest}")

            st.markdown(f'<div class="card">{res}</div>', unsafe_allow_html=True)

# ───────────────── FOOTER ─────────────────
st.markdown("---")
st.caption("Built for Hackathon • Upgraded to SaaS-grade UI")
