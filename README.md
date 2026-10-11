# District Leathers · Fitting Room & Hide Calculator

Prototype for the "Imagine it in our leather" tool: pick a District leather, describe the piece, see it in that leather, get the number of hides from the same lot.

- Demo: `/demo/` (static, no Shopify connection, fixed data)
- Hosted with GitHub Pages from `main` (root)

## Structure

```
index.html        → redirects to /demo/
demo/index.html   → the demo (self-contained, built; do not edit by hand)
src/demo.html     → demo source with {{IMG_*}} placeholders
src/img/          → photos (AI-generated garments, real hide photo, masks)
build.py          → embeds src/img into src/demo.html → demo/index.html
```

Build: `python3 build.py` (Python 3, no dependencies).

Screens: product page (0), fitting room (1, 2, 10, 11), calculator (3), compare (8), cutting map (9), custom project (5), and static mockups of account (4), panel (6) and follow-up (7). The demo opens on the fitting room; the other screens are reached from the flow itself or by hash (`#product`, `#calc`, `#compare`, `#cutmap`, `#project`, `#more`).

Live AI: tap the LD logo 5 times (or open `#setup`) to save an image API key on the device. Without it, or when the call fails or the device is offline, the demo falls back to the pregenerated images.
