# Concept

## Overview

This repository generates styled, printable PDF tables of personal movie records.  
Movie data is stored in a CSV file and exported as A4 PDFs with color-coded genres and flexible sort orders.

## Core Idea

- Maintain a personal movie list (title, genre, rating, year, director, actors) as a CSV.
- Apply sorting and visual styling via Python, then render to PDF using WeasyPrint.
- Produce multiple PDFs sorted differently (by score, genre, year, etc.) for easy reference.

## Data

| Column | Content |
|--------|---------|
| 映画名 | Movie title |
| ジャンル | Genre |
| 評価 | Personal score (float) |
| 年代 | Release year |
| 監督名 | Director |
| 俳優名 | Cast (comma-separated) |

Source file: `data/movies.csv`

## Sort Modes (`Analysis_Movie.sort`)

Sorting is driven by a prioritized list of column keys:

| Key | Behavior |
|-----|----------|
| `評価` | Descending score |
| `ジャンル` | Custom genre order (Action → Comedy) |
| `年代` | Ascending year |
| `映画名` | Alphabetical |
| `監督名` | By director appearance count (descending), then name |
| `俳優名` | By actor appearance count across all rows (descending) |

## Output

PDFs are written to `output/`:

- `Table_sorted_by_score.pdf`
- `Table_sorted_by_genre.pdf`
- `Table_sorted_by_year.pdf`

Each PDF is A4, with table headers repeated on every page.

## Genre Color Coding

Each genre cell is background-colored for quick visual scanning:

| Genre | Color |
|-------|-------|
| アクション | Tomato |
| 西部劇 | Dark orange |
| クライム | Royal blue |
| スリラー | Forest green |
| ミステリー / ミュージカル | Plum |
| ホラー | Grey |
| 戦争 / 史実 | Light grey |
| ドラマ | Light sky blue |
| ロマンス | Light pink |
| SF / ファンタジー | Light green |
| コメディ | Yellow |

## Stack

- **pandas** — data loading, sorting, styling
- **WeasyPrint** — HTML-to-PDF rendering
- **Python 3.12+**
