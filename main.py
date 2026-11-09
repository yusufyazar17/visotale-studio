"""
Visotale Studio — temiz, bağımsız üretim servisi.
Gerekli ortam değişkenleri (Railway → Variables):
  FAL_KEY        fal.ai anahtarı
  TEST_PASSWORD  stüdyo şifresi
  MAX_RUNS       (isteğe bağlı) en fazla üretim sayısı, varsayılan 300
Adresler: /studio (arayüz), /health
"""
import base64, hmac, io, json, os, re, threading, time, uuid

import requests
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, Response
from PIL import Image, ImageOps

from styles import STYLES
from image_prep import prepare_conditioning_image, to_data_uri
from ui import STUDIO_HTML

FAL_KEY = os.environ.get("FAL_KEY", "")
PASSWORD = os.environ.get("TEST_PASSWORD", "")
MAX_RUNS = int(os.environ.get("MAX_RUNS", "300"))
FAL_URL = "https://queue.fal.run/fal-ai/illusion-diffusion"
MODAL_URL = os.environ.get("MODAL_URL", "")
MODAL_SECRET = os.environ.get("MODAL_SECRET", "")
FLUX_URL = "https://queue.fal.run/fal-ai/flux-general"
FLUX_CN = os.environ.get("FLUX_CONTROLNET", "Shakker-Labs/FLUX.1-dev-ControlNet-Union-Pro")
MAX_UPLOAD = 20 * 1024 * 1024

app = FastAPI()
JOBS: dict = {}
RESULTS: dict = {}   # hibrit sonuçları (bellekte, son 40)
LOCK = threading.Lock()
RUNS = 0


def clamp(v, lo, hi, default):
    try:
        return max(lo, min(hi, float(v)))
    except (TypeError, ValueError):
        return default


def find_url(x):
    """fal cevabında (images listesi, image nesnesi vb.) ilk görsel url'sini bul."""
    if isinstance(x, dict):
        u = x.get("url")
        if isinstance(u, str) and u.startswith("http"):
            return u
        for k in ("images", "image", "output", "data"):
            if k in x:
                r = find_url(x[k])
                if r:
                    return r
        for v in x.values():
            r = find_url(v)
            if r:
                return r
    elif isinstance(x, list):
        for v in x:
            r = find_url(v)
            if r:
                return r
    return None


def prepare(raw: bytes) -> str:
    """Fotoğraf -> 1024x1024 gri kare (data URI)."""
    img = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("L")
    w, h = img.size
    s = min(w, h)
    left = (w - s) // 2
    top = int((h - s) * 0.25)  # portrelerde yüzü yukarıda tut
    img = img.crop((left, top, left + s, top + s)).resize((1024, 1024), Image.LANCZOS)
    img = ImageOps.autocontrast(img, cutoff=1).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def build_conditioning(raw: bytes, p: dict) -> str:
    if p.get("layout") == "cutout":
        try:
            img = prepare_conditioning_image(raw, "cutout_strict", p.get("layout_params"))
            return to_data_uri(img)
        except Exception as e:  # arka plan silinemezse düz kareye dön
            print("cutout başarısız, düz kare:", e, flush=True)
    return prepare(raw)


def blur_data_uri(uri: str, radius: float) -> str:
    """Kontrol görselini bulanıklaştır: Flux ince ayrıntıyı kopyalayamasın, sadece açık/koyu kütleleri izlesin."""
    if radius <= 0:
        return uri
    from PIL import ImageFilter
    img = Image.open(io.BytesIO(base64.b64decode(uri.split(",", 1)[1]))).convert("RGB")
    img = img.filter(ImageFilter.GaussianBlur(radius))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def strip_weights(s: str) -> str:
    """Flux (T5) '(metin:1.4)' ağırlık sözdizimini anlamaz; parantezi ve ağırlığı at."""
    return re.sub(r"\(([^()]*?):\s*[0-9.]+\)", r"\1", s)


def run_hybrid(job_id: str, raw: bytes, p: dict):
    try:
        import hybrid
        style = STYLES[p["style"]]
        img = hybrid.hybridize(
            raw, style["template"], style["region"], style.get("hy_layout") or style.get("layout_params"),
            strength=p["hy_strength"], sigma=p["hy_sigma"],
        )
        RESULTS[job_id] = hybrid.to_jpeg_bytes(img)
        while len(RESULTS) > 40:
            RESULTS.pop(next(iter(RESULTS)))
        JOBS[job_id] = {"status": "done", "image_url": f"/api/result/{job_id}.jpg"}
    except Exception as e:  # noqa: BLE001
        JOBS[job_id] = {"status": "error", "error": str(e)}


def run_sdxl(job_id: str, raw: bytes, p: dict):
    """SDXL + QR Monster (Modal GPU). Soğuk açılışta ilk istek ~1 dk sürebilir."""
    try:
        if not MODAL_URL or not MODAL_SECRET:
            raise RuntimeError("MODAL_URL / MODAL_SECRET tanımlı değil (Railway Variables).")
        cond = build_conditioning(raw, p)
        body = {
            "secret": MODAL_SECRET,
            "image_b64": cond.split(",", 1)[1],
            "prompt": strip_weights(p["prompt"]),
            "negative_prompt": strip_weights(p["negative"]),
            "scale": p["sdxl_scale"],
            "end": p["cn_end"],
            "steps": p["steps"] if p["steps"] >= 25 else 30,
            "guidance": p["guidance"] if p["guidance"] <= 9 else 7.0,
        }
        r = requests.post(MODAL_URL, json=body, timeout=280)
        if not r.ok:
            raise RuntimeError(f"Modal hata {r.status_code}: {r.text[:300]}")
        data = base64.b64decode(r.json()["image_b64"])
        RESULTS[job_id] = data
        while len(RESULTS) > 40:
            RESULTS.pop(next(iter(RESULTS)))
        JOBS[job_id] = {"status": "done", "image_url": f"/api/result/{job_id}.jpg"}
    except Exception as e:  # noqa: BLE001
        JOBS[job_id] = {"status": "error", "error": str(e)}


def run_job(job_id: str, raw: bytes, p: dict):
    if p["engine"] == "hibrit":
        return run_hybrid(job_id, raw, p)
    if p["engine"] == "sdxl":
        return run_sdxl(job_id, raw, p)
    try:
        if not FAL_KEY:
            raise RuntimeError("FAL_KEY tanımlı değil.")
        cond = build_conditioning(raw, p)
        if p["engine"] == "flux":
            cond = blur_data_uri(cond, p["blur"])
            url_q = FLUX_URL
            payload = {
                "prompt": strip_weights(p["prompt"]),
                "image_size": "square_hd",
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "output_format": "jpeg",
                "controlnet_unions": [{
                    "path": FLUX_CN,
                    "controls": [{
                        "control_mode": p["mode"],
                        "control_image_url": cond,
                        "conditioning_scale": p["flux_scale"],
                        "start_percentage": 0.0,
                        "end_percentage": p["cn_end"],
                    }],
                }],
            }
        else:
            url_q = FAL_URL
            payload = {
                "image_url": cond,
                "prompt": p["prompt"],
                "negative_prompt": p["negative"],
                "controlnet_conditioning_scale": p["scale"],
                "guidance_scale": p["guidance"],
                "num_inference_steps": p["steps"],
                "control_guidance_end": 1.0,
                "image_size": "square_hd",
            }
        h = {"Authorization": f"Key {FAL_KEY}", "Content-Type": "application/json"}
        sub = requests.post(url_q, json=payload, headers=h, timeout=30)
        if not sub.ok:
            raise RuntimeError(f"fal hata {sub.status_code}: {sub.text[:300]}")
        d = sub.json()
        deadline = time.time() + 180
        while True:
            if time.time() > deadline:
                raise RuntimeError("Zaman aşımı.")
            time.sleep(2)
            try:
                s = requests.get(d["status_url"], headers=h, timeout=15).json()
            except Exception:
                continue
            if s.get("status") == "COMPLETED":
                break
            if s.get("status") in ("FAILED", "ERROR"):
                raise RuntimeError("fal üretimi başarısız: " + str(s)[:300])
        r = requests.get(d["response_url"], headers=h, timeout=20)
        if not r.ok:
            raise RuntimeError(f"fal sonuç hatası: {r.text[:300]}")
        data = r.json()
        url = find_url(data)
        if not url:
            raise RuntimeError("Sonuç biçimi tanınmadı: " + json.dumps(data)[:300])
        JOBS[job_id] = {"status": "done", "image_url": url}
    except Exception as e:  # noqa: BLE001
        JOBS[job_id] = {"status": "error", "error": str(e)}


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/studio", response_class=HTMLResponse)
def studio():
    styles = [{"key": k, "label": v["label"]} for k, v in STYLES.items()]
    defaults = {
        k: {
            "prompt": v["prompt"], "negative_prompt": v["negative"],
            "conditioning_scale": v["scale"], "guidance_scale": v["guidance"],
            "num_inference_steps": v["steps"], "control_guidance_end": 1.0,
            "layout": v.get("layout", "none"),
            "engine": v.get("engine", "illusion"),
        }
        for k, v in STYLES.items()
    }
    return (STUDIO_HTML.replace("__STYLES__", json.dumps(styles, ensure_ascii=False))
            .replace("__DEFAULTS__", json.dumps(defaults, ensure_ascii=False)))


@app.post("/api/generate")
async def generate(
    password: str = Form(...), style: str = Form(...), file: UploadFile = File(...),
    prompt: str | None = Form(None), negative_prompt: str | None = Form(None),
    conditioning_scale: str | None = Form(None), delta: str | None = Form(None),
    engine: str | None = Form(None), mode: str | None = Form(None),
    cn_end: str | None = Form(None), hy_strength: str | None = Form(None),
    hy_sigma: str | None = Form(None), blur: str | None = Form(None), guidance_scale: str | None = Form(None),
    num_inference_steps: str | None = Form(None), layout: str | None = Form(None),
):
    global RUNS
    if not PASSWORD:
        return JSONResponse(status_code=503, content={"ok": False, "error": "TEST_PASSWORD tanımlı değil."})
    if not hmac.compare_digest(password.encode(), PASSWORD.encode()):
        return JSONResponse(status_code=401, content={"ok": False, "error": "Şifre yanlış."})
    base = STYLES.get(style)
    if not base:
        return JSONResponse(status_code=400, content={"ok": False, "error": "Geçersiz stil."})
    raw = file.file.read()
    if not raw or len(raw) > MAX_UPLOAD:
        return JSONResponse(status_code=400, content={"ok": False, "error": "Dosya geçersiz (boş ya da 20MB üstü)."})
    try:
        Image.open(io.BytesIO(raw)).verify()
    except Exception:
        return JSONResponse(status_code=400, content={"ok": False, "error": "Bu dosya bir görsel değil."})
    with LOCK:
        if RUNS >= MAX_RUNS:
            return JSONResponse(status_code=429, content={"ok": False, "error": f"Üretim sınırına ulaşıldı ({MAX_RUNS})."})
        RUNS += 1
    p = {
        "prompt": (prompt or "").strip()[:2000] or base["prompt"],
        "negative": (negative_prompt or "").strip()[:2000] or base["negative"],
        "scale": clamp(conditioning_scale, 0.5, 1.6, base["scale"]),
        "flux_scale": clamp(base.get("flux_scale", 0.6) + clamp(delta, -0.3, 0.3, 0.0) * 2, 0.2, 1.2, 0.65),
        "style": style,
        "sdxl_scale": clamp(base.get("sdxl_scale", 1.0) + clamp(delta, -0.3, 0.3, 0.0) * 1.5, 0.4, 1.8, 1.0),
        "hy_strength": clamp(clamp(hy_strength, 5, 60, 38) + clamp(delta, -0.3, 0.3, 0.0) * 100, 5, 60, 38),
        "hy_sigma": clamp(hy_sigma, 3, 30, 12),
        "engine": engine if engine in ("flux", "illusion", "hibrit", "sdxl") else base.get("engine", "illusion"),
        "mode": mode if mode in ("blur", "tile", "low-quality", "gray", "depth", "canny") else "blur",
        "cn_end": clamp(cn_end, 0.2, 1.0, 0.65),
        "blur": clamp(blur, 0, 40, 8),
        "guidance": clamp(guidance_scale, 1, 20, base["guidance"]),
        "steps": int(clamp(num_inference_steps, 10, 50, base["steps"])),
        "layout": layout if layout in ("cutout", "none") else base.get("layout", "none"),
        "layout_params": base.get("layout_params"),
    }
    job_id = uuid.uuid4().hex
    JOBS[job_id] = {"status": "pending"}
    threading.Thread(target=run_job, args=(job_id, raw, p), daemon=True).start()
    return {"ok": True, "job_id": job_id}


@app.get("/api/result/{name}")
def result(name: str):
    data = RESULTS.get(name.rsplit(".", 1)[0])
    if not data:
        return JSONResponse(status_code=404, content={"ok": False})
    return Response(content=data, media_type="image/jpeg")


@app.get("/api/job/{job_id}")
def job(job_id: str):
    j = JOBS.get(job_id)
    if not j:
        return JSONResponse(status_code=404, content={"ok": False, "status": "error", "error": "İş bulunamadı."})
    return {"ok": j["status"] != "error", **j}
