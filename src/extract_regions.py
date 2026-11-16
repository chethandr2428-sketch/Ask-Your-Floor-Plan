
from pathlib import Path
from PIL import Image
import numpy as np
import cv2
import csv

mask_path = Path("data/masks/1 (2).png")
output_path = Path("outputs")

output_path.mkdir(exist_ok=True)

# Read mask
mask = np.array(Image.open(mask_path).convert("RGB"))

# Find unique colours
pixels = mask.reshape(-1, 3)
colors, counts = np.unique(
    pixels, axis=0, return_counts=True
)

results = []

for color, count in zip(colors, counts):

    # Ignore black background
    if np.array_equal(color, [0, 0, 0]):
        continue

    # Create binary mask for this colour
    binary = np.all(mask == color, axis=2).astype(np.uint8)

    # Find connected regions
    num_labels, labels, stats, centroids = (
        cv2.connectedComponentsWithStats(binary, 8)
    )

    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        cx, cy = centroids[i]

        # Ignore very small regions
        if area < 20:
            continue

        results.append({
            "red": int(color[0]),
            "green": int(color[1]),
            "blue": int(color[2]),
            "area_pixels": int(area),
            "x": int(x),
            "y": int(y),
            "width": int(w),
            "height": int(h),
            "center_x": round(float(cx), 2),
            "center_y": round(float(cy), 2)
        })

# Save results
csv_path = output_path / "plan_1_regions.csv"

if results:
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

print("REGION EXTRACTION COMPLETED")
print("Total regions:", len(results))
print("Saved to:", csv_path)
