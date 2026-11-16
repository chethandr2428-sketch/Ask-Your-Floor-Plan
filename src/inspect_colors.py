
from PIL import Image
from collections import Counter

mask_path = "data/masks/1 (2).png"

img = Image.open(mask_path).convert("RGB")

colors = Counter(img.getdata())

print("MASK COLOUR ANALYSIS")
print("--------------------")
print("Image size:", img.size)
print("Number of unique colours:", len(colors))

for color, count in colors.most_common(20):
    print("RGB:", color, "| Pixels:", count)

# Save a smaller copy for viewing
img.thumbnail((1000, 1000))
img.save("outputs/sample_mask.png")

print("\nMask saved in outputs/sample_mask.png")
