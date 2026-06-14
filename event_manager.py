import numpy as np
import pandas as pd

TYPE_STYLE = {
    "Conference": ("#2563EB", "#DBEAFE", "#1E40AF"),
    "Workshop": ("#2563EB", "#DBEAFE", "#1E40AF"),
    "Seminar": ("#2563EB", "#DBEAFE", "#1E40AF"),
    "Competition": ("#EA580C", "#FFEDD5", "#9A3412"),
    "Hackathon": ("#EA580C", "#FFEDD5", "#9A3412"),
    "Festival": ("#EA580C", "#FFEDD5", "#9A3412"),
}


def _svg(inner):
    return (
        "<svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='#EA580C' "
        "stroke-width='2' stroke-linecap='round' stroke-linejoin='round' "
        "style='vertical-align:-2px;margin-right:7px'>" + inner + "</svg>"
    )


ICON_DATE = _svg("<rect x='3' y='4' width='18' height='18' rx='2'/><path d='M16 2v4M8 2v4M3 10h18'/>")
ICON_TIME = _svg("<circle cx='12' cy='12' r='10'/><path d='M12 6v6l4 2'/>")
ICON_LOC = _svg("<path d='M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z'/><circle cx='12' cy='10' r='3'/>")


class EventManager:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = self._load()

    def _load(self):
        df = pd.read_csv(self.csv_path)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"]).reset_index(drop=True)
        today = pd.Timestamp.now().normalize()
        df["days"] = (df["date"] - today).dt.days
        df["countdown"] = np.where(
            df["days"] == 0,
            "Today",
            np.where(df["days"] > 0, "in " + df["days"].astype(str) + " days", "Past"),
        )
        df["date_label"] = df["date"].dt.strftime("%a, %d %b %Y")
        return df.sort_values("date").reset_index(drop=True)

    def universities(self):
        return ["All"] + np.sort(self.df["university"].unique()).tolist()

    def event_types(self):
        return ["All"] + np.sort(self.df["event_type"].unique()).tolist()

    def filter_events(self, university, event_type, query):
        df = self.df
        u_mask = pd.Series(True, index=df.index) if university == "All" else df["university"].eq(university)
        t_mask = pd.Series(True, index=df.index) if event_type == "All" else df["event_type"].eq(event_type)
        text = str(query).strip().lower()
        q_mask = pd.Series(True, index=df.index) if text == "" else df["event_name"].str.lower().str.contains(text, regex=False, na=False)
        return df[u_mask & t_mask & q_mask].reset_index(drop=True)

    def summary(self, df):
        return {
            "events": int(df.shape[0]),
            "universities": int(df["university"].nunique()),
            "types": int(df["event_type"].nunique()),
        }

    def _card(self, row):
        strip, bg, fg = TYPE_STYLE.get(row["event_type"], ("#EA580C", "#FFEDD5", "#9A3412"))
        return (
            "<div class='card'>"
            f"<div class='strip' style='background:{strip}'></div>"
            "<div class='card-body'>"
            "<div class='row'>"
            f"<span class='badge' style='background:{bg};color:{fg}'>{row['event_type']}</span>"
            f"<span class='count'>{row['countdown']}</span>"
            "</div>"
            f"<div class='uni'>{row['university']}</div>"
            f"<h3>{row['event_name']}</h3>"
            f"<div class='meta'>{ICON_DATE}{row['date_label']} &nbsp;&middot;&nbsp; {ICON_TIME}{row['time']}</div>"
            f"<div class='meta'>{ICON_LOC}{row['location']}</div>"
            f"<p class='desc'>{row['description']}</p>"
            "</div></div>"
        )

    def cards_html(self, df):
        if df.shape[0] == 0:
            return "<div class='empty'>No events match your filters. Try clearing the search box.</div>"
        return "".join(df.apply(self._card, axis=1).tolist())
