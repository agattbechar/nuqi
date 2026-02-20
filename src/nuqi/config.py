from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
CACHE_DIR = DATA_DIR / "cache"

# --- Nouakchott bounding box (v1 default; we can replace with exact admin boundary later)
# Format: (min_lon, min_lat, max_lon, max_lat)
NOUAKCHOTT_BBOX = (-16.1, 18.0, -15.8, 18.25)

# Grid resolution in meters (250m is a great start)
GRID_SIZE_M = 250

# OSM roads we treat as “major”
MAJOR_HIGHWAYS = {"motorway", "trunk", "primary", "secondary"}