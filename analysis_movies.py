import pandas as pd
import re
import textwrap
from weasyprint import HTML

# 追加機能
# ・ジャンルを太字に
# ・評価の色付け
# ・俳優名カウント：カウントが同じ場合に人が交互になってしまう、ランキングなっている名前を太字に

#改行挿入関数
def wrap_text(text, width=16):
    if pd.isna(text):
        return ""
    return '\n'.join(textwrap.wrap(str(text), width))


class Analysis_Movie:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        # self.df["映画名"] = self.df["映画名"].apply(lambda x: wrap_text(x, width=16).replace('\n', '<br>'))
        # print(self.df)


    def sort(self, target_rows : list):
        if "映画名" in target_rows:
            self.df.sort_values(by="映画名", ascending=True, inplace=True)

        if "ジャンル" in target_rows:
            genre_order = [
                'アクション', 
                '西部劇', 
                'クライム', 
                'スリラー',
                'ミステリー', 
                'ミュージカル', 
                'ホラー', 
                '戦争', 
                '史実', 
                'ドラマ', 
                'ロマンス',
                'SF', 
                'ファンタジー',
                'コメディ', 
            ]
            self.df['ジャンル'] = pd.Categorical(self.df['ジャンル'], categories=genre_order, ordered=True)
            self.df.sort_values(by='ジャンル', ascending=True, inplace=True)

        if "評価" in target_rows:
            self.df.sort_values(by="評価", ascending=True, inplace=True)

        if "年代" in target_rows:
            self.df.sort_values(by="年代", ascending=True, inplace=True)

        if "監督名" in target_rows:
            actor_counts = self.df['監督名'].value_counts()
            self.df['tmp_cnt'] = self.df['監督名'].map(actor_counts)
            self.df.sort_values(by='tmp_cnt', ascending=False, inplace=True)
            self.df.drop(columns='tmp_cnt', inplace=True)

        if "俳優名" in target_rows:
            all_actors = self.df['俳優名'].dropna().str.split(',').explode().str.strip()
            actor_counts = all_actors.value_counts()

            # 各行に含まれる俳優の最大頻度を割り当て
            def get_max_count(actor_string):
                if pd.isna(actor_string):
                    return 0
                actor_list = re.split(r'[,]', actor_string)
                actor_list = [a.strip() for a in actor_list]
                return max(actor_counts.get(actor, 0) for actor in actor_list)

            self.df['tmp_cnt'] = self.df['俳優名'].apply(get_max_count)
            self.df.sort_values(by='tmp_cnt', ascending=False, inplace=True)
            self.df.drop(columns='tmp_cnt', inplace=True)


    def _highlight_genre(self, genre):
        color_map = {
            'アクション': '#FF6347',   # tomato
            '西部劇': '#FF8C00',       # darkorange
            'クライム': '#4169E1',   # royalblue
            'スリラー': '#228B22',   # forestgreen
            'ミステリー': '#DDA0DD',     # plum
            'ミュージカル': '#DDA0DD',     # plum
            'ホラー': '#808080',       # grey
            '戦争': '#D3D3D3',       # lightgrey
            '史実': '#D3D3D3',       # lightgrey
            'ドラマ': '#87CEFA',       # lightskyblue
            'ロマンス': '#FFB6C1',         # lightpink
            'SF' : '#90EE90',           # lightgreen
            'ファンタジー' : '#90EE90',           # lightgreen
            'コメディ': '#FFFF00',     # yellow
        }
        return f'background-color: {color_map.get(genre, "#FFFFFF")}'  # default = white

    def export_pdf_with_genre_colors(self, output_filename='Movies_table.pdf'):
        # DataFrame config
        styled = self.df.style \
            .format({"評価": "{:.1f}"}) \
            .applymap(self._highlight_genre, subset=['ジャンル']) \
            .set_table_styles([
                {'selector': 'th', 'props': [('font-size', '10pt'), 
                                             ('font-weight', 'bold'), 
                                             ("padding", "4px 8px")]},
                {'selector': 'td', 'props': [('font-size', '8pt')]},
                {"selector": ".row_heading", "props": [('font-size', '8pt'), 
                                                       ("font-weight", "normal")]},
            ]) \
            .set_properties(subset=['ジャンル', '評価', '年代'], **{'text-align': 'center'})
    
        # DataFrame to HTML
        html = styled.to_html()

        # CSS (HTMLの見た目を整える)
        pdf_css = """
        <style>
        @page {
            size: A4;
            margin: 0.5cm;
        }
        table {
            page-break-inside: auto;
            border-collapse: collapse;
        }
        
        thead {
            display: table-header-group;  /* ヘッダーを各ページの頭に表示 */
        }
        
        tbody {
            page-break-inside: avoid;  /* tbodyの途中でページ割らない */
        }
        
        tr {
            page-break-inside: avoid;
            page-break-after: auto;
        }
        </style>
        """

        # WeasyPrint HTML + CSS を読み込んでPDF化するツール
        full_html = pdf_css + html
        HTML(string=full_html).write_pdf(output_filename)
        print(f"✅ PDF出力完了: {output_filename}")


if __name__ == "__main__":
    am = Analysis_Movie("movies.csv")  # 映画データのCSVファイル名
    am.sort(['ジャンル', '年代'])
    am.export_pdf_with_genre_colors()

