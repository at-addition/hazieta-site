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
