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
    "antika_sakayik": {
        "label": "Antika Şakayıklar",
        "prompt": (
            "masterpiece romantic baroque oil painting, still life with a huge "
            "lush bouquet of ruffled pink and cream-white peonies with olive "
            "green leaves and a few round pink peony buds, in a graceful "
            "teal-blue patinated ceramic amphora vase with two small curled "
            "handles and an ornate footed base, standing on an antique carved "
            "gilded rococo round wooden table with polished dark walnut top, "
            "on the table a rolled aged parchment scroll, old blank paper "
            "sheets with a red wax seal, a white feather quill in a dark green "
            "glass inkwell, an antique silver letter knife, one fallen pink "
            "peony and a loose pink silk ribbon, warm mottled ochre brown and "
            "umber weathered plaster wall, soft golden candlelight glow, "
            "painterly craquelure texture, rich warm old masters tones, "
            "highly detailed, painting not photograph"
        ),
        "negative": NEGATIVE_BASE + ", studio photo, smooth digital art, bright white background, neon colors, modern, picture frame, border, second vase, cold blue wall, readable writing, letters",
        "scale": 1.15, "guidance": 7.5, "steps": 20,
        "layout": "cutout",
        "layout_params": {"cx": 0.50, "cy": 0.38, "w": 0.88, "h": 0.66, "feather": 0.10, "bg": 24, "size": 0.68, "halo": 150, "dy": 0.02, "pad_top": 1.0, "fit": 0.92},
    },
}
