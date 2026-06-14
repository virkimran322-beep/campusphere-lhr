import streamlit as st
from event_manager import EventManager

st.set_page_config(page_title="EVENT HUB", page_icon="🎓", layout="wide")

STYLE = """
<style>
.block-container { padding-top: 2rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(330px, 1fr)); gap: 16px; margin-top: 8px; }
.card { background: #ffffff; border: 1px solid #e6e8eb; border-radius: 14px; padding: 16px 18px; box-shadow: 0 1px 3px rgba(16,24,40,.06); }
.card-top { display: flex; justify-content: space-between; align-items: center; }
.badge { background: #e7f0ff; color: #1d4ed8; font-size: 12px; font-weight: 600; padding: 3px 10px; border-radius: 999px; }
.count { color: #16a34a; font-size: 12px; font-weight: 600; }
.uni { color: #64748b; font-size: 13px; font-weight: 600; margin-top: 8px; }
.card h3 { margin: 4px 0 10px; font-size: 18px; color: #0f172a; }
.meta { color: #475569; font-size: 14px; margin: 2px 0; }
.desc { color: #334155; font-size: 14px; margin-top: 10px; line-height: 1.5; }
.empty { grid-column: 1 / -1; color: #64748b; padding: 48px; text-align: center; border: 1px dashed #cbd5e1; border-radius: 14px; }
</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)

manager = EventManager("data/events.csv")

st.title("🎓 EVENT HUB")
st.caption("University events across Lahore — seminars, workshops, competitions and festivals, all in one place.")

with st.sidebar:
    st.header("Filters")
    university = st.selectbox("University", manager.universities())
    event_type = st.selectbox("Event type", manager.event_types())
    query = st.text_input("Search event name", "")
    st.markdown("Update events by editing **data/events.csv**.")

events = manager.filter_events(university, event_type, query)
stats = manager.summary(events)

export_df = events[["university", "event_name", "event_type", "date", "time", "location", "description"]].copy()
export_df["date"] = export_df["date"].dt.strftime("%Y-%m-%d")
st.sidebar.download_button("Download filtered list (CSV)", export_df.to_csv(index=False).encode("utf-8"), "events_filtered.csv", "text/csv")

m1, m2, m3 = st.columns(3)
m1.metric("Total events", stats["events"])
m2.metric("Universities", stats["universities"])
m3.metric("Event types", stats["types"])

st.markdown("### Upcoming events")
st.markdown(f"<div class='grid'>{manager.cards_html(events)}</div>", unsafe_allow_html=True)
