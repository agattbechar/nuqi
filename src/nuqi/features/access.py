import geopandas as gpd
from nuqi.config import MAJOR_HIGHWAYS

def distance_to_score(d: float) -> float:
    if d <= 250: return 100.0
    if d <= 500: return 80.0
    if d <= 1000: return 50.0
    if d <= 2000: return 30.0
    return 10.0

def compute_access(grid: gpd.GeoDataFrame, roads: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Access = distance from each grid cell centroid to the nearest 'major' road.
    Output columns:
      - dist_major_road_m
      - access_score
    """
    if "highway" in roads.columns:
        major = roads[roads["highway"].isin(MAJOR_HIGHWAYS)].copy()
        if major.empty:
            major = roads.copy()
    else:
        major = roads.copy()

    grid_m = grid.to_crs("EPSG:3857")
    major_m = major.to_crs("EPSG:3857")

    centroids = grid_m.geometry.centroid
    major_union = major_m.geometry.unary_union

    dist_m = centroids.distance(major_union)

    out = grid.copy()
    out["dist_major_road_m"] = dist_m.astype(float)
    out["access_score"] = out["dist_major_road_m"].apply(distance_to_score)
    return out