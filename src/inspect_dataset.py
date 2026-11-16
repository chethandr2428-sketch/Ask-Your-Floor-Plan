
import os
from pathlib import Path
from PIL import Image
from collections import Counter

# Dataset folders
images_path = Path("data/images")
masks_path = Path("data/masks")

# Get all PNG files
images = list(images_path.glob("*.png"))
masks = list(masks_path.glob("*.png"))

print("=" * 45)
print("ASHIAN FLOOR PLAN DATASET REPORT")
print("=" * 45)

print("Total original images:", len(images))
print("Total segmentation masks:", len(masks))

# Match files using their starting number

def get_number(filename):
    return Path(filename).stem.split()[0]

image_numbers = {get_number(f.name) for f in images}
mask_numbers = {get_number(f.name) for f in masks}

matched = image_numbers & mask_numbers

print("Matched floor plans:", len(matched))
print("Images without masks:", len(image_numbers - mask_numbers))
print("Masks without images:", len(mask_numbers - image_numbers))

# Inspect first 3 images
print("\nFIRST 3 FLOOR PLANS")

for file in sorted(images)[:3]:
    with Image.open(file) as img:
        print(file.name, "Size:", img.size, "Mode:", img.mode)

# Inspect first 3 masks
print("\nFIRST 3 SEGMENTATION MASKS")

for file in sorted(masks)[:3]:
    with Image.open(file) as img:
        colors = Counter(img.convert("RGB").getdata())

        print("\nFile:", file.name)
        print("Size:", img.size)
        print("Most common colors:", colors.most_common(10))

print("\nDATASET INSPECTION COMPLETED")
