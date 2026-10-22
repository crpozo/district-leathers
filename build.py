#!/usr/bin/env python3
"""Build demo/index.html from src/demo.html by embedding the images in src/img as data URIs.

Usage: python3 build.py
The demo must stay a single self-contained file (it is shown on an iPad, sometimes offline).
"""
import base64, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src', 'demo.html')
IMG = os.path.join(ROOT, 'src', 'img')
OUT = os.path.join(ROOT, 'demo', 'index.html')

# placeholder -> file in src/img
IMAGES = {
    'IMG_HIDE': 'hide.jpg',            # real leather photo (tinted per color)
    'IMG_JACKET': 'jacket.png',        # AI, flat, grayscale + alpha
    'IMG_PANTS': 'pants.png',          # AI, flat, fluid drape
    'IMG_PANTSCOW': 'pants_cow.png',   # AI, flat, structured drape
    'IMG_SEATS': 'seats.png',          # AI, 1967 Corvette front seats
    'IMG_SOFA': 'sofa.png',            # AI, two-seat sofa
    'IMG_MJACKET': 'm_jacket_base.jpg',    # AI, bomber on model (garment in lifted grayscale)
    'IMG_MJACKET_M': 'm_jacket_mask.png',  # mask of the jacket only
    'IMG_MPANTSF': 'm_pants_f_base.jpg',   # AI, pants on model, front
    'IMG_MPANTSF_M': 'm_pants_f_mask.png',
    'IMG_MPANTSB': 'm_pants_b_base.jpg',   # AI, pants on model, back
    'IMG_MPANTSB_M': 'm_pants_b_mask.png',
    'IMG_SAMPLE': 'sample_jacket.jpg',       # AI, customer-style photo of a cotton bomber (upload example)
    'IMG_SKETCH': 'sample_sketch.jpg',       # AI, pencil sketch of a bomber (upload example)
}
MIME = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}

def main():
    html = open(SRC, encoding='utf-8').read()
    total = 0
    for key, fn in IMAGES.items():
        path = os.path.join(IMG, fn)
        if not os.path.exists(path):
            sys.exit(f'missing image: {path}')
        data = open(path, 'rb').read(); total += len(data)
        uri = 'data:%s;base64,%s' % (MIME[os.path.splitext(fn)[1].lower()], base64.b64encode(data).decode('ascii'))
        html, n = re.subn(r'\{\{%s\}\}' % key, lambda m: uri, html)
        print(f'{key:16} {fn:22} {len(data)//1024:5} KB  x{n}')
    left = re.findall(r'\{\{[A-Z_]+\}\}', html)
    if left:
        sys.exit(f'unreplaced placeholders: {sorted(set(left))}')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(html)
    print(f'wrote {OUT}: {len(html)//1024} KB (images {total//1024} KB)')

if __name__ == '__main__':
    main()
