
from pathlib import Path
from PIL import Image
import re

images_path = Path("data/images")
masks_path = Path("data/masks")

def get_id(filename):
    match = re.match(r"(\d+)", filename)
    return match.group(1) if match else None

images = {
    get_id(f.name): f
    for f in images_path.glob("*.png")
    if get_id(f.name)
}

masks = {
    get_id(f.name): f
    for f in masks_path.glob("*.png")
    if get_id(f.name)
}

common_ids = sorted(
    set(images) & set(masks),
    key=int
)

print("=" * 40)
print("FLOOR PLAN IMAGE-MASK MATCHING")
print("=" * 40)

print("Original images:", len(images))
print("Segmentation masks:", len(masks))
print("Matched pairs:", len(common_ids))
print("Images without masks:", len(set(images) - set(masks)))
print("Masks without images:", len(set(masks) - set(images)))

print("\nFIRST 5 MATCHED PAIRS")

for plan_id in common_ids[:5]:
    image_file = images[plan_id]
    mask_file = masks[plan_id]

    with Image.open(image_file) as img:
        image_size = img.size

    with Image.open(mask_file) as mask:
        mask_size = mask.size

    print("\nPlan:", plan_id)
    print("Original:", image_file.name, image_size)
    print("Mask:", mask_file.name, mask_size)
    print("Same dimensions:", image_size == mask_size)

print("\nPAIR CHECK COMPLETED")
