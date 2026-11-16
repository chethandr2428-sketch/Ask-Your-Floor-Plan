from pathlib import Path
import re, json, sqlite3
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = ROOT / "data" / "images"
MASK_DIR = ROOT / "data" / "masks"
OUT_DIR = ROOT / "outputs" / "part1"
OVERLAY_DIR = OUT_DIR / "overlays"
DB_PATH = ROOT / "floorplans_part1.db"

# Observed mask colours. Some semantic labels are provisional.
PALETTE = {
    "Rooms": (0, 142, 142),
    "Walls_provisional": (175, 216, 248),
    "Windows_provisional": (246, 189, 15),
    "Orange_class_unconfirmed": (255, 142, 70),
    "Room_Separations": (214, 70, 70),
    "Green_class_unconfirmed": (139, 186, 0),
}

def plan_number(path):
    m = re.match(r"(\d+)", path.stem)
    return int(m.group(1)) if m else None

def find_mask(number):
    matches = [p for p in MASK_DIR.glob("*.png") if plan_number(p) == number]
    if not matches:
        return None
    matches.sort(key=lambda p: (p.stem != f"{number} (2)", p.stem != str(number), p.name))
    return matches[0]

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OVERLAY_DIR.mkdir(parents=True, exist_ok=True)

    images = sorted(
        [p for p in IMAGE_DIR.glob("*.png") if plan_number(p) is not None],
        key=lambda p: (plan_number(p), p.name.lower())
    )
    if not images:
        raise SystemExit(f"No PNG images found in {IMAGE_DIR}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS elements;
    DROP TABLE IF EXISTS plans;
    CREATE TABLE plans(
        plan_id INTEGER PRIMARY KEY, image_file TEXT, mask_file TEXT,
        width INTEGER, height INTEGER
    );
    CREATE TABLE elements(
        element_id INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_id INTEGER, class_name TEXT, component_number INTEGER,
        pixel_area INTEGER, x INTEGER, y INTEGER, width INTEGER, height INTEGER,
        center_x REAL, center_y REAL
    );
    """)

    summary_counts = {k: 0 for k in PALETTE}
    missing_masks, plans_output = [], []
    processed = 0

    for img_path in images:
        number = plan_number(img_path)
        mask_path = find_mask(number)
        if mask_path is None:
            missing_masks.append(number)
            print(f"Skipping plan {number}: mask not found")
            continue

        image = cv2.imread(str(img_path))
        mask_bgr = cv2.imread(str(mask_path))
        if image is None or mask_bgr is None:
            print(f"Skipping plan {number}: unreadable image or mask")
            continue
        if image.shape[:2] != mask_bgr.shape[:2]:
            print(f"Skipping plan {number}: image/mask dimensions differ")
            continue

        h, w = image.shape[:2]
        cur.execute("INSERT OR REPLACE INTO plans VALUES(?,?,?,?,?)",
                    (number, img_path.name, mask_path.name, w, h))
        mask_rgb = cv2.cvtColor(mask_bgr, cv2.COLOR_BGR2RGB)
        overlay = image.copy()
        elements = []

        for class_name, rgb in PALETTE.items():
            rgb_arr = np.array(rgb, dtype=np.int16)
            colour_pixels = np.all(
                np.abs(mask_rgb.astype(np.int16) - rgb_arr) <= 5, axis=2
            )
            binary = colour_pixels.astype(np.uint8)
            n, labels, stats, centers = cv2.connectedComponentsWithStats(binary, 8)
            tint = (int(rgb[2]), int(rgb[1]), int(rgb[0]))
            overlay[colour_pixels] = (
                0.55 * overlay[colour_pixels] + 0.45 * np.array(tint)
            ).astype(np.uint8)

            component_index = 0
            minimum_area = 500 if class_name == "Rooms" else (100 if "Walls" in class_name else 8)
            for label_id in range(1, n):
                x, y, bw, bh, area = stats[label_id]
                if area < minimum_area:
                    continue
                component_index += 1
                cx, cy = centers[label_id]
                row = (number, class_name, component_index, int(area),
                       int(x), int(y), int(bw), int(bh), float(cx), float(cy))
                cur.execute("""
                    INSERT INTO elements
                    (plan_id,class_name,component_number,pixel_area,x,y,width,height,center_x,center_y)
                    VALUES(?,?,?,?,?,?,?,?,?,?)
                """, row)
                summary_counts[class_name] += 1
                elements.append({
                    "class_name": class_name,
                    "component_number": component_index,
                    "pixel_area": int(area),
                    "bounding_box_xywh": [int(x), int(y), int(bw), int(bh)],
                    "center_xy": [round(float(cx), 2), round(float(cy), 2)]
                })

        cv2.imwrite(str(OVERLAY_DIR / f"plan_{number}_all_classes.png"), overlay)
        plans_output.append({
            "plan_id": number,
            "image_file": img_path.name,
            "mask_file": mask_path.name,
            "width_pixels": w,
            "height_pixels": h,
            "area_unit": "pixels, not square metres",
            "elements": elements
        })
        processed += 1
        print(f"Processed plan {number} ({processed}/{len(images)})")

    conn.commit()
    conn.close()

    json_file = OUT_DIR / "floorplans_part1.json"
    with json_file.open("w", encoding="utf-8") as f:
        json.dump(plans_output, f, indent=2)

    summary = {
        "total_images_found": len(images),
        "plans_processed": processed,
        "missing_masks": missing_masks,
        "components_by_class": summary_counts,
        "database_file": str(DB_PATH),
        "json_file": str(json_file),
        "overlay_folder": str(OVERLAY_DIR),
        "limitations": [
            "Connected components are candidate regions, not verified individual rooms or doors.",
            "Areas are pixel counts, not real-world measurements.",
            "Only the teal Rooms and red Room_Separations labels have stronger supporting evidence; other class labels are provisional."
        ]
    }
    with (OUT_DIR / "extraction_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\nSUCCESS: processing finished")
    print(f"Plans processed: {processed} of {len(images)}")
    print(f"Database: {DB_PATH}")
    print(f"JSON: {json_file}")
    print(f"Summary: {OUT_DIR / 'extraction_summary.json'}")
    print(f"Overlays: {OVERLAY_DIR}")

if __name__ == "__main__":
    main()
