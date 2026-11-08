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
    },
}
