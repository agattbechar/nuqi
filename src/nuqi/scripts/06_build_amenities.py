from pathlib import Path
import geopandas as gpd

IN_GEOJSON = Path("data/interim/amenities_export.geojson")
OUT = Path("data/interim/amenities.geoparquet")

KEEP = {"hospital", "clinic", "doctors", "school", "marketplace"}

def main():
    if not IN_GEOJSON.exists():
        raise FileNotFoundError(f"Missing {IN_GEOJSON}. Run osmium export first.")

    gdf = gpd.read_file(IN_GEOJSON)

    # Keep only points (nodes become points; some ways/relations might be polygons/lines)
    gdf = gdf[gdf.geometry.type == "Point"].copy()

    # Keep only target amenities
    if "amenity" in gdf.columns:
        gdf = gdf[gdf["amenity"].isin(KEEP)].copy()
    else:
        raise RuntimeError("No 'amenity' column found. Unexpected export structure.")

    # Keep it tidy
    cols = [c for c in ["amenity", "name", "operator", "addr:city", "addr:street"] if c in gdf.columns]
    gdf = gdf[cols + ["geometry"]].copy()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_parquet(OUT, index=False)

    print("Wrote:", OUT)
    print("Rows:", len(gdf))
    print(gdf["amenity"].value_counts())

if __name__ == "__main__":
    main()