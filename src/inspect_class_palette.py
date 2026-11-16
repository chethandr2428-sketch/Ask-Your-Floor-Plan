
from PIL import Image
from collections import Counter
from pathlib import Path

mask_path = "data/masks/1 (2).png"

img = Image.open(mask_path).convert("RGB")

colors = Counter(img.getdata())

# Known colours from CVC-FP documentation
known_classes = {
    (0, 142, 142): "Room",
    (214, 70, 70): "Room Separation"
}

print("=" * 50)
print("FLOOR PLAN CLASS INSPECTION")
print("=" * 50)

for color, count in colors.most_common(20):

    class_name = known_classes.get(
        color, "Unconfirmed class"
    )

    print(
        "RGB:", color,
        "| Class:", class_name,
        "| Pixels:", count
    )

# Save a class palette report
output = Path("outputs")
output.mkdir(exist_ok=True)

with open(output / "class_palette.txt", "w") as f:
    for color, count in colors.most_common(30):
        name = known_classes.get(
            color, "Unconfirmed"
        )
        f.write(
            f"RGB: {color} | {name} | Pixels: {count}\n"
        )

print("\nClass report saved successfully!")
