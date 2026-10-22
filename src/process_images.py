#!/usr/bin/env python3
"""Turn the full-resolution AI photos (src/img/fullres) into the demo assets (src/img).

Flat product shots -> grayscale + alpha PNG (background removed by distance to white).
On-model shots (generated in neutral grey) -> original color JPEG + alpha mask of the garment only
(low saturation, mid luminance, flood-filled from a seed inside the garment, trimmed above/below).
The demo recolors them in the browser keeping each pixel's shading.
"""
import os, sys
from PIL import Image, ImageFilter, ImageOps, ImageChops, ImageDraw
import numpy as np
ROOT = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(ROOT, 'img', 'fullres'); OUT = os.path.join(ROOT, 'img')

FLAT = {'jacket': 40, 'pants': 62, 'pants_cow': 62, 'seats': 62, 'sofa': 48}   # white-distance threshold
MODEL = {'m_jacket': ((0.5, 0.40), 0.0, 1.0), 'm_pants_f': ((0.5, 0.62), 0.262, 0.955), 'm_pants_b': ((0.5, 0.60), 0.232, 0.935)}  # seed, top, bottom

def flat(name, th):
    im = Image.open(f'{SRC}/{name}.png').convert('RGB')
    a = np.asarray(im).astype(np.float32)
    dist = np.sqrt(((255 - a) ** 2).sum(axis=2))
    al = Image.fromarray((np.clip((dist - th) / 36, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(7)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    g = ImageOps.grayscale(im).convert('LA'); g.putalpha(al)
    bbox = al.point(lambda v: 255 if v > 40 else 0).getbbox(); x0, y0, x1, y1 = bbox; m = 24
    g.crop((max(0, x0 - m), max(0, y0 - m), min(im.width, x1 + m), min(im.height, y1 + m))).save(f'{OUT}/{name}.png', optimize=True)
    print(name, os.path.getsize(f'{OUT}/{name}.png') // 1024, 'KB')

def model(name, seed, top, bot):
    im = Image.open(f'{SRC}/{name}.png').convert('RGB'); w, h = im.size
    a = np.asarray(im).astype(np.float32) / 255
    mx = a.max(2); mn = a.min(2); sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    lum = .2126 * a[..., 0] + .7152 * a[..., 1] + .0722 * a[..., 2]
    m = (sat < 0.16) & (lum > 0.17) & (lum < 0.80)
    mi = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(11)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(7))
    mi = mi.point(lambda v: 255 if v > 110 else 0)
    sx, sy = int(w * seed[0]), int(h * seed[1])
    if mi.getpixel((sx, sy)) == 0:
        arr = np.asarray(mi); ys, xs = np.nonzero(arr); i = int(np.argmin((ys - sy) ** 2 + (xs - sx) ** 2)); sy, sx = int(ys[i]), int(xs[i])
    comp = mi.copy(); ImageDraw.floodfill(comp, (sx, sy), 128); comp = comp.point(lambda v: 255 if v == 128 else 0)
    inv = comp.point(lambda v: 0 if v else 255)
    for c in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        if inv.getpixel(c) == 255: ImageDraw.floodfill(inv, c, 128)
    comp = ImageChops.lighter(comp, inv.point(lambda v: 255 if v == 255 else 0))
    px = comp.load()
    for y in range(h):
        if y < int(h * top) or y > int(h * bot):
            for x in range(w): px[x, y] = 0
    comp = comp.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.6))
    mask = Image.new('RGBA', (w, h), (0, 0, 0, 0)); mask.putalpha(comp); mask.save(f'{OUT}/{name}_mask.png', optimize=True)
    im.save(f'{OUT}/{name}_base.jpg', quality=86, optimize=True)
    print(name, os.path.getsize(f'{OUT}/{name}_base.jpg') // 1024, 'KB base,', os.path.getsize(f'{OUT}/{name}_mask.png') // 1024, 'KB mask')

def plain(name, height=900, quality=84):
    im = Image.open(f'{SRC}/{name}.png').convert('RGB'); w, h = im.size
    im.resize((round(w * height / h), height), Image.LANCZOS).save(f'{OUT}/{name}.jpg', quality=quality, optimize=True)
    print(name, os.path.getsize(f'{OUT}/{name}.jpg') // 1024, 'KB')

if __name__ == '__main__':
    for n, th in FLAT.items(): flat(n, th)
    plain('sample_jacket')
    for n, (seed, top, bot) in MODEL.items(): model(n, seed, top, bot)
