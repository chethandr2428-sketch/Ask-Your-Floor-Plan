
import sqlite3
import csv

# Connect to database
conn = sqlite3.connect("floorplans.db")
cursor = conn.cursor()

# Register floor plan 1
cursor.execute("""
INSERT OR IGNORE INTO plans (plan_id, image_name, mask_name)
VALUES (1, '1.png', '1 (2).png')
""")

# Avoid duplicate records if you run this again
cursor.execute("DELETE FROM regions WHERE plan_id = 1")

# Read CSV file
with open("outputs/plan_1_regions.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute("""
        INSERT INTO regions (
            plan_id, red, green, blue, area_pixels,
            x, y, width, height, center_x, center_y
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            1,
            int(row["red"]),
            int(row["green"]),
            int(row["blue"]),
            int(row["area_pixels"]),
            int(row["x"]),
            int(row["y"]),
            int(row["width"]),
            int(row["height"]),
            float(row["center_x"]),
            float(row["center_y"])
        ))

conn.commit()

# Check records
cursor.execute(
    "SELECT COUNT(*) FROM regions WHERE plan_id = 1"
)
print("Regions stored:", cursor.fetchone()[0])

conn.close()

print("DATA IMPORTED SUCCESSFULLY!")
