# Ask Your Floor Plan – AI Assistant for Buildings

## Project Overview
This project develops a floor-plan analysis system that processes floor-plan images and segmentation masks to identify building regions and store extracted information in a structured database.

The goal is to help users ask questions about building layouts using data-driven queries.

## Technologies Used
- Python
- OpenCV
- NumPy
- SQLite
- JSON
- Pandas
- Git and GitHub

## Dataset
The project uses a floor-plan image dataset containing 121 original floor plans and their corresponding segmentation masks.

## Project Results
- 121 floor plans processed.
- 5,184 candidate elements extracted.
- SQLite database created.
- JSON data extraction.
- Colour-based segmentation analysis.
- Visual overlays generated for floor-plan inspection.

## Project Structure
- `data/` – Dataset images and masks (not included in this repository).
- `src/` – Python source code.
- `outputs/` – Extracted data and visualization results.
- `floorplans_part1.db` – SQLite database.
- `requirements.txt` – Python dependencies.

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the extraction pipeline:

```bash
python src/finish_part1.py
```

## Current Limitations
- Extracted connected components are candidate regions and are not guaranteed to represent individual rooms.
- Room names such as Bedroom, Kitchen and Bathroom have not yet been verified.
- Some segmentation colour-to-class mappings are provisional.
- Area measurements are in pixels, not square metres.
- The LLM-based question-answering feature requires further development.

## Future Improvements
- Improve room and door detection.
- Add reliable room-name identification.
- Develop an LLM-based question-answering assistant.
- Improve extraction accuracy and evaluate results.

## Author
Chethan D R

Electronics and Communication Engineering
