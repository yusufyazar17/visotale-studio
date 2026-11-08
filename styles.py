"""Stiller. Yeni stil eklemek = aşağıya bir blok eklemek."""

NEGATIVE_BASE = (
    "(low quality, worst quality:1.4), text, signature, watermark, blurry, "
    "deformed, photograph, realistic pasted face, 3d render, human, person, "
    "asymmetry, mutated, disfigured, extra limbs, cropped, out of frame, "
    "jpeg artifacts, duplicate, tiling, grainy, poorly drawn"
)

STYLES = {
    "klasik_barok": {
        "label": "Klasik Barok",
        "prompt": (
            "dark moody Dutch Golden Age oil painting of a baroque flower "
            "bouquet, loose wide fan-shaped bouquet of large creamy white "
            "peonies, long white freesia and tulip buds, deep burgundy-red "
            "carnations, royal purple bellflowers, a few soft pink roses and "
            "only two or three small orange accents, slender green stems and "
            "pointed leaves, short ornate antique aged-gold urn with a round "
            "medallion relief, dark worn wooden table, very dark mottled "
            "brown-black painterly background with visible brushwork, low-key "
            "dim lighting, strong chiaroscuro, deep shadows, rich dark jewel "
            "tones, thick oil paint texture, craquelure, Rembrandt "
            "atmosphere, painting not photograph"
        ),
        "negative": NEGATIVE_BASE + ", studio photo, bright background, flat gray wall, pastel peach, picture frame, border, second vase",
        "scale": 1.15, "guidance": 7.5, "steps": 20,
    },
    "beyaz_sakayik": {
        "label": "Beyaz Şakayık",
        "prompt": (
            "dark moody baroque still life oil painting, a large loose airy "
            "bouquet made only of ivory-white peonies with golden-yellow "
            "centers, white tulips and tiny white wildflowers with dark green "
            "leaves and stems, in a plain cream-white glazed ceramic round "
            "vase, white satin drape hanging on the left, a few white petals "
            "fallen on a dark polished wooden table, pitch black background, "
            "single soft light from the upper left, deep chiaroscuro, "
            "monochrome white and black palette, thick oil paint, painting "
            "not photograph"
        ),
        "negative": NEGATIVE_BASE + ", studio photo, bright background, colored flowers, orange, pink, purple, red, gold vase, picture frame, border",
        "scale": 1.15, "guidance": 7.5, "steps": 20,
    },
}
