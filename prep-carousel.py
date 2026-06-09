from PIL import Image
import numpy as np

UPLOADS = '/root/.claude/uploads/4fbaaefa-587b-500f-97a0-92a37d27c6eb'
OUT = '/home/user/Mein-Projekt'

def crop_square(src, dst, fx=0.5, fy=0.2, quality=95):
    img = Image.open(src).convert('RGB')
    w, h = img.size
    s = min(w, h)
    left = int((w - s) * fx)
    top  = int((h - s) * fy)
    left = max(0, min(left, w - s))
    top  = max(0, min(top,  h - s))
    img.crop((left, top, left+s, top+s)).save(dst, quality=quality)
    print(f'Saved {dst}  ({s}x{s})')

# Platinum/ash undercut man (IMG_1141) — face center
crop_square(f'{UPLOADS}/635c52ec-IMG_1141.jpeg',
            f'{OUT}/carousel-undercut.jpg', fx=0.5, fy=0.1)

# Silver pixie woman (IMG_1365) — face lower-center
crop_square(f'{UPLOADS}/d201b456-IMG_1365.jpeg',
            f'{OUT}/carousel-pixie.jpg', fx=0.5, fy=0.3)

# Natural silver bob (PHOTO20260109130056) — face upper-center
crop_square(f'{UPLOADS}/9c867d83-PHOTO20260109130056.jpeg',
            f'{OUT}/carousel-silver-bob.jpg', fx=0.5, fy=0.1)

# Fashion editorial crouching (IMG_0221) — full upper crop
crop_square(f'{UPLOADS}/9f563a2a-IMG_0221.jpeg',
            f'{OUT}/carousel-editorial.jpg', fx=0.3, fy=0.0)

print('All done.')
