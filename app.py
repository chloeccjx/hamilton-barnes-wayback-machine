import base64
import json
import re
import unicodedata
from pathlib import Path
import streamlit as st

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(page_title="Specialism Wayback Machine", layout="centered")

# -------------------------------
# Styling
# -------------------------------
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

# ------------------------------------------------
# GLOBAL SOURCES (renders once at bottom)
# Alphabetised by title
# ------------------------------------------------

GLOBAL_SOURCES = [
    ("Amazon - Project Kuiper FCC approval; commit to invest >$10B", "https://www.aboutamazon.com/news/company-news/amazon-receives-fcc-approval-for-project-kuiper-satellite-constellation"),
    ("Brookings (27 Sep 2019) - NotPetya caused an estimated $10B of damage worldwide", "https://www.brookings.edu/articles/a-federal-backstop-for-insuring-against-cyberattacks/"),
    ("Brookings - NotPetya did ~$10B of damage globally (Dec 2021)", "https://www.brookings.edu/articles/how-the-notpetya-attack-is-reshaping-cyber-insurance/"),
    ("Business Wire (19 Oct 2022) - Gartner forecasts worldwide IT spending to grow 5.1% in 2023", "https://www.businesswire.com/news/home/20221019005682/en/Gartner-Forecasts-Worldwide-IT-Spending-to-Grow-5.1-in-2023"),
    ("Business Wire (7 Apr 2021) - Gartner forecasts worldwide IT spending to reach $4.1T in 2021", "https://www.businesswire.com/news/home/20210407005595/en/Gartner-Forecasts-Worldwide-IT-Spending-to-Reach-%244-Trillion-in-2021"),
    ("Canalys (8 Feb 2023) - Cloud infrastructure services spend growth (PDF)", "https://canalys-prod-public.s3.eu-west-1.amazonaws.com/static/press_release/2023/1725098181Worldwide-Cloud-Market-Q4-2022.pdf"),
    ("CBRE (24 Jun 2024) - Global Data Center Trends 2024", "https://www.cbre.com/insights/reports/global-data-center-trends-2024"),
    ("CISA - Colonial Pipeline attack summary (May 2021)", "https://www.cisa.gov/news-events/news/attack-colonial-pipeline-what-weve-learned-what-weve-done-over-past-two-years"),
    ("CISA - Meltdown and Spectre guidance (Jan 2018)", "https://www.cisa.gov/news-events/alerts/2018/01/04/meltdown-and-spectre-side-channel-vulnerability-guidance"),
    ("CISA alert (14 Dec 2020) - Active exploitation of SolarWinds Orion software", "https://www.cisa.gov/news-events/alerts/2020/12/13/active-exploitation-solarwinds-software"),
    ("Cloudflare - Mirai botnet retrospective (Dec 2017)", "https://blog.cloudflare.com/inside-mirai-the-infamous-iot-botnet-a-retrospective-analysis/"),
    ("Cloudflare Learning Center - Mirai botnet background", "https://www.cloudflare.com/learning/ddos/glossary/mirai-botnet/"),
    ("Data Center Dynamics (20 Nov 2025) - Hyperscale capex and capacity hits peak in Q3 2025", "https://www.datacenterdynamics.com/en/news/hyperscale-capex-and-capacity-hits-peak-in-q3-2025-synergy/"),
    ("EU NIS2 Directive (EU) 2022/2555 - EUR-Lex", "https://eur-lex.europa.eu/eli/dir/2022/2555/oj/eng"),
    ("European Commission - AI Act enters into force (Aug 1, 2024)", "https://commission.europa.eu/news-and-media/news/ai-act-enters-force-2024-08-01_en"),
    ("European Commission Digital Strategy - AI Act timeline and applicability", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai"),
    ("FCC - 600 MHz incentive auction yielded $19.8B", "https://www.fcc.gov/600-mhz-band"),
    ("FCC - C-band Auction 107 results (gross bids >$81B)", "https://www.fcc.gov/document/fcc-announces-winning-bidders-c-band-auction"),
    ("FTTH Council Europe (24 May 2022) - European FTTH/B Market Panorama 2022", "https://www.ftthcouncil.eu/committees/market-intelligence/1436/european-ftth-b-market-panorama-2022"),
    ("Gartner (15 Jan 2020) - Worldwide IT spending projected at $3.9T in 2020", "https://www.gartner.com/en/newsroom/press-releases/2020-01-15-gartner-says-global-it-spending-to-reach-3point9-trillion-in-2020"),
    ("Gartner (15 Jan 2026) - Worldwide AI spending forecast $2.52T in 2026", "https://www.gartner.com/en/newsroom/press-releases/2026-1-15-gartner-says-worldwide-ai-spending-will-total-2-point-5-trillion-dollars-in-2026"),
    ("Gartner (16 Jul 2024) - Worldwide IT spending expected at $5.26T in 2024", "https://www.gartner.com/en/newsroom/press-releases/2024-07-16-gartner-forecasts-worldwide-it-spending-to-grow-7-point-5-percent-in-2024"),
    ("Gartner (17 Apr 2019) - Worldwide IT spending projected at $3.79T in 2019", "https://www.gartner.com/en/newsroom/press-releases/2019-04-17-gartner-says-global-it-spending-to-grow-1-1-percent-i"),
    ("Gartner (20 Oct 2021) - Worldwide IT spending projected at $4.5T in 2022", "https://www.gartner.com/en/newsroom/press-releases/2021-10-20-gartner-forecasts-worldwide-it-spending-to-exceed-4-trillion-in-2022"),
    ("Gartner (21 Jan 2025) - Worldwide IT spending expected at $5.61T in 2025", "https://www.gartner.com/en/newsroom/press-releases/2025-01-21-gartner-forecasts-worldwide-it-spending-to-grow-9-point-8-percent-in-2025"),
    ("Gartner (25 Oct 2016) - IT spending forecast to reach $3.5T in 2017", "https://www.gartner.com/en/newsroom/press-releases/2016-10-25-gartner-says-it-spending-in-australia-to-reach-almost-85-billion-in-2017-as-the-battle-for-the-digital-platform-begins"),
    ("Gartner (28 Aug 2024) - Global information security spending estimated $183.9B in 2024; projected ~$212B in 2025", "https://www.gartner.com/en/newsroom/press-releases/2024-08-28-gartner-forecasts-global-information-security-spending-to-grow-15-percent-in-2025"),
    ("Gartner (29 Jul 2025) - Information security spend projected $213B in 2025 and $240B in 2026", "https://www.gartner.com/en/newsroom/press-releases/2025-07-29-gartner-forecasts-worldwide-end-user-spending-on-information-security-to-total-213-billion-us-dollars-in-2025"),
    ("Gartner (3 Feb 2026) - Worldwide IT spending forecast $6.15T in 2026; data center systems spend $496.2B (2025) and $653.4B (2026)", "https://www.gartner.com/en/newsroom/press-releases/2026-02-03-gartner-forecasts-worldwide-it-spending-to-grow-10-point-8-percent-in-2026-totaling-6-point-15-trillion-dollars"),
    ("Gartner (7 Jul 2016) - Worldwide IT spending forecast flat at $3.41T in 2016", "https://www.gartner.com/en/newsroom/press-releases/2016-07-07-gartner-says-worldwide-it-spending-is-forecast-to-be-flat-in-2016"),
    ("Gartner press release (15 Jul 2025) - Worldwide IT spending expected to total $5.43T in 2025 (+7.9%)", "https://www.gartner.com/en/newsroom/press-releases/2025-07-15-gartner-forecasts-worldwide-it-spending-to-grow-7-point-9-percent-in-2025"),
    ("GDPR legal text (Regulation (EU) 2016/679) - EUR-Lex", "https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng"),
    ("Google Cloud Threat Intelligence - SolarWinds SUNBURST (Dec 2020)", "https://cloud.google.com/blog/topics/threat-intelligence/evasive-attacker-leverages-solarwinds-supply-chain-compromises-with-sunburst-backdoor"),
    ("Microsoft - Destructive malware targeting Ukrainian organisations (Jan 2022)", "https://www.microsoft.com/en-us/security/blog/2022/01/15/destructive-malware-targeting-ukrainian-organizations/"),
    ("Microsoft MSRC - Cyber threat activity in Ukraine (Feb 2022)", "https://www.microsoft.com/en-us/msrc/blog/2022/02/analysis-resources-cyber-threat-activity-ukraine/"),
    ("National Audit Office (UK) - Investigation: WannaCry cyber attack and the NHS (Oct 2017)", "https://www.nao.org.uk/reports/investigation-wannacry-cyber-attack-and-the-nhs/"),
    ("NIST NVD - CVE-2021-44228 (Log4Shell)", "https://nvd.nist.gov/vuln/detail/CVE-2021-44228"),
    ("NVIDIA Investor Relations (21 Feb 2024) - Fiscal 2024 results", "https://investor.nvidia.com/news/press-release-details/2024/NVIDIA-Announces-Financial-Results-for-Fourth-Quarter-and-Fiscal-2024/"),
    ("NVIDIA Newsroom (26 Feb 2025) - Q4 and Fiscal 2025 results", "https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2025"),
    ("Ofcom - Media Nations 2021 (published 5 Aug 2021)", "https://www.ofcom.org.uk/media-use-and-attitudes/media-habits-adults/media-nations-2021"),
    ("OneWeb Chapter 11 filing (Mar 2020)", "https://www.space.com/oneweb-satellite-internet-startup-files-for-bankruptcy.html"),
    ("PwC - Global Entertainment & Media Outlook 2025-2029 insights", "https://www.pwc.com/gx/en/issues/business-model-reinvention/outlook/insights-and-perspectives.html"),
    ("Reuters (21 Feb 2024) - NVIDIA data center revenue growth and AI demand context", "https://www.reuters.com/technology/nvidia-forecasts-first-quarter-revenue-above-estimates-2024-02-21/"),
    ("Reuters (28 Mar 2020) - OneWeb files for Chapter 11 bankruptcy", "https://www.reuters.com/article/business/softbank-backed-oneweb-files-for-chapter-11-bankruptcy-plan-cuts-jobs-idUSKBN21F05P/"),
    ("Reuters (5 Apr 2019) - South Korean and US telcos roll out 5G services", "https://www.reuters.com/article/technology/south-korean-us-telcos-roll-out-5g-services-early-as-race-heats-up-idUSKCN1RF0KH/"),
    ("Reuters - EU says no pause on AI Act timeline (Jul 4, 2025)", "https://www.reuters.com/world/europe/artificial-intelligence-rules-go-ahead-no-pause-eu-commission-says-2025-07-04/"),
    ("Reuters - OneWeb emerges from bankruptcy with $1B equity investment (Nov 2020)", "https://www.reuters.com/business/aerospace-defense/british-satellite-firm-oneweb-emerges-bankruptcy-2020-11-20/"),
    ("Reuters - UK fibre deal references ~£3.5B investment narrative (Feb 2026)", "https://www.reuters.com/legal/transactional/virgin-media-o2-owners-buy-uk-fibre-firm-substantial-272-billion-2026-02-18/"),
    ("SK Telecom - 5G service launched April 3, 2019 (milestones press release)", "https://www.sktelecom.com/en/press/press_detail.do?idx=1451"),
    ("Synergy Research Group (18 Sept 2025) - Hyperscale capex $127B in Q2 2025; up 72% YoY", "https://www.srgresearch.com/articles/justifying-the-explosive-growth-in-hyperscale-capex"),
    ("Synergy Research Group (19 Nov 2025) - Q3 2025 cloud infrastructure services revenue $106.9B; trailing 12-month $390B", "https://www.srgresearch.com/articles/cloud-market-share-trends-big-three-together-hold-63-while-oracle-and-the-neoclouds-inch-higher"),
    ("US Department of Energy - Colonial Pipeline cyber incident (May 2021)", "https://www.energy.gov/ceser/colonial-pipeline-cyber-incident"),
    ("WIRED (Oct 2016) - Dyn DNS attack and Mirai botnet impact", "https://www.wired.com/story/internet-down-dyn-october-2016/"),
]

st.divider()
with st.expander("Sources"):
    for title, url in GLOBAL_SOURCES:
        st.markdown(f"- [{title}]({url})")

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
