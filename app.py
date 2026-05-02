import streamlit as st
import os
import json
from huggingface_hub import InferenceClient
from tenacity import retry, stop_after_attempt, wait_fixed
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="SkillAI SaaS",
    page_icon="🚀",
    layout="wide"
)

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("Missing HF_TOKEN")
    st.stop()

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=HF_TOKEN
)

# -------------------------
# CLEAN UI HEADER
# -------------------------
st.title("🚀 SkillAI SaaS")
st.caption("AI Career Intelligence Platform")

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.header("⚙️ Controls")

    skill = st.text_input("Skill", "AI Engineer")

    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
    goal = st.selectbox("Goal", ["Job", "Freelancing", "Startup", "Remote"])
    region = st.selectbox("Market", ["Pakistan", "Global", "Both"])

    generate_btn = st.button("🚀 Generate")

# -------------------------
# SAFE AI PROMPT (JSON OUTPUT ONLY)
# -------------------------
def build_prompt():
    return f"""
Return ONLY valid JSON (no markdown, no explanation).

Skill: {skill}
Level: {level}
Goal: {goal}
Region: {region}

JSON format:
{{
  "roadmap": "...",
  "scope": "...",
  "risk": "Low/Medium/High + reason",
  "salary": "...",
  "resources": ["link1", "link2"],
  "careers": ["..."],
  "time_to_job": "...",
  "rating": 0-10
}}
"""

# -------------------------
# STABLE AI CALL (RETRY + SAFETY)
# -------------------------
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_ai_response():
    res = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You output strict JSON only."},
            {"role": "user", "content": build_prompt()}
        ],
        max_tokens=1200,
        temperature=0.5
    )
    return res.choices[0].message.content


# -------------------------
# CACHE (VERY IMPORTANT FOR SaaS)
# -------------------------
if "data" not in st.session_state:
    st.session_state.data = None


# -------------------------
# GENERATE
# -------------------------
if generate_btn:
    with st.spinner("Analyzing skill..."):
        try:
            raw = get_ai_response()
            st.session_state.data = json.loads(raw)
        except Exception as e:
            st.error("AI failed. Try again.")
            st.stop()

data = st.session_state.data

# -------------------------
# CLEAN DASHBOARD UI
# -------------------------
if data:

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🎯 Skill", skill)
    col2.metric("📊 Level", level)
    col3.metric("🌍 Market", region)
    col4.metric("⭐ Rating", data.get("rating", 0))

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🧭 Roadmap", "🌍 Scope", "⚠️ Risk", "💼 Careers"]
    )

    with tab1:
        st.markdown(data["roadmap"])

    with tab2:
        st.markdown(data["scope"])

    with tab3:
        st.warning(data["risk"])

    with tab4:
        st.write(data["careers"])


    st.subheader("💰 Salary")
    st.info(data["salary"])

    st.subheader("📚 Resources")
    for r in data["resources"]:
        st.markdown(f"- {r}")

# -------------------------
# PDF EXPORT (SAFE)
# -------------------------
def create_pdf(data, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    content = []

    for k, v in data.items():
        text = f"{k.upper()}: {str(v)}"
        content.append(Paragraph(text, styles["Normal"]))
        content.append(Spacer(1, 8))

    doc.build(content)
    return filename


if data:
    pdf = create_pdf(data)

    with open(pdf, "rb") as f:
        st.download_button(
            "📄 Download Report (PDF)",
            f,
            file_name="SkillAI_Report.pdf"
        )
