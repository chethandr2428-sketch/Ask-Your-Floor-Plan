
from pathlib import Path
from PIL import Image
import numpy as np
import cv2
import re

image_folder = Path("data/images")
mask_folder = Path("data/masks")
output_folder = Path("outputs/labeled_rooms")

output_folder.mkdir(parents=True, exist_ok=True)

room_color = np.array([0, 142, 142])

for plan_id in [1, 2, 3]:

    original = np.array(
        Image.open(image_folder / f"{plan_id}.png").convert("RGB")
    )

    mask_files = [
        f for f in mask_folder.glob("*.png")
        if re.match(rf"^{plan_id}(?:\s|\.|\()", f.name)
    ]

    if not mask_files:
        print("Mask missing:", plan_id)
        continue

    mask = np.array(
        Image.open(mask_files[0]).convert("RGB")
    )

    if original.shape != mask.shape:
        print("Image size mismatch:", plan_id)
        continue

    distance = np.sqrt(
        np.sum(
            (mask.astype(np.int16) -
             room_color.astype(np.int16)) ** 2,
            axis=2
        )
    )

    binary = (distance <= 5).astype(np.uint8)

    count, labels, stats, centers = (
        cv2.connectedComponentsWithStats(binary, 8)
    )

    result = cv2.cvtColor(original, cv2.COLOR_RGB2BGR)

    region_number = 0

    for i in range(1, count):

        area = stats[i, cv2.CC_STAT_AREA]

        if area < 5000:
            continue

        region_number += 1

        component = (labels == i).astype(np.uint8)

        contours, _ = cv2.findContours(
            component,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        cv2.drawContours(
            result, contours, -1, (0, 0, 255), 3
        )

        cx, cy = centers[i]

        cv2.putText(
            result,
            f"R{region_number}",
            (int(cx), int(cy)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2
        )

    output_file = (
        output_folder / f"plan_{plan_id}_labeled.png"
    )

    cv2.imwrite(str(output_file), result)

    print(
        f"Plan {plan_id}: {region_number} regions detected"
    )

print("\nROOM REGION VISUALIZATION COMPLETED")
