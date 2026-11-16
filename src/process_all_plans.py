
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
import re

# Project folders
image_folder = Path("data/images")
mask_folder = Path("data/masks")
output_folder = Path("outputs")
output_folder.mkdir(exist_ok=True)

# Provisional room colour in RGB
ROOM_COLOR = np.array([0, 142, 142])
COLOR_TOLERANCE = 5
MIN_AREA = 5000

def get_plan_number(filename):
    match = re.match(r"(\d+)", filename)
    return match.group(1) if match else None

# Match images and masks using their plan numbers
images = {
    get_plan_number(p.name): p
    for p in image_folder.glob("*.png")
    if get_plan_number(p.name)
}

masks = {
    get_plan_number(p.name): p
    for p in mask_folder.glob("*.png")
    if get_plan_number(p.name)
}

all_regions = []

for plan_number in sorted(images.keys(), key=int):

    if plan_number not in masks:
        print(f"Mask missing for plan {plan_number}")
        continue

    mask = cv2.imread(str(masks[plan_number]))

    if mask is None:
        print(f"Could not read mask for plan {plan_number}")
        continue

    # Convert RGB room colour to OpenCV BGR
    room_color_bgr = ROOM_COLOR[::-1]

    difference = np.abs(
        mask.astype(np.int16) -
        room_color_bgr.astype(np.int16)
    )

    binary_mask = np.all(
        difference <= COLOR_TOLERANCE,
        axis=2
    ).astype(np.uint8)

    count, labels, stats, centers = (
        cv2.connectedComponentsWithStats(binary_mask, 8)
    )

    room_number = 1

    for i in range(1, count):

        x, y, width, height, area = stats[i]

        if area < MIN_AREA:
            continue

        center_x, center_y = centers[i]

        all_regions.append({
            "Plan_ID": plan_number,
            "Room_ID": f"R{room_number}",
            "Area_Pixels": int(area),
            "X": int(x),
            "Y": int(y),
            "Width": int(width),
            "Height": int(height),
            "Center_X": round(center_x, 2),
            "Center_Y": round(center_y, 2),
            "Room_Type": "Unknown"
        })

        room_number += 1

# Save results
df = pd.DataFrame(all_regions)

output_file = output_folder / "all_plans_regions.csv"
df.to_csv(output_file, index=False)

print("ALL FLOOR PLANS PROCESSED")
print("-------------------------")
print("Plans found:", len(images))
print("Matched plans:", len(set(images) & set(masks)))
print("Total regions:", len(df))
print("Saved:", output_file)
