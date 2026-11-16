
from pathlib import Path
from PIL import Image
import numpy as np
import re

image_folder = Path("data/images")
mask_folder = Path("data/masks")
output_folder = Path("outputs/overlays")

output_folder.mkdir(parents=True, exist_ok=True)

# Main teal room colour
room_color = np.array([0, 142, 142])

# Process first 3 floor plans
for plan_id in [1, 2, 3]:

    image_file = image_folder / f"{plan_id}.png"

    # Find corresponding mask
    mask_files = [
        f for f in mask_folder.glob("*.png")
        if re.match(rf"^{plan_id}(?:\s|\.|\()", f.name)
    ]

    if not image_file.exists() or not mask_files:
        print("Missing image or mask for plan:", plan_id)
        continue

    mask_file = mask_files[0]

    original = Image.open(image_file).convert("RGB")
    mask = Image.open(mask_file).convert("RGB")

    if original.size != mask.size:
        print("Dimension mismatch:", plan_id)
        continue

    original_array = np.array(original)
    mask_array = np.array(mask)

    # Detect teal room pixels and nearby shades
    distance = np.sqrt(
        np.sum(
            (mask_array.astype(np.int16)
             - room_color.astype(np.int16)) ** 2,
            axis=2
        )
    )

    room_pixels = distance <= 5

    # Create coloured overlay
    result = original_array.copy()

    overlay_color = np.array([0, 255, 0])

    result[room_pixels] = (
        0.55 * original_array[room_pixels]
        + 0.45 * overlay_color
    ).astype(np.uint8)

    output_file = output_folder / f"plan_{plan_id}_overlay.png"

    Image.fromarray(result).save(output_file)

    print("Created:", output_file)

print("\nTHREE PLAN OVERLAYS COMPLETED")
