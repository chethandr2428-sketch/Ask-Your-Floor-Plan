
from PIL import Image
import numpy as np
import cv2
from pathlib import Path

# Load segmentation mask
mask = np.array(
    Image.open("data/masks/1 (2).png").convert("RGB")
)

# Exact room colour
room_color = np.array([0, 142, 142])

# Identify exact room pixels
room_mask = np.all(mask == room_color, axis=2)

# Convert to binary image
binary = room_mask.astype(np.uint8)

# Detect connected room regions
count, labels, stats, centers = (
    cv2.connectedComponentsWithStats(binary, 8)
)

print("ROOM SEPARATION ANALYSIS")
print("-" * 40)

result = cv2.cvtColor(mask, cv2.COLOR_RGB2BGR)

room_number = 0

for i in range(1, count):

    area = stats[i, cv2.CC_STAT_AREA]

    # Ignore very small regions
    if area < 5000:
        continue

    room_number += 1

    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]

    cx, cy = centers[i]

    # Draw region boundary
    component = (labels == i).astype(np.uint8)

    contours, _ = cv2.findContours(
        component,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cv2.drawContours(
        result, contours, -1, (0, 0, 255), 3
    )

    cv2.putText(
        result,
        f"R{room_number}",
        (int(cx), int(cy)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 0),
        2
    )

    print(
        f"R{room_number}: Area={area}, "
        f"Position=({x},{y}), Size=({w},{h})"
    )

# Save result
output = Path("outputs")
output.mkdir(exist_ok=True)

cv2.imwrite(
    str(output / "plan1_separated_rooms.png"),
    result
)

print("\nTotal detected regions:", room_number)
print("Saved: outputs/plan1_separated_rooms.png")
