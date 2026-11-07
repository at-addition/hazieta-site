// 記事のパスの先頭（mhxr / sinoalice / other）から、どのゲームの記事かを決める。
// 色はカードの帯・バッジ・画像が無いときの背景に使う
export interface Game {
  key: string;
  label: string;
  short: string;
  hue: number;
}

export const GAMES: Game[] = [
  { key: 'mhxr', label: 'モンハンエクスプロア', short: 'MHXR', hue: 18 },
  { key: 'sinoalice', label: 'シノアリス', short: 'SINoALICE', hue: 285 },
  { key: 'other', label: 'そのほか', short: 'OTHER', hue: 190 },
];

export function gameOf(id: string): Game {
  return GAMES.find((g) => id.startsWith(g.key + '/')) ?? GAMES[GAMES.length - 1];
}

/** Markdown の本文から、カードに出す短い抜き出しを作る */
// 本文から説明文を抜き出す。オシャベの themes.ts と同じ（2026-11-07 にそろえた）
export function excerpt(body: string | undefined, len = 70): string {
  const text = (body ?? '')
    // 説明にしない行: 他の年の記事への案内や更新の注記（↓↓↓2018年版はこちら↓↓↓・※９月１２日更新・▼…）、
    // リンクだけの行（関連記事のカード）と、その抜粋（末尾が ... の行）
    .replace(/^[ 　]*(?:[↓▼※]|.*年(?:版|度)はこちら).*$/gm, '')
    .replace(/^[ 　]*(?:[-*][ 　]+)?\[.*\]\([^)]*\)[ 　]*$/gm, '')
    .replace(/^.*(?:\.\.\.|…)[ 　]*$/gm, '')
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/^#+\s.*$/gm, '')
    .replace(/https?:\/\/\S+/g, '')
    // Markdown の記号だけを消す。行頭の箇条書き・引用・区切り線と、強調・表の記号。語の中の - と _ は残す（#C-pla など。2026-11-06）
    .replace(/^[ 　]*(?:[-*_]{3,})[ 　]*$/gm, '')
    .replace(/^[ 　]*(?:[-*+>]|\d+\.)[ 　]+/gm, '')
    .replace(/[*`|]/g, '')
    // 空白と改行は詰める。ただし英語の語の間（Koala's March など）は1つ残す
    .replace(/\s+/g, (_, i: number, s: string) => (/[A-Za-z0-9'’.,!?]/.test(s[i - 1] ?? '') && /[A-Za-z0-9]/.test(s[i + _.length] ?? '') ? ' ' : ''))
    .trim();
  return text.length > len ? text.slice(0, len) + '…' : text;
}

// ゲームの一覧（/<ゲーム>/）と、その下のカテゴリの一覧（/<ゲーム>/<フォルダ>/）。記事のパスのフォルダがそのまま URL になる
export const sectionOf = (id: string) => id.split('/').slice(0, 2).join('/');
/** フォルダの見出し（そのフォルダの記事に多いカテゴリ名） */
export function sectionLabel(posts: { data: { categories: string[] } }[]): string {
  const n = new Map<string, number>();
  posts.forEach((p) => p.data.categories.forEach((c) => n.set(c, (n.get(c) ?? 0) + 1)));
  return [...n].sort((a, b) => b[1] - a[1])[0]?.[0] ?? '';
}
