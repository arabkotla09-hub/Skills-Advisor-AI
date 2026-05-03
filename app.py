import streamlit as st
import os
import datetime
import random
from huggingface_hub import InferenceClient

# ═══════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Skills Advisor AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════
MODEL_ID    = "meta-llama/Meta-Llama-3-8B-Instruct"
MAX_TOKENS  = 1600
TEMPERATURE = 0.7

MODES = [
    "⚡ Skill Roadmap",
    "⚔️ Skill Battle",
    "📡 Market Radar",
    "🧠 Career Coach",
    "💀 Roast My Skills",
    "🎲 Surprise Me",
    "💰 Salary Oracle",
    "📝 Resume Kit",
]

LEVELS     = ["Beginner", "Intermediate", "Advanced"]
GOALS      = ["Freelancing", "Remote Job", "Local Job", "Startup", "Side Hustle"]
REGIONS    = ["Pakistan", "Global", "Both"]
TIME_SLOTS = ["5–10 hrs/week", "10–20 hrs/week", "20+ hrs/week"]

THEMES = {
    "Void":    {"bg":"#03040A","sb":"#06080F","card":"#0A0D18","border":"#141D35","acc":"#00F5FF","acc2":"#7B2FFF","text":"#E8F4FD","muted":"#4A5568","tag_bg":"#0D1530","tag_t":"#00F5FF","grad":"linear-gradient(135deg,#00F5FF,#7B2FFF)","glow":"0 0 40px #00F5FF30"},
    "Blood":   {"bg":"#080305","sb":"#0D0408","card":"#120609","border":"#2A0A10","acc":"#FF2D55","acc2":"#FF6B35","text":"#FFF0F3","muted":"#6B4550","tag_bg":"#200810","tag_t":"#FF2D55","grad":"linear-gradient(135deg,#FF2D55,#FF6B35)","glow":"0 0 40px #FF2D5530"},
    "Matrix":  {"bg":"#000A00","sb":"#010D01","card":"#021002","border":"#0A2A0A","acc":"#00FF41","acc2":"#39FF14","text":"#CCFFCC","muted":"#2D6B2D","tag_bg":"#011501","tag_t":"#00FF41","grad":"linear-gradient(135deg,#00FF41,#39FF14)","glow":"0 0 40px #00FF4130"},
    "Gold":    {"bg":"#0A0800","sb":"#0F0A00","card":"#181200","border":"#2E2000","acc":"#FFD700","acc2":"#FF8C00","text":"#FFF8DC","muted":"#6B5B00","tag_bg":"#1A1400","tag_t":"#FFD700","grad":"linear-gradient(135deg,#FFD700,#FF8C00)","glow":"0 0 40px #FFD70030"},
    "Rose":    {"bg":"#FDF4F7","sb":"#F8E8EF","card":"#FFFFFF","border":"#F0C8D8","acc":"#E91E8C","acc2":"#9B27AF","text":"#1A0A10","muted":"#9B7080","tag_bg":"#FCE4EC","tag_t":"#880E4F","grad":"linear-gradient(135deg,#E91E8C,#9B27AF)","glow":"0 0 30px #E91E8C25"},
    "Arctic":  {"bg":"#F0F7FF","sb":"#E4F0FF","card":"#FFFFFF","border":"#C5DDF5","acc":"#0066FF","acc2":"#00CCFF","text":"#001833","muted":"#607D8B","tag_bg":"#E3F2FD","tag_t":"#01579B","grad":"linear-gradient(135deg,#0066FF,#00CCFF)","glow":"0 0 30px #0066FF25"},
}

SURPRISE_SKILLS = [
    "Quantum Computing","Neuro-Linguistic Programming","Web3 Gaming","AI Agent Development",
    "Robotics Process Automation","Blockchain Forensics","AR/VR Development","Bioinformatics",
    "Algorithmic Trading","Digital Forensics","Voice AI / Conversational AI","Edge Computing",
    "MLOps","Synthetic Media / Deepfake Detection","Space Tech Software","DAO Development",
]

ROAST_OPENERS = [
    "Oh honey…", "Bless your heart.", "I've seen better plans on a fortune cookie.",
    "Let me be brutally, painfully honest:", "Sir/Ma'am, we need to talk.",
    "I don't say this lightly, but:", "Okay. Deep breath. Here we go:",
]

# ═══════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════
for k, v in {
    "theme": "Void", "history": [], "saved": [],
    "last_result": "", "mode": "⚡ Skill Roadmap",
    "xp": 0, "streak": 0, "queries_today": 0,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.theme not in THEMES:
    st.session_state.theme = "Void"

T = THEMES[st.session_state.theme]

# ═══════════════════════════════════════════════════════
# CSS — RADICAL REDESIGN
# ═══════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap');

:root {{
  --bg:      {T['bg']};
  --sb:      {T['sb']};
  --card:    {T['card']};
  --border:  {T['border']};
  --acc:     {T['acc']};
  --acc2:    {T['acc2']};
  --text:    {T['text']};
  --muted:   {T['muted']};
  --grad:    {T['grad']};
  --glow:    {T['glow']};
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; }}

html, body, [class*="css"] {{
  font-family: 'Cormorant Garamond', Georgia, serif;
  color: var(--text);
  -webkit-font-smoothing: antialiased;
}}

/* ── App bg with animated grid ── */
.stApp {{
  background: var(--bg);
  background-image:
    linear-gradient(var(--border) 1px, transparent 1px),
    linear-gradient(90deg, var(--border) 1px, transparent 1px);
  background-size: 40px 40px;
  background-position: center center;
  min-height: 100vh;
  position: relative;
}}
.stApp::before {{
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 50% at 20% 20%, {T['acc']}12 0%, transparent 60%),
    radial-gradient(ellipse 50% 60% at 80% 80%, {T['acc2']}0E 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
  background: var(--sb) !important;
  border-right: 1px solid var(--border) !important;
  backdrop-filter: blur(12px) !important;
}}
[data-testid="stSidebar"] * {{ color: var(--text) !important; }}

/* ── Typography ── */
h1 {{
  font-family: 'Rajdhani', sans-serif !important;
  font-weight: 700 !important;
  font-size: 3rem !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
  line-height: 1 !important;
  background: var(--grad);
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
  filter: drop-shadow(0 0 20px {T['acc']}60) !important;
}}
h2 {{
  font-family: 'Rajdhani', sans-serif !important;
  font-weight: 600 !important;
  font-size: 1.5rem !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  color: var(--acc) !important;
}}
h3, h4 {{
  font-family: 'Rajdhani', sans-serif !important;
  font-weight: 600 !important;
  letter-spacing: 0.5px !important;
  color: var(--text) !important;
}}
p, li {{
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 1.05rem !important;
  line-height: 1.8 !important;
}}
code, pre, .stCode {{
  font-family: 'JetBrains Mono', monospace !important;
}}

/* ── Metric cards ── */
[data-testid="stMetric"] {{
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-top: 2px solid var(--acc) !important;
  border-radius: 4px !important;
  padding: 16px 18px !important;
  box-shadow: var(--glow) !important;
  transition: all 0.3s cubic-bezier(.4,0,.2,1) !important;
  position: relative !important;
  overflow: hidden !important;
}}
[data-testid="stMetric"]::after {{
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: var(--grad);
  opacity: 0.6;
}}
[data-testid="stMetric"]:hover {{
  transform: translateY(-3px) !important;
  box-shadow: var(--glow), 0 12px 40px rgba(0,0,0,0.3) !important;
}}
[data-testid="stMetricLabel"] {{
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.65rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.15em !important;
  color: var(--muted) !important;
}}
[data-testid="stMetricValue"] {{
  font-family: 'Rajdhani', sans-serif !important;
  font-weight: 700 !important;
  font-size: 1.3rem !important;
  color: var(--acc) !important;
}}

/* ── Buttons ── */
div.stButton > button:first-child {{
  background: transparent !important;
  color: var(--acc) !important;
  border: 1px solid var(--acc) !important;
  border-radius: 2px !important;
  width: 100% !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.82rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  padding: 0.7rem 1.2rem !important;
  transition: all 0.2s ease !important;
  position: relative !important;
  overflow: hidden !important;
  box-shadow: inset 0 0 0 0 var(--acc) !important;
}}
div.stButton > button:first-child::before {{
  content: '';
  position: absolute;
  inset: 0;
  background: var(--grad);
  opacity: 0;
  transition: opacity 0.2s ease;
  z-index: -1;
}}
div.stButton > button:first-child:hover {{
  color: var(--bg) !important;
  background: var(--acc) !important;
  box-shadow: var(--glow) !important;
  transform: translateY(-1px) !important;
  border-color: var(--acc) !important;
}}
div.stButton > button:first-child:active {{
  transform: translateY(1px) !important;
}}

/* ── Text inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {{
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-bottom: 2px solid var(--acc) !important;
  color: var(--text) !important;
  border-radius: 2px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.9rem !important;
  transition: all 0.2s !important;
  padding: 10px 14px !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
  border-color: var(--acc) !important;
  box-shadow: 0 4px 20px {T['acc']}30 !important;
  outline: none !important;
}}
.stTextInput > label, .stTextArea > label {{
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.7rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.12em !important;
  color: var(--muted) !important;
}}

/* ── Selectbox ── */
.stSelectbox > div > div > div {{
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-bottom: 2px solid var(--acc) !important;
  color: var(--text) !important;
  border-radius: 2px !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.85rem !important;
}}

/* ── Radio ── */
.stRadio > div {{ gap: 4px !important; }}
.stRadio label {{
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-left: 3px solid transparent !important;
  border-radius: 2px !important;
  padding: 8px 14px !important;
  cursor: pointer !important;
  transition: all 0.15s !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.78rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.05em !important;
  color: var(--muted) !important;
}}
.stRadio label:hover {{
  border-left-color: var(--acc) !important;
  color: var(--acc) !important;
  background: {T['acc']}0A !important;
}}
.stRadio label[data-testid*="checked"],
.stRadio label:has(input:checked) {{
  border-left-color: var(--acc) !important;
  color: var(--acc) !important;
  background: {T['acc']}12 !important;
}}

/* ── Expander ── */
[data-testid="stExpander"] {{
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 2px !important;
}}

/* ── Alerts ── */
.stAlert {{ border-radius: 2px !important; border-left: 3px solid var(--acc) !important; }}

/* ── Spinner ── */
.stSpinner > div {{ border-top-color: var(--acc) !important; }}

/* ── Divider ── */
hr {{ border-color: var(--border) !important; margin: 16px 0 !important; }}

/* ════════════════════════════════════
   CUSTOM COMPONENTS
   ════════════════════════════════════ */

/* Terminal header bar */
.terminal-bar {{
  background: var(--card);
  border: 1px solid var(--border);
  border-bottom: none;
  border-radius: 4px 4px 0 0;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}}
.dot {{ width:12px;height:12px;border-radius:50%;display:inline-block; }}
.dot-r{{background:#FF5F57;}} .dot-y{{background:#FFBD2E;}} .dot-g{{background:#28C840;}}
.terminal-title {{
  font-family:'JetBrains Mono',monospace;
  font-size:0.72rem;
  color:var(--muted);
  letter-spacing:0.1em;
  margin-left:8px;
  text-transform:uppercase;
}}

/* Hero */
.hero-shell {{
  border: 1px solid var(--border);
  border-top: 2px solid var(--acc);
  background: var(--card);
  padding: 36px 40px 30px;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
}}
.hero-shell::before {{
  content:'';
  position:absolute;
  top:-100px;right:-100px;
  width:300px;height:300px;
  background:var(--grad);
  border-radius:50%;
  opacity:0.05;
  pointer-events:none;
}}
.hero-corner {{
  position:absolute;
  top:12px;right:16px;
  font-family:'JetBrains Mono',monospace;
  font-size:0.65rem;
  color:var(--muted);
  letter-spacing:0.1em;
}}
.hero-eyebrow {{
  font-family:'JetBrains Mono',monospace;
  font-size:0.7rem;
  letter-spacing:0.2em;
  text-transform:uppercase;
  color:var(--acc);
  margin-bottom:10px;
  display:flex;
  align-items:center;
  gap:8px;
}}
.hero-eyebrow::before {{
  content:'';
  width:24px;height:1px;
  background:var(--acc);
  display:inline-block;
}}
.hero-sub {{
  font-family:'Cormorant Garamond',serif;
  font-style:italic;
  font-size:1.1rem;
  color:var(--muted);
  margin-top:6px;
  line-height:1.6;
}}

/* Result box — terminal style */
.result-shell {{
  margin-top: 20px;
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow: hidden;
  box-shadow: var(--glow);
  animation: emerge 0.5s cubic-bezier(.4,0,.2,1) forwards;
}}
@keyframes emerge {{
  from {{ opacity:0; transform:translateY(20px) scale(0.98); }}
  to   {{ opacity:1; transform:translateY(0) scale(1); }}
}}
.result-body {{
  background: var(--card);
  padding: 28px 32px;
  line-height: 1.85;
  font-family:'Cormorant Garamond',serif;
  font-size:1.05rem;
}}

/* XP Bar */
.xp-track {{
  background: var(--border);
  border-radius: 999px;
  height: 4px;
  overflow: hidden;
  margin: 6px 0 12px;
}}
.xp-fill {{
  height: 100%;
  background: var(--grad);
  border-radius: 999px;
  box-shadow: var(--glow);
  transition: width 0.8s cubic-bezier(.4,0,.2,1);
}}

/* Chips */
.chip {{
  display:inline-flex;align-items:center;gap:5px;
  background:var(--card);
  border:1px solid var(--border);
  color:var(--acc);
  border-radius:2px;
  padding:4px 12px;
  font-size:0.72rem;
  font-family:'JetBrains Mono',monospace;
  font-weight:700;
  margin:2px;
  letter-spacing:0.06em;
  text-transform:uppercase;
  transition:all 0.15s;
}}

/* Section label */
.sec-label {{
  font-family:'JetBrains Mono',monospace;
  font-size:0.62rem;
  font-weight:700;
  letter-spacing:0.2em;
  text-transform:uppercase;
  color:var(--muted);
  margin-bottom:8px;
  display:flex;align-items:center;gap:8px;
}}
.sec-label::after {{
  content:'';flex:1;height:1px;
  background:var(--border);
}}

/* Sidebar logo */
.sidelogo {{
  font-family:'Rajdhani',sans-serif;
  font-weight:700;
  font-size:1.4rem;
  letter-spacing:3px;
  text-transform:uppercase;
  background:var(--grad);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
  filter:drop-shadow(0 0 12px {T['acc']}50);
}}
.sidetag {{
  font-family:'JetBrains Mono',monospace;
  font-size:0.62rem;
  color:var(--muted);
  letter-spacing:0.15em;
  text-transform:uppercase;
  margin-top:2px;
}}

/* Saved card */
.saved-card {{
  background:var(--card);
  border:1px solid var(--border);
  border-left:2px solid var(--acc);
  padding:14px 16px;
  margin-bottom:8px;
  transition:all 0.2s;
  cursor:pointer;
}}
.saved-card:hover {{
  box-shadow:var(--glow);
  transform:translateX(4px);
}}
.saved-title {{
  font-family:'Rajdhani',sans-serif;
  font-weight:700;
  font-size:0.95rem;
  letter-spacing:0.5px;
  color:var(--text);
}}
.saved-meta {{
  font-family:'JetBrains Mono',monospace;
  font-size:0.65rem;
  color:var(--muted);
  margin-top:3px;
  letter-spacing:0.05em;
}}

/* Salary Oracle */
.oracle-ring {{
  width:160px;height:160px;
  border-radius:50%;
  background:var(--card);
  border:2px solid var(--acc);
  display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  margin:16px auto;
  box-shadow:var(--glow),inset 0 0 30px {T['acc']}15;
  position:relative;
}}
.oracle-val {{
  font-family:'Rajdhani',sans-serif;
  font-weight:700;
  font-size:1.6rem;
  color:var(--acc);
  line-height:1;
}}
.oracle-unit {{
  font-family:'JetBrains Mono',monospace;
  font-size:0.65rem;
  color:var(--muted);
  text-transform:uppercase;
  letter-spacing:0.1em;
  margin-top:4px;
}}

/* Scanline overlay */
.stApp::after {{
  content:'';
  position:fixed;
  inset:0;
  background:repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.03) 2px,
    rgba(0,0,0,0.03) 4px
  );
  pointer-events:none;
  z-index:9999;
}}

/* Glitch animation for logo */
@keyframes glitch {{
  0%,100%{{text-shadow:none}}
  20%{{text-shadow:-2px 0 {T['acc2']},2px 0 {T['acc']}}}
  40%{{text-shadow:2px 0 {T['acc2']},-2px 0 {T['acc']}}}
  60%{{text-shadow:none}}
}}

/* Pulse dot */
@keyframes pulse-dot {{
  0%,100%{{opacity:1;transform:scale(1)}}
  50%{{opacity:0.4;transform:scale(0.8)}}
}}
.live-dot {{
  width:8px;height:8px;border-radius:50%;
  background:var(--acc);
  display:inline-block;
  animation:pulse-dot 1.5s infinite;
  box-shadow:0 0 8px var(--acc);
  margin-right:6px;
}}

/* History chip */
.hist-chip {{
  background:var(--card);
  border:1px solid var(--border);
  padding:8px 12px;
  font-family:'JetBrains Mono',monospace;
  font-size:0.75rem;
  color:var(--muted);
  margin-bottom:6px;
  border-left:2px solid var(--border);
  transition:border-color 0.2s;
}}
.hist-chip:hover {{ border-left-color:var(--acc); color:var(--text); }}

/* Surprise skill card */
.surprise-card {{
  background: var(--card);
  border: 1px solid var(--acc);
  padding: 24px;
  text-align: center;
  box-shadow: var(--glow);
  animation: emerge 0.6s ease forwards;
}}
.surprise-skill {{
  font-family:'Rajdhani',sans-serif;
  font-size:2rem;
  font-weight:700;
  color:var(--acc);
  letter-spacing:2px;
  text-transform:uppercase;
}}

/* Roast box */
.roast-box {{
  background: var(--card);
  border: 2px solid {T['acc']};
  padding: 28px 32px;
  margin-top: 18px;
  position: relative;
  box-shadow: var(--glow);
  animation: emerge 0.5s ease forwards;
}}
.roast-opener {{
  font-family:'Rajdhani',sans-serif;
  font-size:1.4rem;
  font-weight:700;
  color:var(--acc);
  letter-spacing:1px;
  margin-bottom:12px;
  text-transform:uppercase;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width:4px; }}
::-webkit-scrollbar-track {{ background:var(--bg); }}
::-webkit-scrollbar-thumb {{ background:var(--border); border-radius:2px; }}
::-webkit-scrollbar-thumb:hover {{ background:var(--acc); }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# AI CLIENT
# ═══════════════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def get_client():
    token = os.getenv("HF_TOKEN")
    if not token:
        return None
    return InferenceClient(model=MODEL_ID, token=token)

client = get_client()
if client is None:
    st.error("⚡ HF_TOKEN not found. Set it in your environment variables.")
    st.stop()

# ═══════════════════════════════════════════════════════
# AI HELPERS
# ═══════════════════════════════════════════════════════
SYSTEM = (
    "You are a brutally honest, data-driven career strategist for tech skills "
    "and the Pakistani & global freelance market. Be specific and direct. "
    "Use clear markdown: ## headers, **bold** key terms, bullet points. "
    "Always include real numbers: salaries, timeframes, market statistics."
)

def build_msgs(prompt):
    msgs = [{"role":"system","content":SYSTEM}]
    for t in st.session_state.history[-4:]:
        msgs.append(t)
    msgs.append({"role":"user","content":prompt})
    return msgs

def stream_ai(prompt):
    try:
        s = client.chat.completions.create(
            messages=build_msgs(prompt), max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE, stream=True,
        )
        full = ""
        for chunk in s:
            if not chunk.choices: continue
            d = chunk.choices[0].delta.content
            if d is None: continue
            full += d
            yield d
        st.session_state.history.append({"role":"user","content":prompt})
        st.session_state.history.append({"role":"assistant","content":full})
        st.session_state.last_result = full
        st.session_state.xp += 50
        st.session_state.queries_today += 1
    except Exception as e:
        yield f"\n\n❌ **Error:** {e}"

def get_ai(prompt):
    try:
        r = client.chat.completions.create(
            messages=build_msgs(prompt), max_tokens=MAX_TOKENS, temperature=TEMPERATURE,
        )
        res = r.choices[0].message.content
        st.session_state.history.append({"role":"user","content":prompt})
        st.session_state.history.append({"role":"assistant","content":res})
        st.session_state.last_result = res
        st.session_state.xp += 50
        st.session_state.queries_today += 1
        return res
    except Exception as e:
        return f"❌ **Error:** {e}"

def save_result(title, mode, content):
    st.session_state.saved.insert(0,{
        "title":title,"mode":mode,"content":content,
        "time":datetime.datetime.now().strftime("%b %d · %H:%M"),
    })
    st.session_state.xp += 20

# ═══════════════════════════════════════════════════════
# PROMPTS
# ═══════════════════════════════════════════════════════
def p_roadmap(skill,level,goal,region,time):
    return f"""Career roadmap for **{skill}** | {level} | {goal} | {region} | {time}

## ⚡ Overview
2–3 sentence pitch. Estimated weeks to first dollar / first job.

## 📅 Phases
Foundation → Core → Advanced → Portfolio (4 phases).
Each: duration, 3–5 topics, one concrete deliverable milestone.

## 💰 Money Reality
Pakistan PKR/month range. Global USD/year. Upwork/Fiverr hourly.
Include entry-level AND senior figures.

## 📚 Best 7 Resources
With URLs. Free first, paid second. One LINE on why each beats alternatives.

## ⚠️ Risk File
Rating: Low / Medium / High.
Three specific risks for this skill + mitigation for each.

## ✅ Day 1–7 Battle Plan
Concrete daily tasks. No vague advice.

## 🏆 Readiness Checklist
5 measurable "I'm ready" checkpoints."""

def p_compare(a,b,level,goal,region,time):
    return f"""Compare **{a}** vs **{b}** | {level} | {goal} | {region} | {time}

## 📊 Head-to-Head Table
Markdown table: Learning Curve | Job Demand 2025 | Freelance Market |
Avg Salary PK | Avg Salary Global | Time to Hire | 2027 Outlook

## ⚡ {a} — Strengths (3) · Weaknesses (3) · Best For

## ⚡ {b} — Strengths (3) · Weaknesses (3) · Best For

## 🏆 Verdict
Definitive winner for THIS profile. No hedging.

## 🔗 Combo Value
Rate 1–10: is learning both worth it? Specific synergies."""

def p_market(skill,level,goal,region,time):
    return f"""Market intelligence: **{skill}** | {region} | {level} | {goal} | {time}

## 📈 Demand Signal
Growing/Stable/Declining? YoY %. Concrete evidence.

## 🏢 Top 10 Employers
Mix: Pakistan + global remote. Pay range + requirements per company.

## 💼 Job Title Map
6–8 titles. Salary | experience needed | top 3 required skills each.

## 🔑 Must-Have Stack
Complementary skills ranked. Tools, frameworks, soft skills. Be specific.

## 📣 Hunt Locations
Platforms, Slack/Discord communities, hashtags for {region}.
3 unconventional tactics others aren't using.

## 📉 Instant Rejection Triggers
Top 5 resume/profile mistakes. Be blunt.

## 🔮 2026–2027 Signal
More or less valuable? Adjacent skills to learn NOW."""

def p_roast(skills,level,goal,region,time):
    opener = random.choice(ROAST_OPENERS)
    return f"""You are a brutally honest (but ultimately helpful) career roast comedian + strategist.

Roast this person's skill choices and career trajectory with wit and savage honesty,
but END with a genuine, actionable rescue plan.

Their profile:
- Skills/situation: {skills}
- Level: {level} | Goal: {goal} | Market: {region} | Time: {time}

Start with: "{opener}"

Structure:
## 🔥 The Roast
3–4 paragraphs of savage, specific, funny critique. Reference real market data.
Call out specific mistakes, outdated skills, or unrealistic expectations.

## 💀 The Hard Truth
One brutal paragraph. The thing they KNOW but won't admit.

## 🚀 The Rescue Plan
Okay, now actually help them. 5 specific actions they can take this week.
End with one sentence of genuine encouragement."""

def p_surprise(skill,level,goal,region,time):
    return f"""The skill: **{skill}** (randomly assigned!)

{level} learner | {goal} | {region} | {time}

Make this exciting. Why is **{skill}** actually a MASSIVE opportunity right now
that most people are sleeping on?

## 🎲 Why This Skill Is Gold Right Now
Market reality + why the timing is perfect.

## ⚡ Fast-Track Plan
6-week sprint to get employable/billable in {skill}.

## 💰 The Money Numbers
Realistic income for {region}. Best-case and worst-case.

## 🌍 Who's Hiring
3–5 specific companies or client types actively paying for {skill}.

## 🎯 Your First Win
The ONE thing to build/do in week 1 to validate this direction."""

def p_coach(question,level,goal,region,time):
    return f"""Career coaching | {level} | {goal} | {region} | {time}

Question: {question}

Give direct, personalised mentorship:
## 🎯 Direct Answer
No preamble. Answer the question.

## 🔍 What You're Missing
2–3 angles they haven't considered.

## ⚡ Do This Today
One concrete action executable in the next 24 hours.

## 💊 Reality Check
If expectations are off, say so clearly. Be a mentor not a cheerleader."""

def p_resume(skill,level,goal,region,time):
    return f"""ATS resume kit: **{skill}** | {level} | {goal} | {region} | {time}

## 🎯 Critical Keywords
Top 20 ATS keywords. Mark top 5 as ⚡ CRITICAL.

## 📝 Skills Block
Ready-to-paste (Technical · Tools · Soft Skills).

## 💼 Bullet Templates
8 STAR-format bullets with [X%] / [N users] placeholders.

## 🔍 LinkedIn Optimisation
5 headline keywords + About section opening paragraph.

## 📧 Cold Outreach Template
One punchy cold email/DM for {goal}.

## ⚡ This-Week Wins
3 profile changes with highest ROI."""

def p_salary(skill, level, region, years_exp, has_portfolio, has_cert):
    portfolio_str = "has a strong portfolio" if has_portfolio else "no portfolio yet"
    cert_str = "has relevant certifications" if has_cert else "no certifications"
    return f"""Salary estimation for **{skill}**

Profile: {level} | {region} | {years_exp} years experience | {portfolio_str} | {cert_str}

Give a precise salary analysis:

## 💰 Your Estimated Range
Specific PKR/month (if Pakistan or Both) AND USD/year (if Global or Both).
Give: Floor · Target · Ceiling

## 📊 What Moves the Number
List 5 specific factors that could increase salary by 20–50%.

## 🎯 Negotiation Script
Exact words to use when negotiating. Specific to {region}.

## ⚡ 90-Day Salary Boost Plan
3 specific actions in 90 days to justify a raise/higher rate.

## 🌍 Geographic Arbitrage
If in Pakistan: exact platforms and strategies to earn USD while living in PKR."""

# ═══════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════
with st.sidebar:
    now = datetime.datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
<div class="sidelogo">SKILLS.AI</div>
<div class="sidetag">Career Intelligence Terminal · v4.0</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # XP System
    xp = st.session_state.xp
    level_num = xp // 500 + 1
    xp_in_level = xp % 500
    xp_pct = int((xp_in_level / 500) * 100)
    st.markdown(f"""
<div class="sec-label">⚡ Career XP · LVL {level_num}</div>
<div class="xp-track"><div class="xp-fill" style="width:{xp_pct}%"></div></div>
<div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:var(--muted);margin-bottom:12px">
  {xp_in_level}/500 XP to next level · Total: {xp} XP
</div>
""", unsafe_allow_html=True)

    st.divider()

    # Theme
    st.markdown('<div class="sec-label">🎨 Theme</div>', unsafe_allow_html=True)
    chosen = st.selectbox("Theme", list(THEMES.keys()),
                          index=list(THEMES.keys()).index(st.session_state.theme),
                          label_visibility="collapsed", key="theme_sel")
    if chosen != st.session_state.theme:
        st.session_state.theme = chosen
        st.rerun()

    swatches = "".join(
        f'<div title="{n}" style="width:16px;height:16px;border-radius:2px;'
        f'background:{t["acc"]};display:inline-block;margin:2px;'
        f'{"outline:2px solid white;outline-offset:2px;" if n==st.session_state.theme else ""}"></div>'
        for n,t in THEMES.items()
    )
    st.markdown(f'<div style="margin:6px 0 14px">{swatches}</div>', unsafe_allow_html=True)
    st.divider()

    # Navigation
    st.markdown('<div class="sec-label">▶ Navigation</div>', unsafe_allow_html=True)
    nav = st.radio("Mode", MODES,
                   index=MODES.index(st.session_state.mode) if st.session_state.mode in MODES else 0,
                   label_visibility="collapsed", key="nav_radio")
    if nav != st.session_state.mode:
        st.session_state.mode = nav
        st.rerun()
    st.divider()

    # Profile
    st.markdown('<div class="sec-label">◈ Profile Config</div>', unsafe_allow_html=True)
    level           = st.selectbox("Level",     LEVELS,     key="sb_level")
    goal            = st.selectbox("Goal",      GOALS,      key="sb_goal")
    region          = st.selectbox("Market",    REGIONS,    key="sb_region")
    time_commitment = st.selectbox("Time/Week", TIME_SLOTS, key="sb_time")

    st.markdown(f"""
<div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:4px">
  <span class="chip">🎓 {level}</span>
  <span class="chip">🎯 {goal}</span>
  <span class="chip">🌍 {region}</span>
</div>""", unsafe_allow_html=True)
    st.divider()

    # Stats
    turns = len(st.session_state.history) // 2
    c1,c2 = st.columns(2)
    c1.metric("Sessions", turns)
    c2.metric("Saved", len(st.session_state.saved))

    st.divider()
    if st.button("⟳ Clear History", key="btn_clr"):
        st.session_state.history = []
        st.session_state.last_result = ""
        st.success("✅ Memory wiped.")

    with st.expander("// TIPS.md"):
        st.markdown(f"""
<div style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:var(--muted);line-height:2">

→ Portfolio > Resume. Always.

→ Niche wins. "Python ETL for SaaS" beats "Python dev".

→ PK Stack: Fiverr → Upwork → LinkedIn → Cold DM.

→ GitHub green = your real background check.

→ 1 X/Twitter thread/week = inbound clients.

→ Speed of execution is the only moat.

→ <span style="color:var(--acc)">+50 XP</span> per query. Level up.
</div>
""", unsafe_allow_html=True)

    st.markdown(f"""
<div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:var(--muted);margin-top:16px;text-align:center;letter-spacing:0.1em">
<span class="live-dot"></span> ONLINE · {now}
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════
HERO = {
    "⚡ Skill Roadmap":  ("SKILL ROADMAP",   "Phase-by-phase learning plans. No fluff. Pure signal."),
    "⚔️ Skill Battle":  ("SKILL BATTLE",    "Side-by-side war: pick the right weapon, not the trendy one."),
    "📡 Market Radar":  ("MARKET RADAR",    "Live hiring intelligence, salary data, and demand signals."),
    "🧠 Career Coach":  ("CAREER COACH",    "Direct, personalised mentorship. Ask anything."),
    "💀 Roast My Skills":("SKILL ROAST",    "Brutal honesty about your career choices. Then a rescue plan."),
    "🎲 Surprise Me":   ("SURPRISE SKILL",  "Spin the wheel. Discover your next unexpected career move."),
    "💰 Salary Oracle": ("SALARY ORACLE",   "Precise salary intelligence calibrated to your exact profile."),
    "📝 Resume Kit":    ("RESUME KIT",      "ATS-optimised keywords and bullets. Copy. Paste. Win."),
}
title, subtitle = HERO.get(st.session_state.mode, ("SKILLS.AI", ""))

st.markdown(f"""
<div class="hero-shell">
  <div class="hero-corner">[ SYS:ONLINE · XP:{st.session_state.xp} ]</div>
  <div class="hero-eyebrow">SKILLS ADVISOR AI · {st.session_state.mode}</div>
  <h1>{title}</h1>
  <div class="hero-sub">{subtitle}</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# RENDER HELPER
# ═══════════════════════════════════════════════════════
def render_stream(prompt, save_title, save_mode):
    st.markdown('<div class="result-shell"><div class="terminal-bar"><span class="dot dot-r"></span><span class="dot dot-y"></span><span class="dot dot-g"></span><span class="terminal-title">OUTPUT STREAM</span></div><div class="result-body">', unsafe_allow_html=True)
    area = st.empty()
    text = ""
    for chunk in stream_ai(prompt):
        text += chunk
        area.markdown(text + "▌")
    area.markdown(text)
    st.markdown('</div></div>', unsafe_allow_html=True)

    ca, cb = st.columns(2)
    with ca:
        if st.button("💾 Save to Library", key=f"save_{save_mode}_{random.randint(0,9999)}"):
            save_result(save_title, save_mode, text)
            st.success(f"✅ Saved! +20 XP")
    with cb:
        with st.expander("{ } Raw Output"):
            st.code(text, language="markdown")

# ═══════════════════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════════════════

# ── SKILL ROADMAP ───────────────────────────────────
if st.session_state.mode == "⚡ Skill Roadmap":
    ci, cb_btn = st.columns([4,1])
    with ci:
        skill = st.text_input("SKILL", placeholder="e.g. AI Engineering, DevOps, Web3, Flutter…",
                              label_visibility="visible", key="r_skill")
    with cb_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        go = st.button("EXECUTE →", key="btn_r")

    st.markdown('<div class="sec-label" style="margin-top:16px">⚡ Quick Launch</div>', unsafe_allow_html=True)
    picks = ["AI Engineering","Flutter","DevOps","Data Science","Web3","Prompt Eng","Cybersecurity","MLOps"]
    pcols = st.columns(len(picks))
    for i,p in enumerate(picks):
        if pcols[i].button(p, key=f"p{i}"):
            skill, go = p, True

    if go and skill and skill.strip():
        s = skill.strip()
        m1,m2,m3,m4 = st.columns(4)
        m1.metric("TARGET SKILL", s); m2.metric("LEVEL", level)
        m3.metric("GOAL", goal); m4.metric("MARKET", region)
        render_stream(p_roadmap(s,level,goal,region,time_commitment), f"Roadmap: {s}", "roadmap")

# ── SKILL BATTLE ────────────────────────────────────
elif st.session_state.mode == "⚔️ Skill Battle":
    c1,c2 = st.columns(2)
    with c1: item_a = st.text_input("CHALLENGER A", placeholder="e.g. React.js", key="ca")
    with c2: item_b = st.text_input("CHALLENGER B", placeholder="e.g. Vue.js",   key="cb")

    st.markdown('<div class="sec-label" style="margin-top:12px">⚡ Classic Battles</div>', unsafe_allow_html=True)
    battles = [("React vs Vue","React.js","Vue.js"),("Flutter vs RN","Flutter","React Native"),
               ("Python vs JS","Python","JavaScript"),("AWS vs GCP","AWS","Google Cloud"),
               ("FastAPI vs Django","FastAPI","Django"),("Next vs Nuxt","Next.js","Nuxt.js")]
    bcols = st.columns(3)
    for i,(lbl,a,b) in enumerate(battles):
        if bcols[i%3].button(lbl, key=f"b{i}"):
            item_a, item_b = a, b

    if st.button("⚔️ BEGIN BATTLE →", key="btn_cmp"):
        if item_a.strip() and item_b.strip():
            m1,m2,m3 = st.columns(3)
            m1.metric("FIGHTER A", item_a); m2.metric("FIGHTER B", item_b); m3.metric("ARENA", region)
            with st.spinner("Analysing combatants…"):
                result = get_ai(p_compare(item_a.strip(),item_b.strip(),level,goal,region,time_commitment))
            st.markdown('<div class="result-shell"><div class="terminal-bar"><span class="dot dot-r"></span><span class="dot dot-y"></span><span class="dot dot-g"></span><span class="terminal-title">BATTLE REPORT</span></div><div class="result-body">', unsafe_allow_html=True)
            st.markdown(result)
            st.markdown('</div></div>', unsafe_allow_html=True)
            ca2,cb2 = st.columns(2)
            with ca2:
                if st.button("💾 Save", key="save_cmp"):
                    save_result(f"Battle: {item_a} vs {item_b}","compare",result)
                    st.success("✅ Saved! +20 XP")
            with cb2:
                with st.expander("{ } Raw Output"):
                    st.code(result, language="markdown")
        else:
            st.warning("⚠️ Both fighters required.")

# ── MARKET RADAR ────────────────────────────────────
elif st.session_state.mode == "📡 Market Radar":
    skill = st.text_input("TARGET SKILL", placeholder="e.g. LLM Fine-tuning, Kubernetes, Rust…", key="ms")

    hot = ["LLM Fine-tuning","Kubernetes","Rust","Data Engineering","Cybersecurity","MLOps","Solidity","Edge AI"]
    st.markdown('<div class="sec-label" style="margin-top:12px">🔥 Hot Signals</div>', unsafe_allow_html=True)
    hcols = st.columns(4)
    for i,h in enumerate(hot):
        if hcols[i%4].button(h, key=f"h{i}"):
            skill = h

    if st.button("📡 SCAN MARKET →", key="btn_mi"):
        if skill.strip():
            m1,m2,m3 = st.columns(3)
            m1.metric("SKILL", skill.strip()); m2.metric("REGION", region); m3.metric("GOAL", goal)
            render_stream(p_market(skill.strip(),level,goal,region,time_commitment), f"Intel: {skill}", "market")
        else:
            st.warning("⚠️ Enter a skill to scan.")

# ── CAREER COACH ────────────────────────────────────
elif st.session_state.mode == "🧠 Career Coach":
    question = st.text_area("YOUR QUESTION", placeholder="e.g. I've been learning Python for 3 months. Should I start applying or build more projects first?",
                            height=100, key="coach_q")

    starters = ["Am I ready to freelance?","How do I land my first Upwork client?",
                 "Should I get certified?","How do I negotiate my first salary?"]
    st.markdown('<div class="sec-label" style="margin-top:12px">💬 Starters</div>', unsafe_allow_html=True)
    scols = st.columns(2)
    for i,sq in enumerate(starters):
        if scols[i%2].button(sq, key=f"sq{i}"):
            question = sq

    if st.button("🧠 CONSULT →", key="btn_cch"):
        if question.strip():
            render_stream(p_coach(question.strip(),level,goal,region,time_commitment),
                          f"Coach: {question[:40]}…","coach")
        else:
            st.warning("⚠️ Ask me something.")

    if st.session_state.history:
        st.divider()
        st.markdown('<div class="sec-label">📜 Memory Log</div>', unsafe_allow_html=True)
        for turn in reversed(st.session_state.history[-6:]):
            icon = "AI ›" if turn["role"]=="assistant" else "YOU ›"
            preview = turn["content"][:180] + ("…" if len(turn["content"])>180 else "")
            st.markdown(f'<div class="hist-chip"><strong>{icon}</strong> {preview}</div>', unsafe_allow_html=True)

# ── ROAST MY SKILLS ─────────────────────────────────
elif st.session_state.mode == "💀 Roast My Skills":
    st.markdown(f"""
<div style="background:var(--card);border:1px solid var(--border);border-left:3px solid {T['acc']};
padding:16px 20px;margin-bottom:20px;font-family:'JetBrains Mono',monospace;font-size:0.8rem;color:var(--muted)">
⚠️ WARNING: This mode delivers <span style="color:{T['acc']};font-weight:700">brutal, honest critique</span>
of your career choices — followed by a real rescue plan. Thick skin required.
</div>
""", unsafe_allow_html=True)

    skills_input = st.text_area(
        "YOUR SKILLS / SITUATION",
        placeholder="e.g. I know basic HTML/CSS and started Python 6 months ago. I want to freelance but have no clients. I keep switching between tutorials without finishing anything.",
        height=120, key="roast_input",
    )

    if st.button("💀 ROAST ME →", key="btn_roast"):
        if skills_input.strip():
            opener = random.choice(ROAST_OPENERS)
            st.markdown(f'<div class="roast-opener">{opener}</div>', unsafe_allow_html=True)
            render_stream(p_roast(skills_input.strip(),level,goal,region,time_commitment),
                          f"Roast: {skills_input[:30]}…","roast")
        else:
            st.warning("⚠️ Describe your situation to get roasted.")

# ── SURPRISE ME ─────────────────────────────────────
elif st.session_state.mode == "🎲 Surprise Me":
    st.markdown(f"""
<div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.1rem;
color:var(--muted);margin-bottom:20px;line-height:1.7">
The algorithm will assign you a random skill from the frontier of tech.
Your job: take it seriously for the next 5 minutes.
You might discover your next career move.
</div>
""", unsafe_allow_html=True)

    if "surprise_skill" not in st.session_state:
        st.session_state.surprise_skill = None

    if st.button("🎲 SPIN THE WHEEL →", key="btn_spin"):
        st.session_state.surprise_skill = random.choice(SURPRISE_SKILLS)

    if st.session_state.surprise_skill:
        sk = st.session_state.surprise_skill
        st.markdown(f"""
<div class="surprise-card">
  <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:var(--muted);letter-spacing:0.15em;margin-bottom:8px">YOUR ASSIGNED SKILL</div>
  <div class="surprise-skill">{sk}</div>
  <div style="font-family:'Cormorant Garamond',serif;font-style:italic;color:var(--muted);margin-top:8px">Roll with it. It might change your life.</div>
</div>
""", unsafe_allow_html=True)

        c1,c2 = st.columns(2)
        with c1:
            if st.button("⚡ Explore This Skill →", key="btn_explore"):
                render_stream(p_surprise(sk,level,goal,region,time_commitment),
                              f"Surprise: {sk}","surprise")
        with c2:
            if st.button("🎲 Spin Again", key="btn_again"):
                st.session_state.surprise_skill = random.choice(SURPRISE_SKILLS)
                st.rerun()

# ── SALARY ORACLE ───────────────────────────────────
elif st.session_state.mode == "💰 Salary Oracle":
    st.markdown(f"""
<div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.05rem;
color:var(--muted);margin-bottom:20px">
Enter your profile. Get a precise salary estimate calibrated to your exact situation — not generic ranges.
</div>
""", unsafe_allow_html=True)

    col_sk, col_yr = st.columns(2)
    with col_sk:
        sal_skill = st.text_input("SKILL / ROLE", placeholder="e.g. React Developer, Data Scientist…", key="sal_s")
    with col_yr:
        years_exp = st.selectbox("YEARS EXPERIENCE", ["0 (Fresh)","1","2","3","4","5+","8+","10+"], key="sal_yr")

    col_p, col_c = st.columns(2)
    with col_p:
        has_portfolio = st.checkbox("I have a portfolio / GitHub", key="sal_port")
    with col_c:
        has_cert = st.checkbox("I have relevant certifications", key="sal_cert")

    if st.button("💰 CONSULT THE ORACLE →", key="btn_sal"):
        if sal_skill.strip():
            # Show animated oracle ring
            sal_display = sal_skill.strip()
            st.markdown(f"""
<div style="text-align:center;margin:16px 0">
  <div class="oracle-ring">
    <div class="oracle-val">{region}</div>
    <div class="oracle-unit">analysing…</div>
  </div>
</div>
""", unsafe_allow_html=True)
            render_stream(
                p_salary(sal_skill.strip(),level,region,years_exp,has_portfolio,has_cert),
                f"Salary: {sal_skill}","salary"
            )
        else:
            st.warning("⚠️ Enter a skill or role.")

# ── RESUME KIT ──────────────────────────────────────
elif st.session_state.mode == "📝 Resume Kit":
    skill = st.text_input("TARGET ROLE / SKILL", placeholder="e.g. Full Stack Dev, ML Engineer, DevOps…", key="res_s")

    targets = ["Full Stack Dev","ML Engineer","DevOps Engineer","Data Analyst","Mobile Dev","AI Engineer"]
    st.markdown('<div class="sec-label" style="margin-top:12px">🎯 Common Targets</div>', unsafe_allow_html=True)
    tcols = st.columns(3)
    for i,tg in enumerate(targets):
        if tcols[i%3].button(tg, key=f"tg{i}"):
            skill = tg

    if st.button("📝 GENERATE KIT →", key="btn_res"):
        if skill.strip():
            m1,m2,m3 = st.columns(3)
            m1.metric("ROLE", skill.strip()); m2.metric("MARKET", region); m3.metric("GOAL", goal)
            render_stream(p_resume(skill.strip(),level,goal,region,time_commitment),
                          f"Resume: {skill}","resume")
        else:
            st.warning("⚠️ Enter a role or skill.")

# ═══════════════════════════════════════════════════════
# SAVED LIBRARY
# ═══════════════════════════════════════════════════════
if st.session_state.saved:
    st.divider()
    st.markdown("## SAVED LIBRARY")
    cols = st.columns(min(len(st.session_state.saved),3))
    for i,entry in enumerate(st.session_state.saved[:6]):
        with cols[i%3]:
            st.markdown(f"""
<div class="saved-card">
  <div class="saved-title">{entry['title']}</div>
  <div class="saved-meta">{entry['time']} · {entry['mode'].upper()}</div>
</div>""", unsafe_allow_html=True)
            with st.expander("Open"):
                st.markdown(entry["content"])

    if st.button("⟳ Clear Library", key="btn_cls"):
        st.session_state.saved = []
        st.rerun()
