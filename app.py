import base64
import json
import re
import unicodedata
from pathlib import Path
import streamlit as st

def render_interactive_tools_hub(current_tool: str) -> None:
    tools = [
        {
            "name": "Candidate Market Insight",
            "url": "https://www.hamilton-barnes.com/candidate-market-insight/",
            "what_it_does": "Shows a broader view of candidate-side market trends, hiring movement and skill demand across selected technology areas.",
            "who_its_for": "Useful for candidates planning their next move, as well as clients wanting a clearer sense of talent availability and market direction.",
            "what_data_it_uses": "Uses market trend data, hiring context, and role-specific insight curated around Hamilton Barnes specialisms.",
            "how_to_interpret": "Treat it as a directional market view that helps explain broader movement rather than a fixed prediction.",
            "why_its_useful": "It helps users understand where demand is moving, where talent is tightening, and how the market is changing over time."
        },
        {
            "name": "UK Salary Calculator",
            "url": "https://hamilton-barnes-salary-calculator-uk.streamlit.app/",
            "what_it_does": "Provides an estimated salary benchmark based on role, level, and location selections within the UK market.",
            "who_its_for": "Useful for candidates reviewing their market value and for hiring teams wanting a clearer benchmark for UK salary positioning.",
            "what_data_it_uses": "Uses Hamilton Barnes salary benchmarking inputs, market data, and role-specific compensation trends.",
            "how_to_interpret": "Read the results as a directional benchmark rather than a guaranteed salary outcome, as final packages can vary by company, region, and skillset.",
            "why_its_useful": "It helps users compare expectations more confidently and make more informed hiring or career decisions."
        },
        {
            "name": "Germany Salary Calculator",
            "url": "https://hamilton-barnes-salary-calculator-germany.streamlit.app/",
            "what_it_does": "Provides an estimated salary benchmark based on role, level, and location selections within the German market.",
            "who_its_for": "Useful for candidates exploring their market value in Germany and for hiring teams wanting clearer compensation guidance.",
            "what_data_it_uses": "Uses Hamilton Barnes benchmarking inputs, salary trend data, and role-specific market information relevant to Germany.",
            "how_to_interpret": "Use the figures as a directional guide rather than a final compensation guarantee, as actual offers vary by employer and hiring context.",
            "why_its_useful": "It makes salary benchmarking easier to understand and gives users a more practical view of market positioning."
        },
        {
            "name": "Wayback Machine",
            "url": "https://hamilton-barnes-wayback-machine.streamlit.app/",
            "what_it_does": "Shows how each specialism has evolved over time across market shifts, technical development, talent demand, and investment context.",
            "who_its_for": "Useful for candidates, clients, and anyone wanting a structured year-by-year view of how technology niches have developed.",
            "what_data_it_uses": "Uses curated market context, public source material, and specialism-specific content structured across the decade.",
            "how_to_interpret": "Read it as a directional industry and market view designed to explain change over time rather than provide a fixed forecast.",
            "why_its_useful": "It helps users understand the bigger picture behind each niche and where long-term change has taken place."
        },
    ]

    visible_tools = [tool for tool in tools if tool["name"] != current_tool]

    st.markdown(
        """
        <style>
        .tools-hub-wrap {
            margin-top: 3rem;
        }

        .tools-hub-title {
            text-align: center;
            font-size: 1.65rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .tools-hub-subtitle {
            text-align: center;
            font-size: 0.95rem;
            max-width: 760px;
            margin: 0 auto 1.8rem auto;
            line-height: 1.6;
        }

        .tool-card {
            background: rgba(255, 255, 255, 0.58);
            border: 1px solid rgba(0, 0, 0, 0.08);
            border-radius: 20px;
            padding: 1.2rem 1.2rem 1rem 1.2rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
        }

        .tool-card-title {
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
        }

        .tool-card-section {
            margin-bottom: 0.55rem;
            line-height: 1.55;
            font-size: 0.93rem;
        }

        .tool-card-section strong {
            font-weight: 700;
        }

        .tool-card-link {
            display: inline-block;
            margin-top: 0.8rem;
            padding: 0.38rem 0.95rem;
            border-radius: 999px;
            border: 1px solid #b5c1cf;
            background: transparent;
            color: black !important;
            text-decoration: none !important;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .tool-card-link:hover {
            border-color: #7ac043;
            color: #7ac043 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="tools-hub-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="tools-hub-title">Explore More Interactive Tools</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tools-hub-subtitle">Explore the rest of the Hamilton Barnes interactive toolset below. Each one is designed to help users better understand salary benchmarks, market positioning, or long-term specialism shifts, while making it easier to move between related tools.</div>',
        unsafe_allow_html=True,
    )

    for tool in visible_tools:
        card_html = f"""
        <div class="tool-card">
            <div class="tool-card-title">{tool["name"]}</div>

            <div class="tool-card-section"><strong>What the tool does:</strong> {tool["what_it_does"]}</div>
            <div class="tool-card-section"><strong>Who it’s for:</strong> {tool["who_its_for"]}</div>
            <div class="tool-card-section"><strong>What data it uses:</strong> {tool["what_data_it_uses"]}</div>
            <div class="tool-card-section"><strong>How to interpret the results:</strong> {tool["how_to_interpret"]}</div>
            <div class="tool-card-section"><strong>Why it’s useful:</strong> {tool["why_its_useful"]}</div>

            <a class="tool-card-link" href="{tool["url"]}" target="_blank">Open tool</a>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Page config
st.set_page_config(page_title="Specialism Wayback Machine", layout="centered")

# Styling
st.markdown(
    """
<style>
/* Hide sidebar + transparent header */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; }

/* Centered content container */
.main .block-container {
    max-width: 900px !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-top: 4.5rem !important;
    padding-bottom: 5rem !important;
}

/* Black text */
h1, h2, h3, h4, h5, h6, p, div, span, li {
    color: #000000 !important;
}

/* Tighten spacing */
h2, h3 {
    margin-top: 1.4rem !important;
}

/* Glass card box */
.glass-card {
    background: rgba(255, 255, 255, 0.55);
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 18px;
    padding: 1.3rem 1.5rem;
    margin-top: 0.6rem;
    margin-bottom: 1.6rem;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.06);
}

.glass-card p {
    margin: 0 0 0.9rem 0;
    line-height: 1.6;
}

.glass-card p:last-child {
    margin-bottom: 0;
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------
# Background
# -------------------------------
def set_background(image_path: Path) -> None:
    encoded = base64.b64encode(image_path.read_bytes()).decode()
    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{encoded}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


BASE_DIR = Path(__file__).parent
bg_path = BASE_DIR / "assets" / "bg1.jpg"
if bg_path.exists():
    set_background(bg_path)

# -------------------------------
# Load content.json
# -------------------------------
DATA_PATH = BASE_DIR / "data" / "content.json"
if not DATA_PATH.exists():
    st.error("Missing data/content.json")
    st.stop()

try:
    content = json.loads(DATA_PATH.read_text(encoding="utf-8"))
except Exception as e:
    st.error("content.json is not valid JSON")
    st.code(str(e))
    st.stop()

# -------------------------------
# Runtime cleaner (fix glued text + $ issues)
# -------------------------------
ZERO_WIDTH = dict.fromkeys(map(ord, ["\u200B", "\u200C", "\u200D", "\uFEFF"]), None)

def clean_text(s: str) -> str:
    if not isinstance(s, str):
        return s

    s = unicodedata.normalize("NFKC", s)
    s = s.translate(ZERO_WIDTH)

    # Remove em/en dashes
    s = s.replace("—", "-").replace("–", "-")

    # Escape $ so Streamlit doesn't trigger math mode
    s = s.replace("$", "&#36;")

    # Fix missing space after full stop
    s = re.sub(r"\.([A-Za-z0-9])", r". \1", s)

    # Fix glued digit-letter boundaries
    s = re.sub(r"(\d)([A-Za-z])", r"\1 \2", s)
    s = re.sub(r"([A-Za-z])(\d)", r"\1 \2", s)

    # Fix quarters: "Q 1" -> "Q1" (case-insensitive)
    s = re.sub(r"\bQ\s+([1-4])\b", r"Q\1", s, flags=re.IGNORECASE)
    s = re.sub(r"\bFY\s+(\d{2,4})\b", r"FY\1", s, flags=re.IGNORECASE)  # optional
    
    # Fix in2026
    s = re.sub(r"\bin(?=\d{4}\b)", "in ", s)

    # -----------------------------
    # FIX ALL DECIMAL SPACING
    # "653. 4" → "653.4"
    # "6. 15" → "6.15"
    # -----------------------------
    s = re.sub(r"(\d+)\.\s+(\d+)", r"\1.\2", s)

    # -----------------------------
    # FIX NUMBER + UNIT SPACING
    # "3.7 T" → "3.7T"
    # "653.4 B" → "653.4B"
    # "12.5 %" → "12.5%"
    # -----------------------------
    s = re.sub(r"(\d+(?:\.\d+)?)\s*(T|B|M|K|%)\b", r"\1\2", s)

    # -----------------------------
    # FIX CURRENCY SPACING
    # "$ 3.7T" → "$3.7T"
    # -----------------------------
    s = re.sub(r"\$\s*(\d)", r"$\1", s)

    # -----------------------------
    # FIX AI casing globally
    # -----------------------------
    s = re.sub(r"\bai\b", "AI", s, flags=re.IGNORECASE)

    # Collapse multiple spaces
    s = re.sub(r"[ ]{2,}", " ", s)

    # Re-join common tech tokens that should NOT be split
    # 3G/4G/5G/6G, 5GHz, Q1-Q4, DDoS, SASE, SD-WAN, etc.

    # Join digit + G patterns: "5 G" -> "5G"
    s = re.sub(r"\b([3-6])\s+G\b", r"\1G", s)

    # Join GHz patterns: "5 GHz" -> "5GHz"
    s = re.sub(r"\b(\d+)\s+GHz\b", r"\1GHz", s, flags=re.IGNORECASE)

    # Join quarter tokens: "Q 1" -> "Q1"
    s = re.sub(r"\bQ\s*([1-4])\b", r"Q\1", s, flags=re.IGNORECASE)

    # Fix DDoS: "DDo S" -> "DDoS"
    s = re.sub(r"\bDDo\s+S\b", "DDoS", s)

    # Fix common split acronyms like "S D-W A N" edge cases (light touch)
    s = re.sub(r"\bSD\s*-\s*WAN\b", "SD-WAN", s, flags=re.IGNORECASE)
    s = re.sub(r"\bSASE\b", "SASE", s)  # no-op but keeps intent clear 
    
    return s.strip()

def walk(obj):
    if isinstance(obj, dict):
        return {k: walk(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(v) for v in obj]
    if isinstance(obj, str):
        return clean_text(obj)
    return obj

content = walk(content)

# -------------------------------
# Helper
# -------------------------------
niches = sorted(content.keys())
if not niches:
    st.warning("No specialisms found in content.json")
    st.stop()

def available_years_for(niche: str):
    years_dict = content.get(niche, {}).get("years", {}) or {}
    years = sorted(years_dict.keys(), key=lambda x: int(x) if x.isdigit() else 9999)
    return years

# -------------------------------
# HERO
# -------------------------------
st.title("The Hamilton Barnes Specialism Wayback Machine")
st.markdown("## We heard that 2026 is the new 2016 👀")
st.write(
    "Here is how our tech specialisms fared over the past decade and what it means for the people building them."
)
st.divider()

# -------------------------------
# Controls (Dropdown + Slider)
# -------------------------------
niche = st.selectbox("Choose a Specialism", niches)

years = available_years_for(niche)
numeric_years = sorted([int(y) for y in years if y.isdigit()])

if not numeric_years:
    numeric_years = list(range(2016, 2027))

year = st.slider(
    "Range Slider",
    min_value=min(numeric_years),
    max_value=max(numeric_years),
    value=min(numeric_years),
    step=1
)

year = str(year)

st.markdown(f"## {niche}: {year}")

# -------------------------------
# Sections (Title + Glass Card)
# -------------------------------
SECTION_ORDER = [
    ("market_shift", "Market Shifts"),
    ("technical_shift", "Technical Shifts"),
    ("talent_shift", "Talent Shifts"),
    ("investment", "Investment Contexts 💵"),
]

year_payload = (content.get(niche, {}).get("years", {}) or {}).get(year, {}) or {}

for key, title in SECTION_ORDER:
    blocks = year_payload.get(key, []) or []
    if not blocks:
        continue

    # Title
    st.markdown(f"### {title}")

    # Glass Box
    box_html = '<div class="glass-card">'
    for p in blocks:
        box_html += f"<p>{p}</p>"
    box_html += "</div>"

    st.markdown(box_html, unsafe_allow_html=True)

# -------------------------------
# Conclusion
# -------------------------------
conclusion = year_payload.get("conclusion", []) or []
st. divider()
if conclusion:
    box_html = """
    <div class="glass-card">
        <div style="font-size: 1.4rem; font-weight: 600; margin-bottom: 0.8rem;">
            What this means 🧠
        </div>
    """

    for p in conclusion:
        box_html += f"<p>{p}</p>"

    box_html += "</div>"

    st.markdown(box_html, unsafe_allow_html=True)

st.divider()

buttons = [
    ("Home", "https://www.hamilton-barnes.com/"),
    ("Explore Roles", "https://www.hamilton-barnes.com/jobs"),
    ("Candidates", "https://www.hamilton-barnes.com/candidates"),
    ("Clients", "https://www.hamilton-barnes.com/clients"),
    ("Graduates", "https://www.empowering-future-network-engineers.com/")
]
st.markdown(
    "<h3 style='text-align: center;'>Explore Hamilton Barnes 🌳</h3>",
    unsafe_allow_html=True
)

for label, url in buttons:
    st.markdown(
        f"""
        <a href="{url}" target="_blank">
            <button style="
                width: 100%;
                padding: 0.25rem;
                margin-bottom: 0.5rem;
                border-radius: 5px;
                border: 1px solid #b5c1cf;
                background-color: transparent;
                color: black;
                cursor: pointer;
                font-weight: 430;
            ">
                {label}
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )
