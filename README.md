# hazieta-site

2017年に `hazieta.com` で書いていたブログ「ハジエッセイ – 要は日記」（モンハンエクスプロア・シノアリス）を、
Wayback Machine に残っていた記録から復元した静的サイト。Astro で作り、GitHub Pages に出す。

- 公開先: https://at-addition.github.io/hazieta-site/
- 記事の URL は元のサイトと同じ道のり（`/mhxr/events/carnival-flag-collect/` など）

## 中身

| 場所 | 中身 |
| :--- | :--- |
| `src/content/posts/` | 記事 87 本の Markdown。`scripts/import.py` が書き出すので手で直さない |
| `src/content/wp-content/` | 記事に載っている画像 245 枚。Astro が縮小・変換して出す |
| `src/pages/` | 一覧（`index.astro`）・記事（`[...slug].astro`）・404 |
| `src/components/PostCard.astro` | 一覧のカード（画像・ゲームのバッジ・日付・タイトル・抜き出し） |
| `src/lib/games.ts` | パスの先頭（`mhxr` / `sinoalice` / `other`）からゲームを決める表と色。カードの抜き出しもここ |
| `src/assets/hazieta-title.svg` | ヘッダーのロゴ。当時のタイトル画像（ハジエッセイ｜要は日記・www.hazieta.com とうさぎ）をなぞった SVG |
| `src/assets/hazieta-logo.svg` | トップの黒い帯の当時のロゴ（hazieta.com とうさぎ）。なぞった SVG で、色は文字色に合わせる |
| `src/assets/rabbit.svg` | 顔だけのうさぎの SVG（今は `public/favicon.svg` の元） |
| `public/favicon.svg` | ブラウザのタブのアイコン。顔だけのうさぎ（明るい画面と暗い画面で色が変わる） |
| `public/favicon.ico` / `apple-touch-icon.png` / `icon-192.png` / `icon-512.png` / `site.webmanifest` | スマホのホーム画面・ブックマークのアイコン。当時のサイトアイコン（体付きのうさぎ `M2`、白地の正方形）をなぞって作り直したもの |
| `design/original/` | 当時の画像。ヘッダー 1080×360・アイコン 400×400（本人から）、サイトアイコン `M2` 300×300・タイトル画像 798×250（Wayback から）。`scripts/trace-logo.py` でなぞった |
| `design/rabbit-body-square_1791.png` | `M2` をなぞった正方形アイコンの元（上のアイコンはここから縮めた） |
| `src/layouts/Base.astro` | 全ページ共通の枠と色（明るい画面・暗い画面）、フォント（Google Fonts の Dela Gothic One と Zen Kaku Gothic New） |
| `scripts/import.py` | 取り出した記事と画像を、このサイトの形に書き直して取り込む |
| `.github/workflows/deploy.yml` | `main` に入ったらビルドして Pages へ出す |

## 記事を取り込み直す

記事の元は、Wayback Machine から取り出して手元に置いたもの（このリポジトリの外）。

```powershell
python -I scripts/import.py
npm run build
```

`import.py` がやること:

- 固定ページ（目次・プライバシーポリシー・お問い合わせ）は取り込まない。プライバシーポリシーには当時の連絡先が書いてある
- 画像とサイト内リンクは**記事のページから見た相対パス**にする。GitHub Pages の `/hazieta-site/` でも独自ドメインの `/` でも同じ記事で動く
- 縮小版の画像（`-300x200.jpg`）を指していても、元の大きさの画像が残っていればそちらを使う
- Wayback に残っていなかった画像（119 枚）は落とす
- 本文の最初の画像を `cover` にする（一覧のカードに出る。画像の無い記事はゲームの色の帯になる）

## 新しい記事を書き足す

`src/content/posts/` の下に Markdown を1本置き、PR で `main` に入れると公開される。
**置いた場所のパスがそのまま URL になる**（`src/content/posts/mhxr/events/new-event.md` → `/mhxr/events/new-event/`）。

```markdown
---
title: "記事のタイトル"
pubDate: "2026-10-24"
categories: ["カテゴリ"]
cover: "../../../images/2026-10-24-top.jpg"   # 一覧のカードに出す画像（省いてよい）
---

本文。画像は src/content/images/ に置き、記事の .md から見た相対パスで書く（縮小・変換される）。
```

- `original` は昔の記事の元の URL なので、新しい記事には書かない
- **新しい画像を `src/content/wp-content/` に置かない。** そこは `import.py` が毎回消して作り直す
- `scripts/import.py` を動かし直しても、手で足した記事は消えない。消すのは前回この道具が書いた記事
  （`scripts/imported.txt` に並んでいるもの）だけ。昔の記事と同じパスに置くと `import.py` が止まって知らせる

## 独自ドメインにするとき

`hazieta.com` は 2024-07-17 に失効していて、取り直せば使える。取り直したら:

1. `astro.config.mjs` の `site` を `https://hazieta.com`、`base` を `/` にする
2. `public/CNAME` に `hazieta.com` と1行書く
3. リポジトリの Settings → Pages の Custom domain に入れ、DNS を GitHub Pages に向ける

## ブランチ運用

**`main` と `task` の2種類だけを使う。** 作業は `task/<内容>` で行い、`main` へは GitHub 上の PR でだけ入れる。
`main` に入るとそのまま公開される。

## 公開の前に見たこと（2026-10-24）

- 画像 245 枚をコンタクトシートで全部見た。ゲームの画面・公式の告知画像・グッズの写真で、個人を特定できるものは無かった。
  画面に出ているのはゲーム内の名前（ハジー / Hazieta）だけ
- 本文に当時の連絡先メールアドレスが載っていたのはプライバシーポリシーだけで、取り込んでいない
- 公式の告知画像・ゲーム画面の著作権はそれぞれのゲームの権利者（カプコン、スクウェア・エニックス）にある。広告を貼らない個人の記録として出している

## 自動で付くもの（2026-10-25）

- 画像の説明（alt）: 空なら「記事のタイトル（写真 n）」。`scripts/fill_alt.py` が取り込みの最後と公開のたび（deploy.yml）に付ける
- 構造化データ（JSON-LD）: 記事は BlogPosting、それ以外は WebSite（`src/layouts/Base.astro`）
- RSS: `/rss.xml`（新しい50本、`src/pages/rss.xml.ts`）
- http の画像は取り込みで外す（https のページでは出ないため）
