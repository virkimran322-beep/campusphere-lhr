# CAMPUSPHERE — Project Context (read first)

CAMPUSPHERE is a **university event calendar website for Lahore**. It shows events from multiple
universities (LUMS, UET, FAST, PU, UMT, COMSATS, GCU) in one place so students can find seminars,
workshops, competitions and festivals without checking each university separately.

**This project is completely separate from FairGo.** It has its own folder, its own git repo, and its
own GitHub repo. Never mix it with FairGo or commit its files into the FairGo repository.

## What it does
- University-wise event listing with date, time, location and a short description.
- Filter by university, filter by event type, and a search box for event names.
- Dashboard-style summary metrics: total events, number of universities, number of event types.
- Reads all events from a CSV file, so updating events needs no code change.

## Tech stack
- **Python + Streamlit** for the web interface.
- **numpy / pandas** for all data handling.
- **CSV** file as the data store (`data/events.csv`).

## HARD coding rules (must always follow in this project)
- Use ONLY these constructs: classes, functions, numpy, pandas, lists, dictionaries, strings,
  conditional statements, variables, datatypes.
- **No raw `for` / `while` loops.** Render repeated content with `df.apply(...)` + `"".join(...)`,
  and build lists/derived columns with `np.where`, `np.sort`, vectorised pandas operations.
- **No comments anywhere, and no English subtitles/annotations written alongside the code.**
  Deliver the code itself — nothing written over or around it explaining it. (Owner instruction.)
- Keep the code clean and consistent with the existing style.

## Project structure
```
CAMPUSPHERE/
├─ app.py                 Streamlit UI: title, summary metrics, filters, event grid, CSV download
├─ event_manager.py       EventManager class — load, filter, summarise, render
├─ data/
│  └─ events.csv          event records (university, event_name, event_type, date, time, location, description)
├─ .streamlit/config.toml theme
├─ requirements.txt
├─ README.md
└─ CLAUDE.md              this file
```

## Run it
```bash
pip install -r requirements.txt
streamlit run app.py
```
Opens at http://localhost:8501. Add or edit events by editing `data/events.csv` only.

## GitHub & deployment
- GitHub repo: `virkimran322-beep/campusphere-lhr` (account `virkimran322-beep`).
- Deploy on **Streamlit Community Cloud** (free permanent `*.streamlit.app` URL): connect the repo,
  branch `main`, main file `app.py`. The deploy step needs the owner's own browser login.
- On-screen app name = **CAMPUSPHERE**; `campusphere-lhr` is only the repo/URL identifier.

## Future improvements (leave room, don't build unless simple)
Online event registration, email notifications for new events, a student login system, and
event booking / payment integration. All data flows through `EventManager`, so these can be added
as new methods + widgets without changing the render path.
