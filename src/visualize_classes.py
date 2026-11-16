
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

image = np.array(
    Image.open("data/images/1.png").convert("RGB")
)

mask = np.array(
    Image.open("data/masks/1 (2).png").convert("RGB")
)

fig, axes = plt.subplots(1, 2, figsize=(14, 7))

axes[0].imshow(image)
axes[0].set_title("Original Floor Plan 1")
axes[0].axis("off")

axes[1].imshow(mask)
axes[1].set_title("Segmentation Mask 1")
axes[1].axis("off")

plt.tight_layout()

plt.savefig(
    "outputs/plan1_comparison.png",
    dpi=150
)

plt.show()

print("Floor plan comparison saved!")
