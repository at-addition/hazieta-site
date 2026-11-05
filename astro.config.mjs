// @ts-check
import { defineConfig } from 'astro/config';

// GitHub Pages のプロジェクトサイトは /<リポジトリ名>/ の下に出る。独自ドメインにしたら base を '/' にする。
// 記事の本文の画像とリンクは相対パスで書いてある（scripts/import.py）ので、base を変えても記事は直さなくてよい
export default defineConfig({
  site: 'https://at-addition.github.io',
  base: '/hazieta-site',
  trailingSlash: 'always',
  // フォントのファイルは CSS に埋め込まない（4KB 未満が埋め込まれ、ページに無い文字の分まで毎回読ませていた。2026-11-06）
  vite: { build: { assetsInlineLimit: (file) => (/\.(woff2?|ttf)$/.test(file) ? false : undefined) } },
  // 昔の WordPress のカテゴリの一覧（/category/<ゲーム>/）を今のゲームの一覧へ送る
  redirects: { '/category/mhxr': '/hazieta-site/mhxr/', '/category/sinoalice': '/hazieta-site/sinoalice/', '/category/other': '/hazieta-site/other/' },
});
