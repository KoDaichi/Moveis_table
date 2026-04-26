# 追加機能
# ・ジャンルを太字に
# ・評価の色付け
# ・俳優名カウント：カウントが同じ場合に人が交互になってしまう、ランキングなっている名前を太字に

import pandas as pd

from exporter import MovieExporter
from sorter import MovieSorter


class Analysis_Movie:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self._sorter = MovieSorter(self.df)
        self._exporter = MovieExporter(self.df)

    def sort(self, keys: list):
        self._sorter.sort(keys)

    def export_pdf_with_genre_colors(self, output_filename="Movies_table.pdf"):
        self._exporter.export_pdf(output_filename)


if __name__ == "__main__":
    am = Analysis_Movie("data/movies.csv")  # 映画データのCSVファイル名
    am.sort(["評価"])
    # am.sort(["ジャンル"])
    am.export_pdf_with_genre_colors()
