import streamlit as st
import os
import time
from huggingface_hub import InferenceClient

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Skill Advisor AI Pro+",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
MAX_TOKENS = 1500
TEMPERATURE = 0.7

APP_MODES = ["Single Skill Roadmap", "Compare Skills/Courses", "Job Market Intel"]

LEVELS = ["Beginner", "Intermediate", "Advanced"]
GOALS = ["Freelancing", "Job", "Remote Job", "Startup", "Side Hustle"]
REGIONS = ["Pakistan", "Global", "Both"]
TIME_SLOTS = ["5-10 hours", "10-20 hours", "20+ hours"]

# ─────────────────────────────────────────────
# THEME
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0c14 0%, #0e1117 60%, #111827 100%);
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0d1021;
    border-right: 1px solid #1e2740;
}

/* Title font */
h1, h2, h3 {
    font-family: 'Space Mono', monospace !important;
    letter-spacing: -0.5px;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #12182b;
    padding: 16px 20px;
    border-radius: 12px;
    border: 1px solid #1e2740;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}

/* Primary button */
div.stButton > button:first-child {
    background: linear-gradient(90deg, #e63946, #c1121f);
    color: white;
    border: none;
    border-radius: 10px;
    width: 100%;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.5px;
    padding: 0.65rem 1rem;
    transition: all 0.2s ease;
}
div.stButton > button:first-child:hover {
    background: linear-gradient(90deg, #ff6b6b, #e63946);
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(230,57,70,0.4);
}

/* Text input */
.stTextInput > div > div > input {
    background: #12182b;
    border: 1px solid #1e2740;
    color: #e2e8f0;
    border-radius: 8px;
}
.stTextInput > div > div > input:focus {
    border-color: #e63946;
    box-shadow: 0 0 0 2px rgba(230,57,70,0.2);
}

/* Selectbox */
.stSelectbox > div > div {
    background: #12182b;
    border: 1px solid #1e2740;
    border-radius: 8px;
}

/* Info/warning boxes */
.stAlert {
    border-radius: 10px;
}

/* Result container */
.result-box {
    background: #12182b;
    border: 1px solid #1e2740;
    border-left: 3px solid #e63946;
    border-radius: 12px;
    padding: 24px 28px;
    margin-top: 16px;
    line-height: 1.75;
}

/* Tags */
.tag {
    display: inline-block;
    background: #1e2740;
    color: #93c5fd;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.78rem;
    margin: 2px;
    font-family: 'Space Mono', monospace;
}

/* Divider */
hr {
    border-color: #1e2740 !important;
}

/* Spinner text */
.stSpinner > div {
    border-top-color: #e63946 !important;
}

/* Expander */
.stExpander {
    background: #12182b;
    border: 1px solid #1e2740;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# AUTH & CLIENT
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_client():
    token = os.getenv("HF_TOKEN")
    if not token:
        return None
    return InferenceClient(model=MODEL_ID, token=token)


client = get_client()
if client is None:
    st.error("❌ **HF_TOKEN not found.** Please set it in your environment variables and restart.")
    st.stop()


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = ""


# ─────────────────────────────────────────────
# AI HELPERS
# ─────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a brutally honest, data-driven career strategist specialising in tech skills "
    "and the Pakistani & global freelance market. Be specific, actionable, and direct. "
    "Use markdown formatting with headers and bullet points."
)


def build_messages(user_prompt: str) -> list[dict]:
    """Build message list including short conversation history."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    # Include last 2 exchanges for context (keeps tokens low)
    for turn in st.session_state.history[-4:]:
        messages.append(turn)
    messages.append({"role": "user", "content": user_prompt})
    return messages


def stream_ai_response(prompt: str):
    """Stream response token-by-token; yields text chunks."""
    messages = build_messages(prompt)
    try:
        stream = client.chat.completions.create(
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            stream=True,
        )
        full = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            full += delta
            yield delta
        # Save to history
        st.session_state.history.append({"role": "user", "content": prompt})
        st.session_state.history.append({"role": "assistant", "content": full})
        st.session_state.last_result = full
    except Exception as e:
        yield f"\n\n❌ **AI Error:** {e}"


def get_ai_response(prompt: str) -> str:
    """Non-streaming wrapper (used for comparison mode)."""
    messages = build_messages(prompt)
    try:
        resp = client.chat.completions.create(
            messages=messages,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        result = resp.choices[0].message.content
        st.session_state.history.append({"role": "user", "content": prompt})
        st.session_state.history.append({"role": "assistant", "content": result})
        st.session_state.last_result = result
        return result
    except Exception as e:
        return f"❌ **AI Error:** {e}"


# ─────────────────────────────────────────────
# PROMPT BUILDERS
# ─────────────────────────────────────────────
def roadmap_prompt(skill, level, goal, region, time_commitment):
    return f"""
Create a detailed, opinionated career roadmap for **{skill}**.

Context:
- Learner Level: {level}
- Career Goal: {goal}
- Target Market: {region}
- Weekly Time: {time_commitment}

Structure your response with these sections:
## 🗺️ Roadmap Overview
A 2-3 sentence summary and estimated time to job-ready.

## 📅 Phase-by-Phase Plan
Break into phases (Foundation → Core → Advanced → Portfolio). For each phase: duration, key topics, and a milestone.

## 💰 Salary / Rate Expectations
Provide realistic ranges for Pakistan AND globally (USD). Include freelance rates on Upwork/Fiverr.

## 📚 Best Resources
List 5-7 specific resources with URLs where possible (free first, paid second).

## ⚠️ Honest Risk Assessment
Rate: Low / Medium / High. What could go wrong? What's the job market reality?

## ✅ Your First 7 Days Action Plan
Concrete daily tasks for the first week.
"""


def compare_prompt(a, b, level, goal, region, time_commitment):
    return f"""
Compare **{a}** vs **{b}** for a {level}-level learner targeting {goal} in {region} with {time_commitment}/week.

## 📊 Side-by-Side Comparison Table
Create a markdown table covering: Learning Curve, Job Demand, Freelance Potential, Community Size, Avg Salary (Pakistan & Global), Time to Employable.

## ✅ {a} — Pros & Cons

## ✅ {b} — Pros & Cons

## 🏆 Final Verdict
Which should THIS specific person learn first, and why? Be direct — no fence-sitting.

## 🔄 Can They Be Combined?
Is there a workflow where knowing both adds value?
"""


def market_intel_prompt(skill, level, goal, region, time_commitment):
    return f"""
Provide current job market intelligence for **{skill}** in {region}.

Context: {level} learner, goal: {goal}, time: {time_commitment}/week.

## 📈 Market Demand Trends
Is this skill growing, stable, or declining? Reference any concrete data points.

## 🏢 Top Hiring Companies
List 8-10 companies actively hiring for this skill (mix of local Pakistani companies and global remote employers).

## 💼 Job Titles to Target
List 5-7 relevant job titles with typical requirements.

## 🔑 Must-Have Complementary Skills
What 3-5 skills MUST be paired with {skill} to be truly hireable?

## 📣 Where to Find Opportunities
Specific platforms, communities, and strategies for {region}.

## 📉 Red Flags to Avoid
Common mistakes that make candidates uncompetitive.
"""


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    app_mode = st.radio("**Mode**", APP_MODES, key="app_mode")

    st.divider()
    level = st.selectbox("📊 Current Level", LEVELS, key="sb_level")
    goal = st.selectbox("🎯 Career Goal", GOALS, key="sb_goal")
    region = st.selectbox("🌍 Market", REGIONS, key="sb_region")
    time_commitment = st.selectbox("⏳ Time/Week", TIME_SLOTS, key="sb_time")

    st.divider()

    # Context tags
    st.markdown("**Your Profile:**")
    st.markdown(
        f'<span class="tag">{level}</span>'
        f'<span class="tag">{goal}</span>'
        f'<span class="tag">{region}</span>'
        f'<span class="tag">{time_commitment}</span>',
        unsafe_allow_html=True,
    )

    st.divider()

    # Clear history
    if st.button("🗑️ Clear Chat History", key="btn_clear"):
        st.session_state.history = []
        st.session_state.last_result = ""
        st.success("History cleared.")

    with st.expander("💡 Pro Tips"):
        st.markdown("""
- **Portfolio > Resume** in 2026. Ship projects.
- **Niching down** on Upwork beats being a generalist.
- For Pakistan: **Fiverr + Upwork + LinkedIn** combo works best.
- **GitHub activity** is your background check.
- Learn in public — Twitter/X threads get you clients.
        """)

    # Show history count
    if st.session_state.history:
        turns = len(st.session_state.history) // 2
        st.caption(f"🧠 {turns} conversation turn(s) in memory")


# ─────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────

# ── MODE 1: Single Skill Roadmap ──────────────
if app_mode == "Single Skill Roadmap":
    st.title("🚀 Skill Roadmap Engine")
    st.markdown("Get a **personalised, no-BS career roadmap** for any tech skill.")

    col_input, col_btn = st.columns([4, 1])
    with col_input:
        skill = st.text_input(
            "Skill",
            placeholder="e.g. AI Engineering, Flutter, Solidity, Prompt Engineering…",
            label_visibility="collapsed",
            key="single_skill_input",
        )
    with col_btn:
        go = st.button("Generate →", key="btn_single")

    if go:
        if not skill.strip():
            st.warning("⚠️ Please enter a skill name.")
        else:
            prompt = roadmap_prompt(skill.strip(), level, goal, region, time_commitment)
            st.divider()
            st.markdown(f"### 📋 Roadmap: {skill}")

            with st.container():
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                output_area = st.empty()
                streamed = ""
                with st.spinner("Generating roadmap…"):
                    for chunk in stream_ai_response(prompt):
                        streamed += chunk
                        output_area.markdown(streamed + "▌")
                output_area.markdown(streamed)
                st.markdown('</div>', unsafe_allow_html=True)

            # Copy helper
            with st.expander("📋 Copy raw text"):
                st.code(streamed, language=None)


# ── MODE 2: Compare Skills / Courses ──────────
elif app_mode == "Compare Skills/Courses":
    st.title("⚔️ Skill Comparison")
    st.markdown("Side-by-side analysis so you pick the **right** option, not the popular one.")

    col1, col2 = st.columns(2)
    with col1:
        item_a = st.text_input("Option A", placeholder="e.g. React.js", key="compare_a")
    with col2:
        item_b = st.text_input("Option B", placeholder="e.g. Next.js", key="compare_b")

    if st.button("⚔️ Compare Now", key="btn_compare"):
        if not item_a.strip() or not item_b.strip():
            st.warning("⚠️ Fill in both options to compare.")
        else:
            prompt = compare_prompt(
                item_a.strip(), item_b.strip(), level, goal, region, time_commitment
            )
            st.divider()

            # Show two metric cards while loading
            m1, m2, m3 = st.columns(3)
            m1.metric("Option A", item_a)
            m2.metric("Option B", item_b)
            m3.metric("Your Goal", goal)

            with st.spinner(f"Comparing {item_a} vs {item_b}…"):
                result = get_ai_response(prompt)

            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)

            with st.expander("📋 Copy raw text"):
                st.code(result, language=None)


# ── MODE 3: Job Market Intel ──────────────────
elif app_mode == "Job Market Intel":
    st.title("📡 Job Market Intel")
    st.markdown("Real-world demand data and hiring strategy for your target skill.")

    skill = st.text_input(
        "Skill to research",
        placeholder="e.g. Data Engineering, DevOps, LLM Fine-tuning…",
        label_visibility="visible",
        key="market_skill_input",
    )

    if st.button("🔍 Run Intel Report", key="btn_market"):
        if not skill.strip():
            st.warning("⚠️ Please enter a skill.")
        else:
            prompt = market_intel_prompt(skill.strip(), level, goal, region, time_commitment)
            st.divider()
            st.markdown(f"### 📡 Market Report: {skill}")

            with st.container():
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                output_area = st.empty()
                streamed = ""
                with st.spinner("Pulling market intelligence…"):
                    for chunk in stream_ai_response(prompt):
                        streamed += chunk
                        output_area.markdown(streamed + "▌")
                output_area.markdown(streamed)
                st.markdown('</div>', unsafe_allow_html=True)

            with st.expander("📋 Copy raw text"):
                st.code(streamed, language=None)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.divider()
col_f1, col_f2 = st.columns([3, 1])
with col_f1:
    st.caption("🚀 Skill Advisor AI Pro+ · Stable Build v3.0")
with col_f2:
    st.caption(f"Model: `{MODEL_ID.split('/')[-1]}`")    st.divider()
    # Adding unique keys just in case
    level = st.selectbox("📊 Current Level", ["Beginner", "Intermediate", "Advanced"], key="sb_level")
    goal = st.selectbox("🎯 Career Goal", ["Freelancing", "Job", "Remote Job", "Startup", "Side Hustle"], key="sb_goal")
    region = st.selectbox("🌍 Market", ["Pakistan", "Global", "Both"], key="sb_region")
    time_commitment = st.selectbox("⏳ Time/Week", ["5-10 hours", "10-20 hours", "20+ hours"], key="sb_time")
    st.divider()
    st.info("💡 **Pro Tip:** In 2026, proof of work (GitHub/Portfolio) beats a resume every time.")

# -----------------------
# AI LOGIC
# -----------------------
def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a brutally honest and practical career strategist."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

# -----------------------
# MAIN UI
# -----------------------
if app_mode == "Single Skill Roadmap":
    st.title("🚀 Skill Advisor AI Pro+")
    st.markdown("### Your personal career roadmap engine")
    
    skill = st.text_input("🔍 Enter Skill", placeholder="e.g. AI Engineering", key="single_skill_input")

    if st.button("Generate Plan", key="btn_single"):
        if skill.strip():
            with st.spinner("Analyzing market..."):
                prompt = f"""
                Provide a detailed career roadmap for {skill}.
                Learner Level: {level}
                Goal: {goal}
                Market: {region}
                Time: {time_commitment}/week
                
                Include: Step-by-step roadmap, Global/Pakistan Salary, Best Resources with links, and a Risk level.
                """
                result = get_ai_response(prompt)
                st.markdown(result)
        else:
            st.warning("Please enter a skill.")

else:
    st.title("⚔️ Skill & Course Comparison")
    st.markdown("### Side-by-side analysis of your options")
    
    col1, col2 = st.columns(2)
    with col1:
        item_a = st.text_input("Option A (Skill/Course)", placeholder="e.g. React.js", key="compare_a")
    with col2:
        item_b = st.text_input("Option B (Skill/Course)", placeholder="e.g. Next.js", key="compare_b")

    if st.button("⚔️ Start Comparison", key="btn_compare"):
        if item_a.strip() and item_b.strip():
            with st.spinner(f"Comparing {item_a} vs {item_b}..."):
                compare_prompt = f"""
                Compare these two items side-by-side for a {level} level learner aiming for {goal} in {region}:
                1: {item_a}
                2: {item_b}

                Please provide a side-by-side table, Pros & Cons for each, and a final verdict based on {time_commitment}/week.
                """
                comparison_result = get_ai_response(compare_prompt)
                st.divider()
                st.markdown(comparison_result)
        else:
            st.warning("⚠️ Please fill in both options.")

# -----------------------
# FOOTER
# -----------------------
st.divider()
st.caption("🚀 Built for Hackathon Domination | Stable Build v2.1")    st.divider()
    level = st.selectbox("📊 Current Level", ["Beginner", "Intermediate", "Advanced"])
    goal = st.selectbox("🎯 Career Goal", ["Freelancing", "Job", "Remote Job", "Startup"])
    region = st.selectbox("🌍 Market", ["Pakistan", "Global", "Both"])
    time_commitment = st.selectbox("⏳ Time/Week", ["5-10 hours", "10-20 hours", "20+ hours"])

# -----------------------
# AI LOGIC
# -----------------------
def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a brutally honest and practical career strategist."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1200,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# -----------------------
# MAIN UI - SINGLE MODE
# -----------------------
if app_mode == "Single Skill Roadmap":
    st.title("🚀 Skill Advisor AI Pro+")
    skill = st.text_input("🔍 Enter Skill", placeholder="e.g. AI Engineering")

    if st.button("Generate Roadmap"):
        if skill.strip():
            with st.spinner("Analyzing market..."):
                prompt = f"Provide a roadmap for {skill} at {level} level for a {goal} in {region}."
                result = get_ai_response(prompt)
                st.markdown(result)
        else:
            st.warning("Please enter a skill.")

# -----------------------
# MAIN UI - COMPARE MODE
# -----------------------
else:
    st.title("⚔️ Skill & Course Comparison")
    st.markdown("### Side-by-side analysis of your learning options")
    
    col1, col2 = st.columns(2)
    with col1:
        item_a = st.text_input("Option A (Skill or Course)", placeholder="e.g. React.js")
    with col2:
        item_b = st.text_input("Option B (Skill or Course)", placeholder="e.g. Next.js")

    if st.button("⚔️ Start Comparison"):
        if item_a.strip() and item_b.strip():
            with st.spinner(f"Comparing {item_a} vs {item_b}..."):
                compare_prompt = f"""
                Compare these two items side-by-side for a {level} level learner aiming for {goal} in {region}:
                1: {item_a}
                2: {item_b}

                Please provide:
                ### ⚖️ Side-by-Side Comparison Table
                (Compare: Learning Difficulty, Time to Mastery, Market Demand, Salary Potential)

                ### ✅ Pros & Cons
                - **{item_a}**: Pros vs Cons
                - **{item_b}**: Pros vs Cons

                ### 💰 ROI Analysis
                Which one gets a {goal} faster in the current {region} market?

                ### 🏆 The Verdict
                Based on {time_commitment}/week, which one should the user pick first?
                """
                comparison_result = get_ai_response(compare_prompt)
                
                st.divider()
                st.markdown(comparison_result)
        else:
            st.warning("⚠️ Please fill in both options to compare.")

# -----------------------
# FOOTER
# -----------------------
st.divider()
st.caption("🚀 Built for Hackathon Domination | Comparison Engine v2.0")# -----------------------
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
