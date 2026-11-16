
import cv2
import numpy as np
from pathlib import Path

image_path = Path("data/images/1.png")
mask_path = Path("data/masks/1 (2).png")

output_folder = Path("outputs/class_inspection")
output_folder.mkdir(parents=True, exist_ok=True)

image = cv2.imread(str(image_path))
mask = cv2.imread(str(mask_path))

if image is None or mask is None:
    raise FileNotFoundError("Could not load Plan 1 image or mask.")

if image.shape[:2] != mask.shape[:2]:
    mask = cv2.resize(
        mask,
        (image.shape[1], image.shape[0]),
        interpolation=cv2.INTER_NEAREST
    )

# Main RGB colours found in the mask
colors = {
    "teal": (0, 142, 142),
    "light_blue": (175, 216, 248),
    "yellow": (246, 189, 15),
    "orange": (255, 142, 70),
    "red": (214, 70, 70),
    "green": (139, 186, 0)
}

for name, rgb in colors.items():

    bgr = np.array(rgb[::-1], dtype=np.int16)

    difference = np.abs(
        mask.astype(np.int16) - bgr
    )

    selected = np.all(difference <= 5, axis=2)

    overlay = image.copy()
    overlay[selected] = (
        0.4 * image[selected] + 0.6 * bgr
    ).astype(np.uint8)

    output_path = output_folder / f"{name}.png"
    cv2.imwrite(str(output_path), overlay)

    print(name, "pixels:", int(np.count_nonzero(selected)))

print("COLOUR OVERLAYS CREATED")
print("Saved in:", output_folder)
