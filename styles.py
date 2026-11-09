"""Stiller. Yeni stil eklemek = aşağıya bir blok eklemek."""

NEGATIVE_BASE = (
    "(low quality, worst quality:1.4), text, letters, writing, signature, watermark, "
    "blurry, deformed, photograph, realistic pasted face, 3d render, human, person, "
    "asymmetry, mutated, disfigured, extra limbs, cropped, out of frame, "
    "jpeg artifacts, duplicate, tiling, grainy, poorly drawn"
)

STYLES = {
    "aycicegi": {
        "label": "Ayçiçekleri",
        "prompt": (
            "thick impasto expressive oil painting, still life of a large "
            "bouquet of eleven big golden-orange sunflowers with dark brown "
            "spiral centers and ragged feathery petals, olive-green leaves, "
            "in a round rustic cobalt-blue glazed ceramic vase with cracked "
            "weathered surface and rust-orange patches, on a worn warm wooden "
            "table, deep textured cobalt and ultramarine blue wall behind, "
            "heavy palette knife strokes, visible raised paint ridges, bold "
            "post-impressionist brushwork, warm golden light against cool blue "
            "background, rich saturated colors, painting not photograph"
        ),
        "negative": NEGATIVE_BASE + ", studio photo, smooth digital art, flat colors, pastel, picture frame, border, second vase, muted dull colors",
        "scale": 1.15, "guidance": 7.5, "steps": 20,
        "layout": "cutout",
        "layout_params": {"cx": 0.50, "cy": 0.38, "w": 0.88, "h": 0.66, "feather": 0.10, "bg": 24, "size": 0.68, "halo": 150, "dy": 0.02, "pad_top": 1.0, "fit": 0.92},
    },
    "kirmizi_gul": {
        "label": "Kırmızı Güller",
        "engine": "sdxl",
        "template": "kirmizi_gul.jpg",  # hibrit model için (isteğe bağlı)
        "region": {"cx": 0.50, "cy": 0.36, "w": 0.90, "h": 0.52},
        "prompt": (
            "impressionist oil painting with visible brush strokes, a lush round "
            "bouquet of deep red roses with green leaves in a cream white "
            "ceramic vase, fallen red rose petals on a warm wooden table, "
            "golden brown painterly background, masterpiece"
        ),
        "negative": "white roses, yellow roses, pink roses, blue vase, glass vase, photograph, text, watermark, signature, people, frame",
        "sdxl_scale": 1.15,
        "scale": 1.15, "guidance": 7.0, "steps": 30,
        "layout": "cutout",
        "layout_params": {"cx": 0.50, "cy": 0.38, "w": 0.88, "h": 0.66, "feather": 0.10, "bg": 24, "size": 0.68, "halo": 150, "dy": 0.02, "pad_top": 1.0, "fit": 0.92},
    },
}
