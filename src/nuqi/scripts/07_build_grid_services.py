import geopandas as gpd
from nuqi.config import NOUAKCHOTT_BBOX, GRID_SIZE_M, PROCESSED_DIR
from nuqi.geo.grid import bbox_grid_wgs84
from nuqi.features.services import compute_services

def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    grid = bbox_grid_wgs84(NOUAKCHOTT_BBOX, GRID_SIZE_M)
    amenities = gpd.read_parquet("data/interim/amenities.geoparquet")

    scored = compute_services(grid, amenities)
    out = PROCESSED_DIR / "grid_services.geoparquet"
    scored.to_parquet(out, index=False)

    print("Wrote:", out)
    print(scored[["services_score", "health_score", "school_score", "market_score"]].describe())

if __name__ == "__main__":
    main()