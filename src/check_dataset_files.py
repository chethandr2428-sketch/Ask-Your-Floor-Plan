
import os

folders = ["data/images", "data/masks"]

for folder in folders:
    print("\nFOLDER:", folder)
    print("-" * 40)

    files = os.listdir(folder)

    print("Total files:", len(files))

    for file in files[:10]:
        print(file)

# Check for annotation files
print("\nCHECKING FOR ANNOTATIONS")

for root, dirs, files in os.walk("data"):
    for file in files:
        if file.lower().endswith(
            (".json", ".xml", ".txt", ".csv", ".svg")
        ):
            print(os.path.join(root, file))
