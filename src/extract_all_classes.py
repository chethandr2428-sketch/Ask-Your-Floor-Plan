
import cv2
import numpy as np
import pandas as pd
from pathlib import Path

# Input files
mask_path = Path("data/masks/1 (2).png")
output_folder = Path("outputs/class_extraction")
output_folder.mkdir(parents=True, exist_ok=True)

mask = cv2.imread(str(mask_path))

if mask is None:
    raise FileNotFoundError("Mask image not found!")

# RGB colours and provisional class names
classes = {
    "Rooms": (0, 142, 142),
    "Walls": (175, 216, 248),
    "Windows": (246, 189, 15),
    "Parking_Doors": (255, 142, 70),
    "Room_Separations": (214, 70, 70),
    "Doors": (139, 186, 0)
}

tolerance = 5
results = []

for class_name, rgb in classes.items():

    # Convert RGB to BGR
    color_bgr = np.array(rgb[::-1], dtype=np.int16)

    difference = np.abs(
        mask.astype(np.int16) - color_bgr
    )

    binary = np.all(
        difference <= tolerance,
        axis=2
    ).astype(np.uint8)

    pixel_count = int(np.count_nonzero(binary))

    # Save individual binary mask
    output_path = output_folder / f"{class_name}.png"
    cv2.imwrite(str(output_path), binary * 255)

    results.append({
        "Class": class_name,
        "Pixel_Count": pixel_count,
        "Mask_File": str(output_path)
    })

df = pd.DataFrame(results)

df.to_csv(
    output_folder / "class_summary.csv",
    index=False
)

print("CLASS EXTRACTION COMPLETED")
print("--------------------------")
print(df.to_string(index=False))
print("\nSaved in:", output_folder)
