import numpy as np
import pandas as pd


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
        return (
            "<div class='card'>"
            "<div class='card-top'>"
            f"<span class='badge'>{row['event_type']}</span>"
            f"<span class='count'>{row['countdown']}</span>"
            "</div>"
            f"<div class='uni'>{row['university']}</div>"
            f"<h3>{row['event_name']}</h3>"
            f"<div class='meta'>&#128197; {row['date_label']} &nbsp;&middot;&nbsp; &#128340; {row['time']}</div>"
            f"<div class='meta'>&#128205; {row['location']}</div>"
            f"<p class='desc'>{row['description']}</p>"
            "</div>"
        )

    def cards_html(self, df):
        if df.shape[0] == 0:
            return "<div class='empty'>No events match your filters. Try clearing the search box.</div>"
        return "".join(df.apply(self._card, axis=1).tolist())
