import streamlit as st
import os
import datetime
from huggingface_hub import InferenceClient

# ─────────────────────────────────────────────
# PAGE CONFIG (must be first)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Skills Advisor AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
MODEL_ID    = "meta-llama/Meta-Llama-3-8B-Instruct"
MAX_TOKENS  = 1600
TEMPERATURE = 0.7

MODES = [
    "🗺️ Skill Roadmap",
    "⚔️ Compare Skills",
    "📡 Market Intel",
    "🧠 AI Career Coach",
    "📝 Resume Keywords",
]

LEVELS     = ["Beginner", "Intermediate", "Advanced"]
GOALS      = ["Freelancing", "Remote Job", "Local Job", "Startup", "Side Hustle"]
REGIONS    = ["Pakistan", "Global", "Both"]
TIME_SLOTS = ["5–10 hrs/week", "10–20 hrs/week", "20+ hrs/week"]

THEMES = {
    "Midnight": {
        "bg":         "#080B12",
        "sidebar_bg": "#0C0F1A",
        "card_bg":    "#111827",
        "border":     "#1F2A45",
        "accent":     "#6366F1",
        "accent2":    "#8B5CF6",
        "text":       "#E2E8F0",
        "muted":      "#64748B",
        "tag_bg":     "#1E2A45",
        "tag_text":   "#A5B4FC",
        "gradient":   "linear-gradient(135deg,#6366F1 0%,#8B5CF6 100%)",
    },
    "Aurora": {
        "bg":         "#050E14",
        "sidebar_bg": "#071018",
        "card_bg":    "#0A1A22",
        "border":     "#0F2D3D",
        "accent":     "#06B6D4",
        "accent2":    "#22D3EE",
        "text":       "#E0F7FA",
        "muted":      "#546E7A",
        "tag_bg":     "#0F2D3D",
        "tag_text":   "#67E8F9",
        "gradient":   "linear-gradient(135deg,#06B6D4 0%,#0891B2 100%)",
    },
    "Ember": {
        "bg":         "#0D0A08",
        "sidebar_bg": "#120E0A",
        "card_bg":    "#1A1208",
        "border":     "#2D1F0E",
        "accent":     "#F97316",
        "accent2":    "#FB923C",
        "text":       "#FEF3C7",
        "muted":      "#78716C",
        "tag_bg":     "#2D1F0E",
        "tag_text":   "#FED7AA",
        "gradient":   "linear-gradient(135deg,#F97316 0%,#EF4444 100%)",
    },
    "Sage": {
        "bg":         "#F8FAF9",
        "sidebar_bg": "#F0F4F2",
        "card_bg":    "#FFFFFF",
        "border":     "#D1E0D8",
        "accent":     "#059669",
        "accent2":    "#10B981",
        "text":       "#1A2E25",
        "muted":      "#6B7280",
        "tag_bg":     "#D1FAE5",
        "tag_text":   "#065F46",
        "gradient":   "linear-gradient(135deg,#059669 0%,#10B981 100%)",
    },
    "Arctic": {
        "bg":         "#F0F4F8",
        "sidebar_bg": "#E8EEF4",
        "card_bg":    "#FFFFFF",
        "border":     "#CBD5E1",
        "accent":     "#3B82F6",
        "accent2":    "#6366F1",
        "text":       "#0F172A",
        "muted":      "#64748B",
        "tag_bg":     "#DBEAFE",
        "tag_text":   "#1E40AF",
        "gradient":   "linear-gradient(135deg,#3B82F6 0%,#6366F1 100%)",
    },
}

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for k, v in {
    "theme":       "Midnight",
    "history":     [],
    "saved":       [],
    "last_result": "",
    "mode":        "🗺️ Skill Roadmap",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.theme not in THEMES:
    st.session_state.theme = "Midnight"
T = THEMES[st.session_state.theme]

# ─────────────────────────────────────────────
# DYNAMIC CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Literata:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}
html, body, [class*="css"] {{
    font-family: 'Literata', Georgia, serif;
    color: {T['text']};
}}
.stApp {{
    background: {T['bg']};
    background-image:
        radial-gradient(ellipse at 15% 15%, {T['accent']}18 0%, transparent 45%),
        radial-gradient(ellipse at 85% 85%, {T['accent2']}10 0%, transparent 45%);
    min-height: 100vh;
}}
[data-testid="stSidebar"] {{
    background: {T['sidebar_bg']} !important;
    border-right: 1px solid {T['border']} !important;
}}
[data-testid="stSidebar"] * {{ color: {T['text']} !important; }}

h1 {{
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.4rem !important;
    letter-spacing: -1.5px !important;
    background: {T['gradient']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0 !important;
    line-height: 1.1 !important;
}}
h2, h3, h4 {{
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    color: {T['text']} !important;
    letter-spacing: -0.5px !important;
}}
[data-testid="stMetric"] {{
    background: {T['card_bg']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 16px !important;
    padding: 18px 20px !important;
    box-shadow: 0 2px 16px rgba(0,0,0,0.1) !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}}
[data-testid="stMetric"]:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(0,0,0,0.18) !important;
}}
[data-testid="stMetricLabel"] {{
    color: {T['muted']} !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    font-family: 'Syne', sans-serif !important;
}}
[data-testid="stMetricValue"] {{
    color: {T['text']} !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
}}
div.stButton > button:first-child {{
    background: {T['gradient']} !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    width: 100% !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    letter-spacing: 0.3px !important;
    padding: 0.65rem 1.1rem !important;
    transition: all 0.25s cubic-bezier(.4,0,.2,1) !important;
    box-shadow: 0 4px 14px {T['accent']}45 !important;
}}
div.stButton > button:first-child:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px {T['accent']}65 !important;
    filter: brightness(1.1) !important;
}}
div.stButton > button:first-child:active {{
    transform: translateY(0) !important;
}}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {{
    background: {T['card_bg']} !important;
    border: 1px solid {T['border']} !important;
    color: {T['text']} !important;
    border-radius: 10px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {T['accent']} !important;
    box-shadow: 0 0 0 3px {T['accent']}28 !important;
}}
.stSelectbox > div > div > div {{
    background: {T['card_bg']} !important;
    border: 1px solid {T['border']} !important;
    color: {T['text']} !important;
    border-radius: 10px !important;
}}
.stRadio label {{
    background: {T['card_bg']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 10px !important;
    padding: 8px 14px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
}}
.stRadio label:hover {{
    border-color: {T['accent']} !important;
    background: {T['accent']}15 !important;
}}
[data-testid="stExpander"] {{
    background: {T['card_bg']} !important;
    border: 1px solid {T['border']} !important;
    border-radius: 12px !important;
}}
.stAlert {{ border-radius: 12px !important; }}
.stSpinner > div {{ border-top-color: {T['accent']} !important; }}
hr {{ border-color: {T['border']} !important; margin: 18px 0 !important; }}

/* ── Custom components ── */
.hero-wrap {{
    background: {T['card_bg']};
    border: 1px solid {T['border']};
    border-radius: 20px;
    padding: 30px 36px 28px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}}
.hero-wrap::after {{
    content: '';
    position: absolute;
    width: 260px; height: 260px;
    top: -80px; right: -80px;
    background: {T['gradient']};
    border-radius: 50%;
    opacity: 0.07;
    pointer-events: none;
}}
.mode-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: {T['accent']}20;
    border: 1px solid {T['accent']}45;
    color: {T['accent']};
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.76rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    letter-spacing: 0.04em;
    margin-bottom: 10px;
}}
.hero-sub {{
    color: {T['muted']};
    font-size: 1rem;
    font-style: italic;
    margin-top: 5px;
}}
.result-box {{
    background: {T['card_bg']};
    border: 1px solid {T['border']};
    border-top: 3px solid {T['accent']};
    border-radius: 16px;
    padding: 28px 32px;
    margin-top: 18px;
    line-height: 1.85;
    box-shadow: 0 4px 24px rgba(0,0,0,0.14);
    animation: fadeUp 0.4s ease forwards;
}}
@keyframes fadeUp {{
    from {{ opacity:0; transform:translateY(14px); }}
    to   {{ opacity:1; transform:translateY(0); }}
}}
.slabel {{
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {T['accent']};
    margin-bottom: 8px;
}}
.pill {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: {T['tag_bg']};
    color: {T['tag_text']};
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 0.78rem;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    margin: 3px 2px;
}}
.sidelogo {{
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.25rem;
    background: {T['gradient']};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.sidetag {{
    font-size: 0.7rem;
    color: {T['muted']};
    letter-spacing: 0.06em;
    text-transform: uppercase;
}}
.saved-card {{
    background: {T['card_bg']};
    border: 1px solid {T['border']};
    border-left: 3px solid {T['accent']};
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
    transition: all 0.2s;
}}
.saved-card:hover {{
    box-shadow: 0 4px 20px {T['accent']}22;
    transform: translateX(3px);
}}
.saved-title {{ font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.9rem; color: {T['text']}; }}
.saved-meta  {{ font-size: 0.75rem; color: {T['muted']}; margin-top: 2px; }}
.hist-item {{
    background: {T['card_bg']};
    border: 1px solid {T['border']};
    border-radius: 8px;
    padding: 9px 13px;
    font-size: 0.82rem;
    color: {T['muted']};
    margin-bottom: 6px;
    line-height: 1.5;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AI CLIENT
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_client():
    token = os.getenv("HF_TOKEN")
    if not token:
        return None
    return InferenceClient(model=MODEL_ID, token=token)

client = get_client()
if client is None:
    st.error("❌ **HF_TOKEN not found.** Set it in your environment variables and restart.")
    st.stop()

# ─────────────────────────────────────────────
# AI HELPERS
# ─────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a brutally honest, data-driven career strategist specialising in tech skills "
    "and the Pakistani & global freelance market. Be specific, actionable, and direct. "
    "Use clear markdown with ## headers, bullet points, and **bold** key terms. "
    "Include real numbers (salaries, timeframes) wherever possible."
)

def build_messages(prompt: str) -> list[dict]:
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in st.session_state.history[-4:]:
        msgs.append(turn)
    msgs.append({"role": "user", "content": prompt})
    return msgs

def stream_ai(prompt: str):
    try:
        stream = client.chat.completions.create(
            messages=build_messages(prompt),
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            stream=True,
        )
        full = ""
        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta.content
            if delta is None:
                continue
            full += delta
            yield delta
        st.session_state.history.append({"role": "user",      "content": prompt})
        st.session_state.history.append({"role": "assistant", "content": full})
        st.session_state.last_result = full
    except Exception as e:
        yield f"\n\n❌ **AI Error:** {e}"

def get_ai(prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            messages=build_messages(prompt),
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        result = resp.choices[0].message.content
        st.session_state.history.append({"role": "user",      "content": prompt})
        st.session_state.history.append({"role": "assistant", "content": result})
        st.session_state.last_result = result
        return result
    except Exception as e:
        return f"❌ **AI Error:** {e}"

def save_result(title: str, mode: str, content: str):
    st.session_state.saved.insert(0, {
        "title":   title,
        "mode":    mode,
        "content": content,
        "time":    datetime.datetime.now().strftime("%b %d, %H:%M"),
    })

# ─────────────────────────────────────────────
# PROMPTS
# ─────────────────────────────────────────────
def p_roadmap(skill, level, goal, region, time):
    return f"""Career roadmap for **{skill}** | Level: {level} | Goal: {goal} | Market: {region} | {time}

## 🗺️ Overview
2-3 sentence pitch + estimated weeks/months to job-ready.

## 📅 Learning Phases
4 phases: Foundation → Core → Advanced → Portfolio. Each: duration, 3-5 topics, concrete milestone.

## 💰 Salary & Rates
Pakistan (PKR/month) + Global (USD/year) + Upwork/Fiverr hourly rate.

## 📚 Best Resources
7 resources with URLs. Free first, paid second. One sentence WHY each is the best choice.

## ⚠️ Risk Assessment
Risk level (Low/Medium/High) + 3 honest risks + mitigation strategies.

## ✅ First 7 Days
Day-by-day action plan. Concrete tasks, not vague advice.

## 🏆 Success Checkpoints
5 measurable milestones that prove you're job-ready."""

def p_compare(a, b, level, goal, region, time):
    return f"""Compare **{a}** vs **{b}** | {level} | {goal} | {region} | {time}

## 📊 Comparison Table
Markdown table: Learning Curve | Job Demand | Freelance Market | Avg Salary PK | Avg Salary Global | Time to Hire | Future Outlook

## 💚 {a} — Strengths (3), Weaknesses (3), Best use case

## 💜 {b} — Strengths (3), Weaknesses (3), Best use case

## 🏆 Verdict
Clear winner for THIS person. 3-4 sentences. No fence-sitting.

## 🔗 Synergy
Rate 1–10: is it worth learning both? Why?"""

def p_market(skill, level, goal, region, time):
    return f"""Market intelligence for **{skill}** | {region} | {level} | {goal} | {time}

## 📈 Demand Trend
Growing/Stable/Declining? YoY change. Why?

## 🏢 Top 10 Employers
Mix of Pakistan + global remote. What they pay + what they want.

## 💼 Target Job Titles
6-8 titles with: salary, experience needed, top required skills.

## 🔑 Must-Have Stack
Complementary skills ranked by importance (tools, frameworks, soft skills).

## 📣 Where to Find Work
Platforms, communities, hashtags, networking tactics for {region}. Include 3 unconventional tactics.

## 📉 Candidate Killers
Top 5 mistakes that get resumes rejected instantly.

## 🔮 2-Year Outlook
More or less valuable? Adjacent skills to learn now."""

def p_coach(question, level, goal, region, time):
    return f"""I am a {level} learner targeting {goal} in {region}. Available: {time}.

Question: {question}

Give me direct career coaching:
- Direct answer to my question
- 2-3 things I might not have considered  
- A next step I can take TODAY
- A reality check if my expectations are off

Be a mentor, not a cheerleader. Be honest."""

def p_resume(skill, level, goal, region, time):
    return f"""ATS-optimised resume kit for **{skill}** | {level} | {goal} | {region} | {time}

## 🎯 Power Keywords
Top 20 ATS keywords. Mark the top 5 as CRITICAL.

## 📝 Skills Section
Ready-to-paste skills section (Technical, Tools, Soft Skills).

## 💼 Bullet Point Templates
8 STAR-format bullet templates with placeholders [X%], [N users], etc.

## 🔍 LinkedIn Optimisation
5 headline keywords + About section opening paragraph template.

## 📧 Cold Outreach Template
One cold email/DM template for {goal}.

## ⚡ Quick Wins
3 highest-impact profile additions to do this week."""

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div class="sidelogo">⚡ Skills Advisor AI</div>'
        '<div class="sidetag">Your career intelligence engine</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Theme switcher
    st.markdown('<div class="slabel">🎨 Theme</div>', unsafe_allow_html=True)
    chosen = st.selectbox(
        "Theme", list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme),
        label_visibility="collapsed",
        key="theme_sel",
    )
    if chosen != st.session_state.theme:
        st.session_state.theme = chosen
        st.rerun()

    # Color swatches
    swatches = "".join(
        f'<div title="{n}" style="width:18px;height:18px;border-radius:50%;'
        f'background:{t["accent"]};display:inline-block;margin:2px;'
        f'{"outline:2px solid white;outline-offset:2px;" if n==st.session_state.theme else ""}"></div>'
        for n, t in THEMES.items()
    )
    st.markdown(f'<div style="margin:6px 0 16px">{swatches}</div>', unsafe_allow_html=True)
    st.divider()

    # Navigation
    st.markdown('<div class="slabel">📌 Mode</div>', unsafe_allow_html=True)
    nav = st.radio("Mode", MODES,
                   index=MODES.index(st.session_state.mode),
                   label_visibility="collapsed",
                   key="nav_radio")
    if nav != st.session_state.mode:
        st.session_state.mode = nav
        st.rerun()
    st.divider()

    # Profile
    st.markdown('<div class="slabel">👤 Your Profile</div>', unsafe_allow_html=True)
    level           = st.selectbox("Level",     LEVELS,     key="sb_level")
    goal            = st.selectbox("Goal",      GOALS,      key="sb_goal")
    region          = st.selectbox("Market",    REGIONS,    key="sb_region")
    time_commitment = st.selectbox("Time/Week", TIME_SLOTS, key="sb_time")

    st.markdown(
        f'<div style="margin-top:10px">'
        f'<span class="pill">🎓 {level}</span>'
        f'<span class="pill">🎯 {goal}</span>'
        f'<span class="pill">🌍 {region}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    # Stats
    turns = len(st.session_state.history) // 2
    c1, c2 = st.columns(2)
    c1.metric("Sessions", turns)
    c2.metric("Saved", len(st.session_state.saved))

    st.divider()
    if st.button("🗑️ Clear History", key="btn_clr"):
        st.session_state.history = []
        st.session_state.last_result = ""
        st.success("✅ Cleared")

    with st.expander("💡 Career Tips 2026"):
        st.markdown(f"""
<div style="color:{T['muted']};font-size:0.82rem;line-height:1.8">

🚀 **Portfolio beats resume.** Always ship.

💼 **Niche on Upwork.** "Python dev" loses. "Python ETL for SaaS" wins.

🇵🇰 **PK Stack:** Fiverr → Upwork → LinkedIn → Cold email.

🐙 **GitHub = your background check.** Green squares matter.

📢 **Learn in public.** One X thread/week brings clients.

⏱️ **Speed of execution** separates earners from learners.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
HERO_META = {
    "🗺️ Skill Roadmap":   ("🗺️ Skill Roadmap",   "Personalised, phase-by-phase learning plans for any tech skill."),
    "⚔️ Compare Skills":  ("⚔️ Compare Skills",  "Side-by-side analysis — pick the right skill, not the hyped one."),
    "📡 Market Intel":    ("📡 Market Intel",    "Real hiring data, salary ranges, and demand trends."),
    "🧠 AI Career Coach": ("🧠 AI Career Coach", "Ask anything — get direct, no-fluff career guidance."),
    "📝 Resume Keywords": ("📝 Resume Keywords", "ATS keywords, bullet templates, and LinkedIn copy — ready to paste."),
}
badge, sub = HERO_META[st.session_state.mode]
st.markdown(f"""
<div class="hero-wrap">
    <div class="mode-badge">● ACTIVE MODE: {badge}</div>
    <h1>Skills Advisor AI</h1>
    <div class="hero-sub">{sub}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# RENDER HELPER
# ─────────────────────────────────────────────
def render_stream(prompt: str, title: str, mode: str):
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    area = st.empty()
    text = ""
    for chunk in stream_ai(prompt):
        text += chunk
        area.markdown(text + "▌")
    area.markdown(text)
    st.markdown('</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("💾 Save Result", key=f"save_{mode}"):
            save_result(title, mode, text)
            st.success("✅ Saved to library!")
    with col_b:
        with st.expander("📋 Copy Raw Text"):
            st.code(text, language=None)

# ─────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────

# ── ROADMAP ────────────────────────────────
if st.session_state.mode == "🗺️ Skill Roadmap":
    col_in, col_btn = st.columns([4, 1])
    with col_in:
        skill = st.text_input("Skill", placeholder="e.g. AI Engineering, Flutter, DevOps, Web3…",
                              label_visibility="collapsed", key="r_skill")
    with col_btn:
        go = st.button("Generate →", key="btn_r")

    st.markdown('<div class="slabel" style="margin-top:14px">⚡ Quick picks</div>', unsafe_allow_html=True)
    picks = ["AI Engineering", "Flutter", "DevOps", "Data Science", "Web3", "Prompt Engineering"]
    pcols = st.columns(len(picks))
    for i, p in enumerate(picks):
        if pcols[i].button(p, key=f"p{i}"):
            skill, go = p, True

    if go:
        if not skill or not skill.strip():
            st.warning("⚠️ Enter or select a skill.")
        else:
            s = skill.strip()
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Skill", s); m2.metric("Level", level)
            m3.metric("Goal", goal); m4.metric("Market", region)
            st.markdown(f"### 📋 Roadmap: {s}")
            render_stream(p_roadmap(s, level, goal, region, time_commitment),
                          f"Roadmap: {s}", "roadmap")

# ── COMPARE ────────────────────────────────
elif st.session_state.mode == "⚔️ Compare Skills":
    c1, c2 = st.columns(2)
    with c1: item_a = st.text_input("Option A", placeholder="e.g. React.js", key="ca")
    with c2: item_b = st.text_input("Option B", placeholder="e.g. Vue.js",   key="cb")

    st.markdown('<div class="slabel" style="margin-top:10px">⚡ Popular battles</div>', unsafe_allow_html=True)
    battles = [("React vs Vue","React.js","Vue.js"),("Flutter vs RN","Flutter","React Native"),
               ("Python vs JS","Python","JavaScript"),("AWS vs GCP","AWS","Google Cloud")]
    bcols = st.columns(len(battles))
    for i,(lbl,a,b) in enumerate(battles):
        if bcols[i].button(lbl, key=f"b{i}"):
            item_a, item_b = a, b

    if st.button("⚔️ Run Comparison →", key="btn_cmp"):
        if not item_a.strip() or not item_b.strip():
            st.warning("⚠️ Fill in both options.")
        else:
            m1, m2, m3 = st.columns(3)
            m1.metric("Option A", item_a); m2.metric("Option B", item_b); m3.metric("Goal", goal)
            st.markdown(f"### ⚔️ {item_a.strip()} vs {item_b.strip()}")
            with st.spinner(f"Comparing…"):
                result = get_ai(p_compare(item_a.strip(), item_b.strip(), level, goal, region, time_commitment))
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div>', unsafe_allow_html=True)
            ca, cb = st.columns(2)
            with ca:
                if st.button("💾 Save", key="save_cmp"):
                    save_result(f"Compare: {item_a} vs {item_b}", "compare", result)
                    st.success("✅ Saved!")
            with cb:
                with st.expander("📋 Copy Raw Text"):
                    st.code(result, language=None)

# ── MARKET INTEL ───────────────────────────
elif st.session_state.mode == "📡 Market Intel":
    skill = st.text_input("Skill to research",
                          placeholder="e.g. LLM Fine-tuning, Kubernetes, Rust, MLOps…",
                          key="ms")

    hot = ["LLM Fine-tuning","Kubernetes","Rust","Data Engineering","Cybersecurity","MLOps"]
    st.markdown('<div class="slabel" style="margin-top:10px">🔥 Hot right now</div>', unsafe_allow_html=True)
    hcols = st.columns(len(hot))
    for i, h in enumerate(hot):
        if hcols[i].button(h, key=f"h{i}"):
            skill = h

    if st.button("🔍 Run Intel Report →", key="btn_mi"):
        if not skill.strip():
            st.warning("⚠️ Enter a skill to research.")
        else:
            s = skill.strip()
            st.markdown(f"### 📡 Market Report: {s}")
            render_stream(p_market(s, level, goal, region, time_commitment),
                          f"Intel: {s}", "market")

# ── AI CAREER COACH ────────────────────────
elif st.session_state.mode == "🧠 AI Career Coach":
    question = st.text_area(
        "Your question",
        placeholder="e.g. I've been learning Python for 3 months. Should I start applying or build more projects?",
        height=110, key="coach_q",
    )

    starters = ["Am I ready to freelance?","How do I get my first Upwork client?",
                 "Should I get a certification?","How to negotiate my first salary?"]
    st.markdown('<div class="slabel" style="margin-top:10px">💬 Starter questions</div>', unsafe_allow_html=True)
    scols = st.columns(len(starters))
    for i, sq in enumerate(starters):
        if scols[i].button(sq, key=f"sq{i}"):
            question = sq

    if st.button("🧠 Get Coaching →", key="btn_cch"):
        if not question.strip():
            st.warning("⚠️ Ask me anything about your career.")
        else:
            st.markdown("### 🧠 Career Coach Response")
            render_stream(p_coach(question.strip(), level, goal, region, time_commitment),
                          f"Coach: {question[:40]}…", "coach")

    if st.session_state.history:
        st.divider()
        st.markdown('<div class="slabel">📜 Recent Conversation</div>', unsafe_allow_html=True)
        for turn in reversed(st.session_state.history[-6:]):
            icon = "🧠" if turn["role"] == "assistant" else "👤"
            preview = turn["content"][:200] + ("…" if len(turn["content"]) > 200 else "")
            st.markdown(f'<div class="hist-item"><strong>{icon}</strong> {preview}</div>',
                        unsafe_allow_html=True)

# ── RESUME KEYWORDS ────────────────────────
elif st.session_state.mode == "📝 Resume Keywords":
    skill = st.text_input("Target role / skill",
                          placeholder="e.g. Full Stack Developer, ML Engineer, DevOps…",
                          key="res_s")

    targets = ["Full Stack Dev","ML Engineer","DevOps Engineer","Data Analyst","Mobile Dev"]
    st.markdown('<div class="slabel" style="margin-top:10px">🎯 Common targets</div>', unsafe_allow_html=True)
    tcols = st.columns(len(targets))
    for i, tg in enumerate(targets):
        if tcols[i].button(tg, key=f"tg{i}"):
            skill = tg

    if st.button("📝 Generate Resume Kit →", key="btn_res"):
        if not skill.strip():
            st.warning("⚠️ Enter a skill or job title.")
        else:
            s = skill.strip()
            m1, m2, m3 = st.columns(3)
            m1.metric("Role", s); m2.metric("Market", region); m3.metric("Goal", goal)
            st.markdown(f"### 📝 Resume Kit: {s}")
            render_stream(p_resume(s, level, goal, region, time_commitment),
                          f"Resume: {s}", "resume")

# ─────────────────────────────────────────────
# SAVED LIBRARY
# ─────────────────────────────────────────────
if st.session_state.saved:
    st.divider()
    st.markdown("## 📚 Saved Library")
    cols = st.columns(min(len(st.session_state.saved), 3))
    for i, entry in enumerate(st.session_state.saved[:6]):
        with cols[i % 3]:
            st.markdown(f"""
<div class="saved-card">
  <div class="saved-title">{entry['title']}</div>
  <div class="saved-meta">🕐 {entry['time']} · {entry['mode'].upper()}</div>
</div>""", unsafe_allow_html=True)
            with st.expander("View", expanded=False):
                st.markdown(entry["content"])
    if st.button("🗑️ Clear Library", key="btn_cls"):
        st.session_state.saved = []
        st.rerun()
