
import sqlite3

# Create database
connection = sqlite3.connect("floorplans.db")

cursor = connection.cursor()

# Create Plans table
cursor.execute("""
CREATE TABLE IF NOT EXISTS plans (
    plan_id INTEGER PRIMARY KEY,
    image_name TEXT,
    mask_name TEXT
)
""")

# Create Regions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS regions (
    region_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER,
    red INTEGER,
    green INTEGER,
    blue INTEGER,
    area_pixels INTEGER,
    x INTEGER,
    y INTEGER,
    width INTEGER,
    height INTEGER,
    center_x REAL,
    center_y REAL,
    FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
)
""")

connection.commit()
connection.close()

print("DATABASE CREATED SUCCESSFULLY!")
print("Database: floorplans.db")
print("Tables: plans, regions")
