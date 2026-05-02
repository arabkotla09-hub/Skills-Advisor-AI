import streamlit as st
import os
from huggingface_hub import InferenceClient

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(
    page_title="Skill AI Advisor",
    page_icon="🧠",
    layout="wide"
)

# -----------------------
# HF TOKEN
# -----------------------
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    st.error("❌ HF_TOKEN missing in environment variables")
    st.stop()

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=HF_TOKEN
)

# -----------------------
# SIDEBAR (CONTROL PANEL)
# -----------------------
st.sidebar.title("⚙️ Control Panel")

level = st.sidebar.selectbox("📊 Skill Level", ["Beginner", "Intermediate", "Advanced"])
goal = st.sidebar.selectbox("🎯 Goal", ["Job", "Freelancing", "Startup", "Remote Job"])
region = st.sidebar.selectbox("🌍 Market", ["Pakistan", "Global", "Both"])
time_commitment = st.sidebar.selectbox("⏳ Time Weekly", ["5-10 hrs", "10-20 hrs", "20+ hrs"])

st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: Be consistent. Build projects.")

# -----------------------
# HEADER (SAAS STYLE)
# -----------------------
st.title("🧠 Skill AI Advisor Pro")
st.markdown("### Your AI-powered career strategist 🚀")

# -----------------------
# INPUT SECTION (CLEAN UI)
# -----------------------
with st.container():
    skill = st.text_input("🔍 Enter Skill or Course", placeholder="e.g. AI, Cyber Security, Web Development")

    generate = st.button("⚡ Generate Career Plan")

# -----------------------
# PROMPT ENGINE
# -----------------------
def build_prompt(skill):
    return f"""
You are a world-class career strategist.

Skill: {skill}
Level: {level}
Goal: {goal}
Market: {region}
Time: {time_commitment}

Return structured output:

1. Roadmap (step-by-step)
2. Market demand (future scope)
3. Salary (Pakistan + Global)
4. Best learning resources (with links)
5. Risks
6. Job opportunities
7. Time to become job-ready
8. Skill rating (1-10)
9. Pro tips

Be realistic, sharp, and practical.
"""

# -----------------------
# AI CALL (SAFE)
# -----------------------
def get_response(skill):
    try:
        res = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a strict but helpful career advisor."},
                {"role": "user", "content": build_prompt(skill)}
            ],
            max_tokens=900,
            temperature=0.7
        )
        return res.choices[0].message.content

    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# -----------------------
# OUTPUT UI (CHAT STYLE)
# -----------------------
if generate:

    if skill.strip():

        with st.spinner("🧠 Thinking like a career expert..."):
            output = get_response(skill)

        st.markdown("---")

        # MAIN OUTPUT BOX (CHAT STYLE)
        st.subheader("📘 Career Analysis Report")

        st.markdown(
            f"""
            <div style="
                padding:20px;
                border-radius:12px;
                background-color:#111827;
                color:white;
                line-height:1.6;
                font-size:15px;
            ">
            {output}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # INSIGHT CARDS
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🎯 Goal", goal)

        with col2:
            st.metric("📊 Level", level)

        with col3:
            st.metric("🌍 Market", region)

        with col4:
            st.metric("⏳ Time", time_commitment)

        # DOWNLOAD SECTION
        st.download_button(
            "📥 Download Full Report",
            data=output,
            file_name=f"{skill}_career_report.txt"
        )

    else:
        st.warning("⚠️ Please enter a skill")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.caption("🧠 Skill AI Advisor • Built for next-gen career planning")    st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }

    .stTextInput input {
        background-color: #262730;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------
# SIDEBAR CONTROLS
# -----------------------
st.sidebar.title("⚙️ Customize")

level = st.sidebar.selectbox("📊 Skill Level", ["Beginner", "Intermediate", "Advanced"])

goal = st.sidebar.selectbox("🎯 Goal", ["Freelancing", "Job", "Remote Job", "Startup", "Side Hustle"])

region = st.sidebar.selectbox("🌍 Market", ["Pakistan", "Global", "Both"])

time_commitment = st.sidebar.selectbox("⏳ Time/Week", ["5-10 hours", "10-20 hours", "20+ hours"])

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
You are a brutally honest career advisor.

Skill: {skill}
Level: {level}
Goal: {goal}
Market: {region}
Time: {time_commitment}

Give:

1. Roadmap step-by-step
2. Scope & future demand
3. Salary range (Pakistan + Global)
4. Best courses (with links)
5. Risk level
6. Career opportunities
7. Time to job-ready
8. Skill rating out of 10
9. Pro tips

Be practical and realistic.
"""

# -----------------------
# SAFE AI FUNCTION (NO CRASH)
# -----------------------
def generate_response(skill):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a practical career advisor."},
                {"role": "user", "content": build_prompt(skill)}
            ],
            max_tokens=900,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# -----------------------
# BUTTON ACTION
# -----------------------
if st.button("🚀 Generate Advanced Plan"):

    if skill.strip():

        with st.spinner("🧠 AI analyzing skill & market..."):
            result = generate_response(skill)

        tab1, tab2, tab3, tab4 = st.tabs([
            "📘 Full Report",
            "⚡ Insights",
            "📊 Score",
            "📥 Export"
        ])

        with tab1:
            st.markdown(result)

        with tab2:
            st.success("Quick Summary")
            st.write(f"""
- Goal: {goal}
- Level: {level}
- Market: {region}
- Time: {time_commitment}
            """)
            st.info("Focus on real projects, not just learning.")

        with tab3:
            st.metric("Demand", "High")
            st.metric("Earning Potential", "High")
            st.metric("Risk", "Medium")
            st.progress(80)

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
st.caption("🚀 Built for Hackathon Domination")        }

        .stTextInput input {
            background-color: #262730;
            color: white;
        }

        .stSelectbox, .stRadio {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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
# PROMPT BUILDER
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

1. Roadmap (step-by-step)
2. Scope & Future Demand
3. Salary Range (Pakistan + Global)
4. Best Courses & Resources (with real links)
5. Risk Level
6. Career Opportunities
7. Time to Job Ready
8. Skill Rating (out of 10)
9. Pro Tips

Be practical and honest.
"""

# -----------------------
# AI CALL
# -----------------------
def generate_response(skill):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a brutally honest career advisor."
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
# BUTTON
# -----------------------
if st.button("🚀 Generate Advanced Plan"):

    if skill.strip():

        with st.spinner("🧠 AI analyzing skill..."):
            result = generate_response(skill)

        tab1, tab2, tab3, tab4 = st.tabs([
            "📘 Full Report",
            "⚡ Insights",
            "📊 Score",
            "📥 Export"
        ])

        with tab1:
            st.markdown(result)

        with tab2:
            st.success("Quick Summary")
            st.write(f"""
- Goal: {goal}
- Level: {level}
- Market: {region}
- Time: {time_commitment}
            """)
            st.info("Focus on projects, not just theory.")

        with tab3:
            st.metric("Demand", "High")
            st.metric("Earning", "High")
            st.metric("Risk", "Medium")
            st.progress(80)

        with tab4:
            st.download_button(
                "Download Report",
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
level = st.sidebar.selectbox("📊 Skill Level", ["Beginner", "Intermediate", "Advanced"])

goal = st.sidebar.selectbox("🎯 Goal", [
    "Freelancing", "Job", "Remote Job", "Startup", "Side Hustle"
])

region = st.sidebar.selectbox("🌍 Market", ["Pakistan", "Global", "Both"])

time_commitment = st.sidebar.selectbox("⏳ Time/Week", [
    "5-10 hours", "10-20 hours", "20+ hours"
])

# -----------------------
# MAIN UI
# -----------------------
st.title("🚀 Skill Advisor AI Pro+")
st.markdown("### AI-powered **career roadmap + market intelligence**")

skill = st.text_input("🔍 Enter Skill", placeholder="e.g. AI, Cyber Security")

# -----------------------
# PROMPT (UPGRADED 🔥)
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
level = st.sidebar.selectbox("📊 Skill Level", ["Beginner", "Intermediate", "Advanced"])

goal = st.sidebar.selectbox("🎯 Goal", [
    "Freelancing", "Job", "Remote Job", "Startup", "Side Hustle"
])

region = st.sidebar.selectbox("🌍 Market", ["Pakistan", "Global", "Both"])

time_commitment = st.sidebar.selectbox("⏳ Time/Week", [
    "5-10 hours", "10-20 hours", "20+ hours"
])

# -----------------------
# MAIN UI
# -----------------------
st.title("🚀 Skill Advisor AI Pro+")
st.markdown("### AI-powered **career roadmap + market intelligence**")

skill = st.text_input("🔍 Enter Skill", placeholder="e.g. AI, Cyber Security")

# -----------------------
# PROMPT (UPGRADED 🔥)
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
level = st.sidebar.selectbox("📊 Skill Level", ["Beginner", "Intermediate", "Advanced"])

goal = st.sidebar.selectbox("🎯 Goal", [
    "Freelancing", "Job", "Remote Job", "Startup", "Side Hustle"
])

region = st.sidebar.selectbox("🌍 Market", ["Pakistan", "Global", "Both"])

time_commitment = st.sidebar.selectbox("⏳ Time/Week", [
    "5-10 hours", "10-20 hours", "20+ hours"
])

# -----------------------
# MAIN UI
# -----------------------
st.title("🚀 Skill Advisor AI Pro+")
st.markdown("### AI-powered **career roadmap + market intelligence**")

skill = st.text_input("🔍 Enter Skill", placeholder="e.g. AI, Cyber Security")

# -----------------------
# PROMPT (UPGRADED 🔥)
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
st.caption("🚀 Built for Hackathon Domination")# -----------------------
st.title("🚀 Skill Advisor AI Pro+")
st.markdown("### AI-powered career roadmap engine")

skill = st.text_input("🔍 Enter Skill (e.g. AI, Cyber Security)")

# -----------------------
# PROMPT
# -----------------------
def build_prompt(skill):
    return f"""
You are a brutally honest career advisor.

Skill: {skill}
Level: {level}
Goal: {goal}
Market: {region}
Time: {time_commitment}

Provide:

1. Roadmap (step-by-step)
2. Scope & future demand
3. Salary range (Pakistan + Global)
4. Best courses (real links)
5. Risk level
6. Career opportunities
7. Time to job-ready
8. Skill rating (out of 10)
9. Pro tips

Be practical, realistic, and honest.
"""

# -----------------------
# API CALL (SAFE)
# -----------------------
@st.cache_data(show_spinner=False)
def generate_response(skill):
    try:
        response = client.text_generation(
            prompt=build_prompt(skill),
            max_new_tokens=900,
            temperature=0.7,
            return_full_text=False
        )
        return response
    except Exception as e:
        return f"❌ API Error: {str(e)}"

# -----------------------
# BUTTON ACTION
# -----------------------
if st.button("🚀 Generate Advanced Plan"):
    if skill.strip():

        with st.spinner("🧠 AI analyzing global market trends..."):
            result = generate_response(skill)

        tab1, tab2, tab3, tab4 = st.tabs([
            "📘 Full Report",
            "⚡ Insights",
            "📊 Score",
            "📥 Export"
        ])

        with tab1:
            st.markdown(result)

        with tab2:
            st.success("Quick Summary")
            st.write(f"""
- Goal: {goal}
- Level: {level}
- Market: {region}
- Time: {time_commitment}
""")

        with tab3:
            st.metric("Demand", "High")
            st.metric("Earning", "High")
            st.metric("Risk", "Medium")
            st.progress(85)

        with tab4:
            st.download_button(
                "Download Report",
                data=result,
                file_name=f"{skill}_report.txt"
            )
            st.code(result)

    else:
        st.warning("Enter a skill first")

# -----------------------
# FOOTER
# -----------------------
st.markdown("---")
st.caption("🚀 Hackathon SaaS Version (Stable Build)")
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
