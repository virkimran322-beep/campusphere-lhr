import streamlit as st
from event_manager import EventManager

st.set_page_config(page_title="CAMPUSPHERE", page_icon="🎓", layout="wide")

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@500;600&family=Fira+Sans:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Fira Sans', sans-serif; }
.stApp { background: #FFF7ED; }
.block-container { padding-top: 2.2rem; max-width: 1200px; }
.hero-title { font-size: 46px; font-weight: 700; letter-spacing: -1.5px; color: #0F172A; margin: 0 0 2px; }
.hero-title .dot { color: #EA580C; }
[data-testid="stMetric"] { background: #fff; border: 1px solid #FCEAE1; border-radius: 16px; padding: 16px 20px; }
[data-testid="stMetricValue"] { color: #EA580C; font-weight: 700; }
[data-testid="stMetricLabel"] { color: #9A3412; }
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div { border-radius: 10px; }
.section { font-size: 22px; font-weight: 700; color: #0F172A; margin: 22px 0 6px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 18px; margin-top: 8px; }
.card { background: #fff; border: 1px solid #FCEAE1; border-radius: 16px; overflow: hidden; padding-bottom: 16px;
        transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease; }
.card:hover { transform: translateY(-4px); box-shadow: 0 14px 30px rgba(234,88,12,.16); border-color: #EA580C; }
.strip { height: 6px; }
.card-body { padding: 14px 18px 0; }
.row { display: flex; justify-content: space-between; align-items: center; }
.badge { font-family: 'Fira Code', monospace; font-size: 11px; font-weight: 600; letter-spacing: .4px;
         text-transform: uppercase; padding: 4px 10px; border-radius: 8px; }
.count { font-family: 'Fira Code', monospace; font-size: 12px; font-weight: 600; color: #2563EB; }
.uni { color: #9A3412; font-weight: 600; font-size: 13px; margin-top: 12px; }
.card h3 { margin: 4px 0 12px; font-size: 19px; font-weight: 700; color: #0F172A; line-height: 1.25; }
.meta { color: #475569; font-size: 14px; margin: 3px 0; }
.desc { color: #334155; font-size: 14px; margin-top: 10px; line-height: 1.5; }
.empty { grid-column: 1 / -1; text-align: center; padding: 56px; color: #9A3412;
         border: 2px dashed #FCEAE1; border-radius: 16px; background: #fff; }
@media (prefers-reduced-motion: reduce) { .card { transition: none; } .card:hover { transform: none; } }
</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)

manager = EventManager("data/events.csv")

st.markdown("<h1 class='hero-title'>CAMPUSPHERE<span class='dot'>.</span></h1>", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
with f1:
    university = st.selectbox("University", manager.universities())
with f2:
    event_type = st.selectbox("Event type", manager.event_types())
with f3:
    query = st.text_input("Search event name", "")

events = manager.filter_events(university, event_type, query)
stats = manager.summary(events)

m1, m2, m3 = st.columns(3)
m1.metric("Total events", stats["events"])
m2.metric("Universities", stats["universities"])
m3.metric("Event types", stats["types"])

export_df = events[["university", "event_name", "event_type", "date", "time", "location", "description"]].copy()
export_df["date"] = export_df["date"].dt.strftime("%Y-%m-%d")
st.download_button("Download filtered list (CSV)", export_df.to_csv(index=False).encode("utf-8"), "events_filtered.csv", "text/csv")

st.markdown("<div class='section'>Upcoming events</div>", unsafe_allow_html=True)
st.markdown(f"<div class='grid'>{manager.cards_html(events)}</div>", unsafe_allow_html=True)
