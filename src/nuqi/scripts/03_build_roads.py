from pathlib import Path
import geopandas as gpd

IN_GEOJSON = Path("data/interim/nouakchott_export.geojson")
OUT = Path("data/interim/roads.geoparquet")

def main():
    if not IN_GEOJSON.exists():
        raise FileNotFoundError(f"Missing {IN_GEOJSON}. Run osmium export first.")

    gdf = gpd.read_file(IN_GEOJSON)

    # Keep only line geometries (roads/ways)
    gdf = gdf[gdf.geometry.type.isin(["LineString", "MultiLineString"])].copy()
    gdf = gdf[gdf.geometry.notna() & ~gdf.geometry.is_empty].copy()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_parquet(OUT, index=False)

    print("Wrote:", OUT)
    print("Rows:", len(gdf))
    print("CRS:", gdf.crs)
    print("Columns sample:", list(gdf.columns)[:25])

if __name__ == "__main__":
    main()