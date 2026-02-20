import geopandas as gpd
from nuqi.config import NOUAKCHOTT_BBOX, GRID_SIZE_M, PROCESSED_DIR
from nuqi.geo.grid import bbox_grid_wgs84
from nuqi.features.access import compute_access

def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    roads = gpd.read_parquet("data/interim/roads.geoparquet")
    grid = bbox_grid_wgs84(NOUAKCHOTT_BBOX, GRID_SIZE_M)
    scored = compute_access(grid, roads)

    out = PROCESSED_DIR / "grid_access.geoparquet"
    scored.to_parquet(out, index=False)

    print("Wrote:", out)
    print("Cells:", len(scored))
    print(scored[["dist_major_road_m", "access_score"]].describe())

if __name__ == "__main__":
    main()