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
        "prompt": (
            "impressionist oil painting with thick palette knife strokes, "
            "still life of a lush round bouquet of vivid red roses with deep "
            "green leaves and a few small buds, in a round cream-white glazed "
            "ceramic vase with soft golden reflections, a fallen red rose and "
            "scattered red petals on a warm golden-brown wooden table, warm "
            "ochre gold and umber background with soft blue-gray patches, "
            "loose visible brushwork, rich saturated reds, warm sunlight, "
            "painting not photograph"
        ),
        "negative": NEGATIVE_BASE + ", studio photo, smooth digital art, sharp realistic details, pastel, pink roses, picture frame, border, second vase, cold dark background",
        "scale": 1.15, "guidance": 7.5, "steps": 20,
        "layout": "cutout",
        "layout_params": {"cx": 0.50, "cy": 0.38, "w": 0.88, "h": 0.66, "feather": 0.10, "bg": 24, "size": 0.68, "halo": 150, "dy": 0.02, "pad_top": 1.0, "fit": 0.92},
    },
}
