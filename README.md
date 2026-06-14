# CAMPUSPHERE — Lahore University Events

A single platform that shows university events across Lahore (LUMS, UET, FAST, PU, UMT, COMSATS, GCU).
Students can filter by university and event type, and search by event name — built with Python, Streamlit, pandas, and numpy.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501

## Add or edit events

Open `data/events.csv` and add a row. Columns:

`university, event_name, event_type, date (YYYY-MM-DD), time, location, description`

No code changes are needed — the dashboard reads the CSV on every load.

## Project structure

```
UniEventCalendar/
  app.py              Streamlit UI (filters, metrics, event grid)
  event_manager.py    EventManager class: load, filter, summarise, render
  data/events.csv     Event records (the data source)
  .streamlit/config.toml  Theme
  requirements.txt
  README.md
```

## Possible future improvements

Online event registration, email notifications for new events, a student login system,
and event booking/payment integration.
```
