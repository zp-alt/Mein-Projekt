from PIL import Image
import numpy as np

SRC = '/root/.claude/uploads/4fbaaefa-587b-500f-97a0-92a37d27c6eb/833e75ee-245E9C4CF490459D8EE586060000AAB9.png'
OUT = '/home/user/Mein-Projekt'

def sepia(arr):
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    sr = np.clip(r*0.393 + g*0.769 + b*0.189, 0, 255)
    sg = np.clip(r*0.349 + g*0.686 + b*0.168, 0, 255)
    sb = np.clip(r*0.272 + g*0.534 + b*0.131, 0, 255)
    return np.stack([sr, sg, sb], axis=2)

def bw(arr):
    gray = 0.299*arr[:,:,0] + 0.587*arr[:,:,1] + 0.114*arr[:,:,2]
    return np.stack([gray, gray, gray], axis=2)

# Crop to square (864x864) — face is upper-center
img = Image.open(SRC).convert('RGB')
w, h = img.size  # 864x1536
size = w          # 864 — use full width
top  = int(h * 0.04)   # slight top crop to catch full face + hair
img  = img.crop((0, top, size, top + size))
arr  = np.array(img, dtype=np.float32)

# ── Variant A: Radial blend — face in color, edges fade to sepia ──
def radial_sepia(arr, cx=0.5, cy=0.32, r=0.38, softness=0.45):
    sz = arr.shape[0]
    Y, X = np.mgrid[0:sz, 0:sz]
    dist = np.sqrt(((X/sz) - cx)**2 + ((Y/sz) - cy)**2)
    mask = np.clip((dist - r) / softness, 0, 1)
    mask = mask[:,:,np.newaxis]
    sep = sepia(arr)
    return arr * (1 - mask) + sep * mask

varA = np.clip(radial_sepia(arr), 0, 255).astype(np.uint8)
Image.fromarray(varA).save(f'{OUT}/zyhra-portrait-A.jpg', quality=95)
print('Saved A: radial color→sepia')

# ── Variant B: Full warm sepia ──
varB = np.clip(sepia(arr), 0, 255).astype(np.uint8)
Image.fromarray(varB).save(f'{OUT}/zyhra-portrait-B.jpg', quality=95)
print('Saved B: full sepia')

# ── Variant C: B&W with 15% original color tint (desaturated, not dead) ──
bw_arr = bw(arr)
varC = np.clip(bw_arr * 0.85 + arr * 0.15, 0, 255).astype(np.uint8)
Image.fromarray(varC).save(f'{OUT}/zyhra-portrait-C.jpg', quality=95)
print('Saved C: near-B&W with warm tint')

print('Done.')
