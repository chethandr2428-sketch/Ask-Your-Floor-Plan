
import pandas as pd
from pathlib import Path

# Load extracted room measurements
input_file = "outputs/room_area_report.csv"

df = pd.read_csv(input_file)

# Add room classification column
df["room_type"] = "Unknown"

# Save classification dataset
output_file = "outputs/room_classification_dataset.csv"

df.to_csv(output_file, index=False)

print("ROOM CLASSIFICATION DATASET CREATED")
print("-----------------------------------")
print("Total regions:", len(df))
print("\nDataset preview:")
print(df.head())

print("\nSaved:", output_file)
