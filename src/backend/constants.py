GENRE_ORDER = [
    "アクション",
    "西部劇",
    "クライム",
    "スリラー",
    "ミステリー",
    "ミュージカル",
    "ホラー",
    "戦争",
    "史実",
    "ドラマ",
    "ロマンス",
    "SF",
    "ファンタジー",
    "コメディ",
]

GENRE_COLORS = {
    "アクション":   "#FF6347",  # tomato
    "西部劇":       "#FF8C00",  # darkorange
    "クライム":     "#4169E1",  # royalblue
    "スリラー":     "#228B22",  # forestgreen
    "ミステリー":   "#DDA0DD",  # plum
    "ミュージカル": "#DDA0DD",  # plum
    "ホラー":       "#808080",  # grey
    "戦争":         "#D3D3D3",  # lightgrey
    "史実":         "#D3D3D3",  # lightgrey
    "ドラマ":       "#87CEFA",  # lightskyblue
    "ロマンス":     "#FFB6C1",  # lightpink
    "SF":           "#90EE90",  # lightgreen
    "ファンタジー": "#90EE90",  # lightgreen
    "コメディ":     "#FFFF00",  # yellow
}

PDF_CSS = """
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
