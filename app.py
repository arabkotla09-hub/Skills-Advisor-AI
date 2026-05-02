import streamlit as st
import os
from huggingface_hub import InferenceClient
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(page_title="Skill Advisor AI Pro", page_icon="🚀", layout="wide")

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("❌ Please set HF_TOKEN in environment variables")
    st.stop()

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=HF_TOKEN
)

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.title("⚙️ Customize Your Plan")

level = st.sidebar.selectbox("📊 Skill Level", ["Beginner", "Intermediate", "Advanced"])

goal = st.sidebar.selectbox("🎯 Goal", [
    "Freelancing", "Job", "Remote Job", "Startup", "Side Hustle"
])

region = st.sidebar.selectbox("🌍 Market Focus", ["Pakistan", "Global", "Both"])

time_commitment = st.sidebar.selectbox("⏳ Time per Week", [
    "5-10 hours", "10-20 hours", "20+ hours"
])

# -----------------------
# MAIN UI
# -----------------------
st.title("🚀 Skill Advisor AI Pro+")
st.markdown("### Get **roadmap + career insights + resources + risk analysis**")

skill = st.text_input("🔍 Enter Skill", placeholder="e.g. AI, Cyber Security, Web Development")

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

Provide structured output:

### 📍 Roadmap
(step-by-step with timeline)

### 🌍 Scope & Future Demand

### 💰 Salary Range (Pakistan + Global)

### 🎓 Best Courses & Resources
Include real links (Coursera, Udemy, YouTube, free)

### ⚠️ Risk Level (Low/Medium/High + reason)

### 💼 Career Opportunities

### ⏱️ Time to Job Ready

### ⭐ Skill Rating (out of 10)

### 🔥 Pro Tips
"""

# -----------------------
# GENERATE RESPONSE
# -----------------------
def generate_response(skill):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a practical and honest career advisor."},
                {"role": "user", "content": build_prompt(skill)}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# -----------------------
# PDF GENERATION
# -----------------------
def create_pdf(text, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    for line in text.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)
    return filename

# -----------------------
# BUTTON
# -----------------------
if st.button("🚀 Generate Full Report"):
    if skill.strip():

        with st.spinner("🧠 AI analyzing skill + market..."):
            result = generate_response(skill)

        # -----------------------
        # TABS
        # -----------------------
        tab1, tab2, tab3 = st.tabs([
            "📘 Full Report",
            "⚡ Insights",
            "📥 Export"
        ])

        # FULL REPORT
        with tab1:
            st.markdown(result)

        # INSIGHTS
        with tab2:
            st.success("⚡ Quick Insights")

            st.write(f"""
- 🎯 Goal: **{goal}**
- 📊 Level: **{level}**
- 🌍 Market: **{region}**
- ⏳ Time: **{time_commitment}**
            """)

            st.info("💡 Tip: Build projects + portfolio for faster growth.")

            st.metric("📈 Demand", "High")
            st.metric("💰 Income Potential", "High")
            st.metric("⚠️ Risk", "Medium")

        # EXPORT
        with tab3:
            # TXT download
            st.download_button(
                "📄 Download as TXT",
                data=result,
                file_name=f"{skill}_report.txt"
            )

            # PDF generation
            pdf_file = create_pdf(result, f"{skill}_report.pdf")

            with open(pdf_file, "rb") as f:
                st.download_button(
                    "📄 Download as PDF",
                    f,
                    file_name=f"{skill}_report.pdf"
                )

    else:
        st.warning("⚠️ Please enter a skill")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.caption("🚀 Built for Hackathon Excellence")
