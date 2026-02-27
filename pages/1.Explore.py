import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="The Tech Wayback Machine", layout="wide")
st.title("Tech Wayback Machine")

DATA_PATH = Path("data/content.json")

if not DATA_PATH.exists():
    st.error("Missing data/content.json")
    st.stop()

try:
    content = json.loads(DATA_PATH.read_text(encoding="utf-8"))
except Exception as e:
    st.error("content.json is not valid JSON")
    st.code(str(e))
    st.stop()

niches = sorted(content.keys())
if not niches:
    st.warning("No niches found in content.json")
    st.stop()

with st.sidebar:
    st.header("Choose your path")
    niche = st.selectbox("Tech niche", niches)

    is_2026 = st.toggle("Year: 2016 ↔ 2026", value=True)
    year = "2026" if is_2026 else "2016"

st.subheader(f"{niche} — {year}")

paragraphs = content.get(niche, {}).get(year, [])
if not paragraphs:
    st.info("No content for this selection yet.")
else:
    for p in paragraphs:
        st.write(p)

conclusion = content.get(niche, {}).get("conclusion", [])
if conclusion:
    st.divider()
    st.markdown("### What this means 🧠")
    for p in conclusion:
        st.write(p)
