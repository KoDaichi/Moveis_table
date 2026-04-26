import pandas as pd
from weasyprint import HTML

from constants import GENRE_COLORS, PDF_CSS


class MovieExporter:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def _highlight_genre(self, genre):
        color = GENRE_COLORS.get(genre, "#FFFFFF")
        return f"background-color: {color}"

    def _build_styled_table(self):
        return (
            self.df.style.format({"評価": "{:.1f}"})
            .map(self._highlight_genre, subset=["ジャンル"])
            .set_table_styles(
                [
                    {
                        "selector": "th",
                        "props": [
                            ("font-size", "10pt"),
                            ("font-weight", "bold"),
                            ("padding", "4px 8px"),
                        ],
                    },
                    {"selector": "td", "props": [("font-size", "8pt")]},
                    {
                        "selector": ".row_heading",
                        "props": [("font-size", "8pt"), ("font-weight", "normal")],
                    },
                ]
            )
            .set_properties(
                subset=["ジャンル", "評価", "年代"], **{"text-align": "center"}
            )
        )

    def export_pdf(self, output_filename="Movies_table.pdf"):
        html = self._build_styled_table().to_html()
        HTML(string=PDF_CSS + html).write_pdf(output_filename)
        print(f"✅ PDF出力完了: {output_filename}")
