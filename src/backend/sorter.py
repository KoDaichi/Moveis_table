import re

import pandas as pd

from constants import GENRE_ORDER


class MovieSorter:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def by_title(self):
        self.df.sort_values(by="映画名", ascending=True, inplace=True)

    def by_genre(self):
        self.df["ジャンル"] = pd.Categorical(
            self.df["ジャンル"], categories=GENRE_ORDER, ordered=True
        )
        self.df.sort_values(by="ジャンル", ascending=True, inplace=True)

    def by_rating(self):
        self.df.sort_values(by="評価", ascending=False, inplace=True)

    def by_year(self):
        self.df.sort_values(by="年代", ascending=True, inplace=True)

    def by_director(self):
        director_counts = self.df["監督名"].value_counts()
        self.df["tmp_cnt"] = self.df["監督名"].map(director_counts)
        self.df.sort_values(
            by=["tmp_cnt", "監督名"], ascending=[False, True], inplace=True
        )
        self.df.drop(columns="tmp_cnt", inplace=True)

    def by_actor(self):
        all_actors = self.df["俳優名"].dropna().str.split(",").explode().str.strip()
        actor_counts = all_actors.value_counts()

        # 各行に含まれる俳優の最大頻度を割り当て
        def get_max_count(actor_string):
            if pd.isna(actor_string):
                return 0
            actors = [a.strip() for a in re.split(r",", actor_string)]
            return max(actor_counts.get(actor, 0) for actor in actors)

        self.df["tmp_cnt"] = self.df["俳優名"].apply(get_max_count)
        self.df.sort_values(
            by=["tmp_cnt", "俳優名"], ascending=[False, True], inplace=True
        )
        self.df.drop(columns="tmp_cnt", inplace=True)

    def sort(self, keys: list):
        dispatch = {
            "映画名":   self.by_title,
            "ジャンル": self.by_genre,
            "評価":     self.by_rating,
            "年代":     self.by_year,
            "監督名":   self.by_director,
            "俳優名":   self.by_actor,
        }
        for key in keys:
            if key in dispatch:
                dispatch[key]()
