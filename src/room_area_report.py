
import cv2
import csv
import os

# Load segmentation mask
mask = cv2.imread("data/masks/1 (2).png")

if mask is None:
    print("ERROR: Mask image not found!")
    exit()

# Identify room colour
room_color = (142, 142, 0)  # BGR format

# Create binary mask
binary = cv2.inRange(
    mask,
    room_color,
    room_color
)

# Detect room regions
count, labels, stats, centers = cv2.connectedComponentsWithStats(
    binary, 8
)

# Create report
os.makedirs("outputs", exist_ok=True)

with open("outputs/room_area_report.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Room_ID",
        "Area_Pixels",
        "X",
        "Y",
        "Width",
        "Height",
        "Center_X",
        "Center_Y"
    ])

    room_number = 0

    for i in range(1, count):
        area = stats[i, cv2.CC_STAT_AREA]

        if area > 5000:
            room_number += 1

            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            width = stats[i, cv2.CC_STAT_WIDTH]
            height = stats[i, cv2.CC_STAT_HEIGHT]

            center_x, center_y = centers[i]

            writer.writerow([
                f"R{room_number}",
                area,
                x,
                y,
                width,
                height,
                round(center_x, 2),
                round(center_y, 2)
            ])

print("ROOM AREA REPORT GENERATED!")
print("Saved: outputs/room_area_report.csv")
