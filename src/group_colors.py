
from PIL import Image
from collections import Counter
from pathlib import Path

img = Image.open("data/masks/1 (2).png").convert("RGB")

colors = Counter(img.getdata())

# Main colours identified in the mask
main_colors = [
    (0, 142, 142),
    (175, 216, 248),
    (246, 189, 15),
    (255, 142, 70),
    (214, 70, 70),
    (139, 186, 0)
]

group_counts = {color: 0 for color in main_colors}

for color, count in colors.items():

    if color == (0, 0, 0):
        continue

    nearest = min(
        main_colors,
        key=lambda c: sum(
            (color[i] - c[i]) ** 2
            for i in range(3)
        )
    )

    distance = sum(
        (color[i] - nearest[i]) ** 2
        for i in range(3)
    ) ** 0.5

    if distance <= 5:
        group_counts[nearest] += count

print("GROUPED COLOUR ANALYSIS")
print("-" * 40)

for color, count in group_counts.items():
    print("RGB:", color, "| Pixels:", count)

print("\nCOLOUR GROUPING COMPLETED")
