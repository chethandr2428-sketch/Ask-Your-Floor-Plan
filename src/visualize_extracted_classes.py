
import cv2
from pathlib import Path

original = cv2.imread("data/images/1.png")
folder = Path("outputs/class_extraction")
output = Path("outputs/class_comparison")
output.mkdir(exist_ok=True)

for file in folder.glob("*.png"):

    mask = cv2.imread(str(file), cv2.IMREAD_GRAYSCALE)

    if mask is None:
        continue

    mask = cv2.resize(
        mask,
        (original.shape[1], original.shape[0]),
        interpolation=cv2.INTER_NEAREST
    )

    overlay = original.copy()
    overlay[mask > 0] = (0, 255, 0)

    cv2.imwrite(
        str(output / f"{file.stem}_overlay.png"),
        overlay
    )

print("VISUAL COMPARISONS CREATED")
print("Saved in:", output)
