"""
Hibrit illüzyon: hazır tablo + fotoğraf. Yapay zeka çizmez.
Tablonun ince fırça detayı (yüksek frekans) aynen kalır; çiçek bölgesinde
geniş açık-koyu dağılım (düşük frekans, LAB 'L' kanalı) fotoğrafın yüzüne göre
değiştirilir. Renk (a, b kanalları) tablodan gelir. Gözünü kısınca yüz çıkar.
"""
import io
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
_TPL_CACHE: dict = {}


def load_template(rel_path: str) -> Image.Image:
    if rel_path not in _TPL_CACHE:
        _TPL_CACHE[rel_path] = Image.open(os.path.join(HERE, rel_path)).convert("RGB")
    return _TPL_CACHE[rel_path].copy()


def photo_gray_square(raw: bytes, layout_params: dict | None):
    """Arka planı silinmiş, oval içine sığmış gri kare (1024). Başarısızsa düz kare."""
    import image_prep
    try:
        return image_prep.prepare_conditioning_image(raw, "cutout_strict", layout_params)
    except Exception as e:  # noqa: BLE001
        print("hibrit: cutout başarısız, düz kare:", e, flush=True)
        return image_prep.prepare_conditioning_image(raw, None, None)


def hybridize(raw: bytes, template_path: str, region: dict, layout_params: dict | None,
              strength: float = 24.0, sigma: float = 10.0) -> Image.Image:
    paint = load_template(template_path)
    W, H = paint.size

    face = photo_gray_square(raw, layout_params).convert("L")
    S = face.size[0]
    # composed oval (w=.88 S, h=.66 S, merkez .5/.38) -> tablodaki buket elipsine
    lp = layout_params or {}
    ow, oc_y = lp.get("w", 0.88), lp.get("cy", 0.38)
    cx, cy = region["cx"] * W, region["cy"] * H
    rw, rh = region["w"] * W, region["h"] * H
    scale = rw / (ow * S)
    side = int(S * scale)
    face_big = face.resize((side, side), Image.LANCZOS)
    canvas = Image.new("L", (W, H), 128)
    canvas.paste(face_big, (int(cx - 0.5 * side), int(cy - oc_y * side)))

    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([cx - rw / 2, cy - rh / 2, cx + rw / 2, cy + rh / 2], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(max(10, min(rw, rh) * 0.06)))
    m = np.asarray(mask, dtype=np.float32) / 255.0

    rgb = np.asarray(paint, dtype=np.float32) / 255.0
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    L = lab[..., 0]
    Llow = cv2.GaussianBlur(L, (0, 0), sigma)
    Lhigh = L - Llow

    f = np.asarray(canvas, dtype=np.float32) / 255.0
    f = cv2.GaussianBlur(f, (0, 0), max(1.0, sigma * 0.3))
    local_mean = float((Llow * m).sum() / max(m.sum(), 1.0))
    target = local_mean + (f - 0.5) * 2.0 * strength
    Llow_new = Llow * (1 - m) + target * m
    lab[..., 0] = np.clip(Llow_new + Lhigh, 0, 100)
    out = np.clip(cv2.cvtColor(lab, cv2.COLOR_LAB2RGB), 0, 1)
    return Image.fromarray((out * 255).astype(np.uint8))


def to_jpeg_bytes(img: Image.Image) -> bytes:
    b = io.BytesIO()
    img.save(b, format="JPEG", quality=92)
    return b.getvalue()
