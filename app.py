import streamlit as st
import os
from huggingface_hub import InferenceClient
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(
    page_title="Skill Advisor AI Pro+",
    page_icon="🚀",
    layout="wide"
)

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("❌ HF_TOKEN missing in environment variables")
    st.stop()

client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=HF_TOKEN
)

# -----------------------
# SIDEBAR INPUTS
# -----------------------
st.sidebar.title("🎛️ Control Panel")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Overview", "🧭 Roadmap", "🌍 Scope", "⚠️ Risk Analysis", "💰 Career & Salary", "📚 Resources", "📥 Export"]
)

skill = st.sidebar.text_input("🔍 Skill", "AI")

level = st.sidebar.selectbox("📊 Level", ["Beginner", "Intermediate", "Advanced"])
goal = st.sidebar.selectbox("🎯 Goal", ["Job", "Freelancing", "Startup", "Remote Job"])
region = st.sidebar.selectbox("🌍 Market", ["Pakistan", "Global", "Both"])
time_commitment = st.sidebar.selectbox("⏳ Time/Week", ["5-10h", "10-20h", "20h+"])


# -----------------------
# PROMPT
# -----------------------
def build_prompt(skill):
    return f"""
You are a senior career advisor.

Skill: {skill}
Level: {level}
Goal: {goal}
Region: {region}
Time: {time_commitment}

Return structured analysis with:
Roadmap, Scope, Risk, Salary, Resources, Careers, Timeline, Rating.
"""


def generate():
    try:
        res = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a strict, practical career advisor."},
                {"role": "user", "content": build_prompt(skill)}
            ],
            max_tokens=1200,
            temperature=0.6
        )
        return res.choices[0].message.content
    except Exception as e:
        return str(e)


# -----------------------
# SESSION STATE (cache result)
# -----------------------
if "result" not in st.session_state:
    st.session_state.result = ""

if st.sidebar.button("🚀 Generate Analysis"):
    if skill.strip():
        with st.spinner("Analyzing skill + market..."):
            st.session_state.result = generate()
    else:
        st.warning("Enter a skill first")


result = st.session_state.result


# -----------------------
# UI PAGES
# -----------------------

if page == "🏠 Overview":
    st.title("🚀 Skill Advisor AI Pro+")
    st.markdown("Get AI-powered career guidance, roadmap, risk analysis & resources")

    if result:
        st.success("Analysis Ready ✔")

        col1, col2, col3 = st.columns(3)
        col1.metric("🎯 Goal", goal)
        col2.metric("📊 Level", level)
        col3.metric("🌍 Market", region)

        st.markdown("### 🧠 AI Summary")
        st.info(result[:800] + " ...")

    else:
        st.warning("Generate analysis from sidebar")



elif page == "🧭 Roadmap":
    st.title("🧭 Learning Roadmap")

    if result:
        st.markdown(result)
    else:
        st.info("Generate analysis first")


elif page == "🌍 Scope":
    st.title("🌍 Market Scope")

    if result:
        st.write("Extracted Scope Section")
        st.markdown(result)
    else:
        st.info("No data yet")


elif page == "⚠️ Risk Analysis":
    st.title("⚠️ Risk Level Breakdown")

    if result:
        st.warning("AI-generated risk insights")
        st.markdown(result)
    else:
        st.info("Generate report first")


elif page == "💰 Career & Salary":
    st.title("💰 Salary & Career Paths")

    if result:
        st.success("Career Opportunities")
        st.markdown(result)
    else:
        st.info("Generate report first")


elif page == "📚 Resources":
    st.title("📚 Learning Resources Hub")

    if result:
        st.markdown("### Courses + Links")
        st.markdown(result)
    else:
        st.info("Generate report first")


elif page == "📥 Export":
    st.title("📥 Export Report")

    if result:
        st.download_button(
            "📄 Download TXT",
            result,
            file_name=f"{skill}_report.txt"
        )
    else:
        st.info("Nothing to export yet")# SESSION STATE (cache result)
# -----------------------
if "result" not in st.session_state:
    st.session_state.result = ""

if st.sidebar.button("🚀 Generate Analysis"):
    if skill.strip():
        with st.spinner("Analyzing skill + market..."):
            st.session_state.result = generate()
    else:
        st.warning("Enter a skill first")


result = st.session_state.result


# -----------------------
# UI PAGES
# -----------------------

if page == "🏠 Overview":
    st.title("🚀 Skill Advisor AI Pro+")
    st.markdown("Get AI-powered career guidance, roadmap, risk analysis & resources")

    if result:
        st.success("Analysis Ready ✔")

        col1, col2, col3 = st.columns(3)
        col1.metric("🎯 Goal", goal)
        col2.metric("📊 Level", level)
        col3.metric("🌍 Market", region)

        st.markdown("### 🧠 AI Summary")
        st.info(result[:800] + " ...")

    else:
        st.warning("Generate analysis from sidebar")



elif page == "🧭 Roadmap":
    st.title("🧭 Learning Roadmap")

    if result:
        st.markdown(result)
    else:
        st.info("Generate analysis first")


elif page == "🌍 Scope":
    st.title("🌍 Market Scope")

    if result:
        st.write("Extracted Scope Section")
        st.markdown(result)
    else:
        st.info("No data yet")


elif page == "⚠️ Risk Analysis":
    st.title("⚠️ Risk Level Breakdown")

    if result:
        st.warning("AI-generated risk insights")
        st.markdown(result)
    else:
        st.info("Generate report first")


elif page == "💰 Career & Salary":
    st.title("💰 Salary & Career Paths")

    if result:
        st.success("Career Opportunities")
        st.markdown(result)
    else:
        st.info("Generate report first")


elif page == "📚 Resources":
    st.title("📚 Learning Resources Hub")

    if result:
        st.markdown("### Courses + Links")
        st.markdown(result)
    else:
        st.info("Generate report first")


elif page == "📥 Export":
    st.title("📥 Export Report")

    if result:
        st.download_button(
            "📄 Download TXT",
            result,
            file_name=f"{skill}_report.txt"
        )
    else:
        st.info("Nothing to export yet")
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
