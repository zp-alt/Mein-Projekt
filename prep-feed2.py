from PIL import Image
import numpy as np

UPLOADS = '/root/.claude/uploads/4fbaaefa-587b-500f-97a0-92a37d27c6eb'
OUT = '/home/user/Mein-Projekt'

def crop_square(img_path, out_path, focus_x=0.5, focus_y=0.5, quality=95):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    size = min(w, h)
    left = int((w - size) * focus_x)
    top  = int((h - size) * focus_y)
    left = max(0, min(left, w - size))
    top  = max(0, min(top,  h - size))
    img.crop((left, top, left + size, top + size)).save(out_path, quality=quality)
    print(f'Cropped: {out_path} ({size}x{size})')

# P7 — Vintage curls profile (portrait): focus upper-center on face
crop_square(f'{UPLOADS}/6cf200a5-IMG_8066.jpeg',
            f'{OUT}/feed-vintage-curls.jpg', focus_x=0.5, focus_y=0.12)

# P8 — Zyhra lying (landscape): focus on face/upper body on left side
crop_square(f'{UPLOADS}/2fe365da-IMG_0220.jpeg',
            f'{OUT}/feed-zyhra-lying.jpg', focus_x=0.02, focus_y=0.5)

# P9 — Chess/LV still life (portrait): center crop
crop_square(f'{UPLOADS}/46362c90-IMG_6946.jpeg',
            f'{OUT}/feed-chess-still.jpg', focus_x=0.5, focus_y=0.3)

# P10 — Shag mullet (portrait): focus on head+shoulders
crop_square(f'{UPLOADS}/c3843376-IMG_3164.jpeg',
            f'{OUT}/feed-shag-mullet.jpg', focus_x=0.5, focus_y=0.1)

# P11 — Nape line (portrait): focus on center/nape area — tight crop
crop_square(f'{UPLOADS}/6ede9078-IMG_0212.jpeg',
            f'{OUT}/feed-nape.jpg', focus_x=0.5, focus_y=0.3)

# P12 — 17:23 Magazine selective color: keep red lips, B&W rest
def selective_red(img_path, out_path):
    img = Image.open(img_path).convert('RGB')
    # Center-crop to square
    w, h = img.size
    size = min(w, h)
    left = (w - size) // 2
    top  = (h - size) // 2
    img = img.crop((left, top, left + size, top + size))

    arr = np.array(img, dtype=np.float32)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

    # Red lip detection: high red, low green/blue
    is_red = (r > 120) & (r > g * 1.6) & (r > b * 1.6) & (g < 110) & (b < 110)

    # Grayscale
    gray = 0.299 * r + 0.587 * g + 0.114 * b

    out = np.zeros_like(arr)
    for c, channel in enumerate([r, g, b]):
        out[:,:,c] = np.where(is_red, arr[:,:,c], gray)

    np.clip(out, 0, 255, out=out)
    Image.fromarray(out.astype(np.uint8)).save(out_path, quality=95)
    print(f'Selective color: {out_path}')

selective_red(f'{UPLOADS}/af689c17-1723_MAGAZINE_No.17_2025_7.jpeg',
              f'{OUT}/feed-magazine-selective.jpg')

print('All done.')
