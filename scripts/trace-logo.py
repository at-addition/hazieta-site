"""2色のロゴ画像を拡大・2値化してから輪郭をなぞり、SVG（線の形のデータ）にする。

    pip install --target <作業用> vtracer Pillow
    python scripts/trace-logo.py design/original/hazieta-header_1080x360.jpg out.svg invert   # 黒地に白のロゴ
    python scripts/trace-logo.py design/original/rabbit_400x400.jpg out.svg plain              # 白地に黒のロゴ

できた SVG は余白ごと元の画像の大きさなので、src/assets に置くときに viewBox を絵の外枠に詰めた（2026-10-24）。

SVG は拡大しても崩れないので、元の解像度の低さが消える。色は currentColor にして明暗どちらの画面でも使えるようにする。"""
import re, sys
from PIL import Image, ImageFilter, ImageOps
import vtracer

src, out, invert = sys.argv[1], sys.argv[2], sys.argv[3] == 'invert'
SCALE = 6
im = Image.open(src).convert('L')
w, h = im.size
big = im.resize((w * SCALE, h * SCALE), Image.LANCZOS).filter(ImageFilter.GaussianBlur(SCALE * 0.6))
if invert:                       # 白い図形を黒にしてからなぞる（なぞるのは黒い部分）
    big = ImageOps.invert(big)
bw = big.point(lambda v: 0 if v < 128 else 255, '1').convert('RGB')
tmp = out + '.png'
bw.save(tmp)
vtracer.convert_image_to_svg_py(tmp, out, colormode='binary', mode='spline',
                                filter_speckle=SCALE * 6, corner_threshold=60,
                                length_threshold=4.0, splice_threshold=45, path_precision=2)
svg = open(out, encoding='utf-8').read()
# 塗りを currentColor にし、viewBox を元の大きさに合わせる（座標は拡大後のまま、表示の大きさだけ元に戻す）
svg = re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="currentColor"', svg)
svg = re.sub(r'<svg[^>]*>', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w * SCALE} {h * SCALE}" width="{w}" height="{h}">', svg, count=1)
open(out, 'w', encoding='utf-8').write(svg)
print(out, len(svg), 'bytes', svg.count('<path'), 'paths')
