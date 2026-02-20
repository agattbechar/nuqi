import geopandas as gpd

HEALTH = {"hospital", "clinic", "doctors"}
SCHOOL = {"school"}
MARKET = {"marketplace"}

def distance_to_score(d: float) -> float:
    # Same transparent bins (tune later)
    if d <= 250: return 100.0
    if d <= 500: return 80.0
    if d <= 1000: return 50.0
    if d <= 2000: return 30.0
    return 10.0

def _dist_to_union(grid_m: gpd.GeoDataFrame, pts_m: gpd.GeoDataFrame) -> list[float]:
    if len(pts_m) == 0:
        # If category missing in OSM, return NaNs-like large distance
        return [float("inf")] * len(grid_m)
    union = pts_m.geometry.unary_union
    return grid_m.geometry.centroid.distance(union).astype(float).tolist()

def compute_services(grid: gpd.GeoDataFrame, amenities: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    grid_m = grid.to_crs("EPSG:3857")
    am_m = amenities.to_crs("EPSG:3857")

    health = am_m[am_m["amenity"].isin(HEALTH)]
    school = am_m[am_m["amenity"].isin(SCHOOL)]
    market = am_m[am_m["amenity"].isin(MARKET)]

    dist_health = _dist_to_union(grid_m, health)
    dist_school = _dist_to_union(grid_m, school)
    dist_market = _dist_to_union(grid_m, market)

    out = grid.copy()
    out["dist_health_m"] = dist_health
    out["dist_school_m"] = dist_school
    out["dist_market_m"] = dist_market

    out["health_score"] = out["dist_health_m"].apply(distance_to_score)
    out["school_score"] = out["dist_school_m"].apply(distance_to_score)
    out["market_score"] = out["dist_market_m"].apply(distance_to_score)

    # Simple average (transparent). Later we can weight.
    out["services_score"] = (out["health_score"] + out["school_score"] + out["market_score"]) / 3.0
    return out
