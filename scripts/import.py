"""google-context に取り出した記事（Markdown）と画像を、この Astro サイトへ取り込む。

    python -I scripts/import.py

- 記事は src/content/posts/<元のパス>.md（元の URL と同じ道のりで出すため）
- 画像は src/content/<元のパス>（記事が指しているものだけ）
- 画像と元のサイト内へのリンク（http://hazieta.com/...）は、記事のページから見た相対パスにする。
  記事は /<base>/<元のパス>/ に出るので、サイトの根元まではパスの段数ぶん ../ を重ねる。
  相対にしておけば、GitHub Pages の /hazieta-site/ でも独自ドメインの / でも同じ記事で動く
- 固定ページ（目次・プライバシーポリシー・お問い合わせ）は取り込まない。目次はトップが代わりになり、
  プライバシーポリシーには当時の連絡先メールアドレスが書いてある
"""
import json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = 'hazieta.com'
SRC = rf'C:\@Addition\google-context\doc_txt\AdSenseブログ\{DOMAIN}\記事'
BIN = rf'C:\@Addition\google-context\doc_bin\AdSenseブログ\{DOMAIN}'
POSTS = os.path.join(ROOT, 'src', 'content', 'posts')
SKIP_PAGES = {'contents', 'privacy-policy', 'contact'}

# 前回この道具が書いた記事だけを消す。手で書き足した記事は消さない
IMPORTED = os.path.join(ROOT, 'scripts', 'imported.txt')
if os.path.exists(IMPORTED):
    for rel in open(IMPORTED, encoding='utf-8').read().split():
        p = os.path.join(POSTS, *rel.split('/'))
        if os.path.exists(p):
            os.remove(p)
os.makedirs(POSTS, exist_ok=True)
written = []
used, n, dropped = set(), 0, 0
for name in sorted(os.listdir(SRC)):
    text = open(os.path.join(SRC, name), encoding='utf-8').read()
    head, _, body = text.partition('\n---\n')
    meta = dict(re.findall(r'^- ([^:]+): (.*)$', head, re.M))
    title = re.search(r'^# (.*)$', head, re.M).group(1).strip()
    path = re.sub(r'^https?://[^/]+/', '', meta['元の URL']).strip('/')
    if path in SKIP_PAGES or not meta.get('公開'):
        continue

    up = '../' * len(path.split('/'))

    def local_img(m):
        rel = m.group(1)
        # 縮小版（-300x200.jpg）を指していても、元の大きさの画像が取れていればそちらを使う
        full = re.sub(r'-\d+x\d+(\.\w+)$', r'\1', rel)
        if full != rel and os.path.exists(os.path.join(BIN, *full.split('/'))):
            rel = full
        used.add(rel)
        return f']({up}{rel})'
    body = re.sub(r'\]\((?:\.\./)+doc_bin/AdSenseブログ/' + re.escape(DOMAIN) + r'/([^)]+)\)', local_img, body)
    # Wayback に残っていなかった自サイトの画像は、もう表示できないので落とす
    body, gone = re.subn(r'!\[[^\]]*\]\(https?://(?:www\.)?' + re.escape(DOMAIN) + r'/[^)]*\)\s*', '', body)
    dropped += gone
    body = re.sub(r'\]\(https?://(?:www\.)?' + re.escape(DOMAIN) + r'/([^)]*)\)', lambda m: f']({up}{m.group(1)})', body)
    body = re.sub(r'\]\(//', '](https://', body)

    fm = {
        'title': title,
        'pubDate': meta['公開'],
        'categories': [c.strip() for c in meta.get('カテゴリ', '').split(',') if c.strip()],
        'original': meta['元の URL'],
    }
    if meta.get('更新'):
        fm['updatedDate'] = meta['更新']
    # 一覧のカードに出す画像は、本文の最初の画像（記事の .md から見た相対パス。Astro が縮小して出す）
    first = re.search(r'!\[[^\]]*\]\((\.\./[^)]+)\)', body)
    if first:
        fm['cover'] = first.group(1)
    lines = ['---'] + [f'{k}: {json.dumps(v, ensure_ascii=False)}' for k, v in fm.items()] + ['---', '']
    dst = os.path.join(POSTS, *path.split('/')) + '.md'
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        sys.exit(f'{dst} は手で書いた記事と重なっている。どちらかの場所を変える')
    open(dst, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + body.strip() + '\n')
    written.append(path + '.md')
    n += 1

# 画像は src/content/wp-content に置く。記事の .md から見た相対パスがそのままここを指し、
# Astro が画像として取り込んで（縮小・変換して）出力する
IMAGES = os.path.join(ROOT, 'src', 'content')
shutil.rmtree(os.path.join(IMAGES, 'wp-content'), ignore_errors=True)
for rel in sorted(used):
    s, d = os.path.join(BIN, *rel.split('/')), os.path.join(IMAGES, *rel.split('/'))
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)
open(os.path.join(ROOT, 'scripts', 'images.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(sorted(used)) + '\n')
# http の画像は https のページから読み込まれず崩れて見えるので外す（2026-10-25 本人指示）
http_dropped = 0
for rel in written:
    f = os.path.join(POSTS, *rel.split('/'))
    s = open(f, encoding='utf-8').read()
    s2, k = re.subn(r'!\[(?:[^\[\]]|\[[^\]]*\])*\]\(http://[^)]*\)', '', s)
    if k:
        http_dropped += k
        open(f, 'w', encoding='utf-8', newline='\n').write(s2)
print('http images dropped', http_dropped, file=sys.stderr)

# 書いた記事の中の、サイト内に無いページへのリンク（昔の WordPress のカテゴリ・タグの一覧や、2ページ目など）は
# 開くと「見つかりません」になるので、リンクを外して文字だけ残す。画像と、実在する記事・手で足した記事へのリンクは残す
pages = {os.path.relpath(os.path.join(dp, f), POSTS).replace(os.sep, '/')[:-3]
         for dp, _, fs in os.walk(POSTS) for f in fs if f.endswith('.md')}
unlinked = 0
for rel in written:
    f = os.path.join(POSTS, *rel.split('/'))
    here = rel[:-3]   # 記事は /<パス>/ に出るので、リンクはそのフォルダから見た相対
    s = open(f, encoding='utf-8').read()

    def fix(m):
        global unlinked
        text, url = m.group(1), m.group(2)
        target = os.path.normpath(os.path.join(here, url.split('#')[0])).replace(os.sep, '/').strip('/')
        if url.startswith('http') or target.startswith('wp-content') or target in pages or target == '.':
            return m.group(0)
        unlinked += 1
        return text
    s2 = re.sub(r'(?<!!)\[((?:[^\[\]]|!\[[^\]]*\]\([^)]*\))*)\]\((\.\./[^)\s]*)\)', fix, s)
    if s2 != s:
        open(f, 'w', encoding='utf-8', newline='\n').write(s2)
print('unlinked', unlinked, file=sys.stderr)
open(IMPORTED, 'w', encoding='utf-8', newline='\n').write('\n'.join(sorted(written)) + '\n')

# 画像の説明（alt）を付ける。新しい記事は公開のたびに同じ道具が付ける
import subprocess
subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'scripts', 'fill_alt.py')], check=True)
print('posts', n, 'images', len(used), 'dropped', dropped, file=sys.stderr)
