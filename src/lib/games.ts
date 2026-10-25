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
export function excerpt(body: string | undefined, len = 70): string {
  const text = (body ?? '')
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/^#+\s.*$/gm, '')
    .replace(/[*_`>|-]/g, '')
    .replace(/\s+/g, '')
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
