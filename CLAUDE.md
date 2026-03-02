# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

「To Corona Ex」漫画配信サービスの無料エピソードをAtom形式のRSSフィードとして生成・公開するツール。GitHub Actionsで12時間ごとに自動実行し、GitHub Pagesで配信する。

## コマンド

```bash
# 依存関係のインストール
uv sync --all-extras

# メインスクリプト実行（フィード生成）
uv run main.py
```

パッケージマネージャーは `uv`、Python バージョンは 3.13。

## アーキテクチャ

**処理フロー**:
1. `feed.csv` から漫画IDを読み込む
2. To Corona Ex API (`api.to-corona-ex.com`) へHTTPリクエストを送信
   - コミック情報: `/comics/{comic_id}`
   - 無料エピソード一覧: `/episodes?comic_id=...&episode_status=free_viewing&limit=5&order=desc`
3. `feedgenerator` ライブラリでAtomフィードを生成 → `feeds/{id}.xml`
4. Jinja2で `templates/index.html` からWebインターフェース生成 → `feeds/index.html`
5. GitHub Actionsが `feeds/` ディレクトリをGitHub Pagesへデプロイ

**主要ファイル**:
- `main.py` — 全ロジックが集約された単一スクリプト
- `feed.csv` — 対象漫画IDの一覧（行ごとに1つのID）
- `templates/index.html` — Jinja2テンプレート（Bootstrap 5.3使用）
- `.github/workflows/gh-pages.yaml` — 自動実行・デプロイワークフロー

**依存ライブラリ**: `requests`（HTTP通信）、`feedgenerator`（Atom生成）、`jinja2`（テンプレート）

## 新しい漫画の追加

`feed.csv` に漫画IDを1行追加するだけでフィードが自動生成される。
