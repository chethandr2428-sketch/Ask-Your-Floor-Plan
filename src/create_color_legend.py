
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt

mask = Image.open("data/masks/1 (2).png").convert("RGB")

colors = Counter(mask.getdata())

# Ignore background and select major colours
major_colors = [
    (color, count)
    for color, count in colors.most_common(30)
    if color != (0, 0, 0) and count > 100
]

fig, ax = plt.subplots(figsize=(10, 7))

for i, (color, count) in enumerate(major_colors):
    y = len(major_colors) - i - 1

    ax.barh(
        y, 1,
        color=[value / 255 for value in color],
        edgecolor="black"
    )

    ax.text(
        1.05, y,
        f"RGB {color} | Pixels: {count}",
        va="center",
        fontsize=9
    )

ax.set_yticks([])
ax.set_xlim(0, 4)
ax.set_title("Floor Plan Segmentation Colour Legend")
ax.axis("off")

plt.tight_layout()
plt.savefig("outputs/color_legend.png", dpi=150)
plt.show()

print("Colour legend saved successfully!")
