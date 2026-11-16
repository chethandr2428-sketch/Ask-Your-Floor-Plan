
import sqlite3

conn = sqlite3.connect("floorplans.db")
cursor = conn.cursor()

print("DATABASE VERIFICATION")
print("-" * 35)

cursor.execute("SELECT * FROM plans")
print("\nPlans:")
for row in cursor.fetchall():
    print(row)

cursor.execute("""
SELECT plan_id, COUNT(*)
FROM regions
GROUP BY plan_id
""")

print("\nRegions per plan:")
for row in cursor.fetchall():
    print(row)

cursor.execute("""
SELECT name FROM sqlite_master
WHERE type='table'
""")

print("\nDatabase tables:")
print(cursor.fetchall())

conn.close()
