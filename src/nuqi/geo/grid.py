import math
import geopandas as gpd
from shapely.geometry import Polygon
from pyproj import Transformer

def bbox_grid_wgs84(bbox: tuple[float, float, float, float], cell_m: int) -> gpd.GeoDataFrame:
    min_lon, min_lat, max_lon, max_lat = bbox

    to_m = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    to_ll = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

    min_x, min_y = to_m.transform(min_lon, min_lat)
    max_x, max_y = to_m.transform(max_lon, max_lat)

    cols = math.ceil((max_x - min_x) / cell_m)
    rows = math.ceil((max_y - min_y) / cell_m)

    polys = []
    for r in range(rows):
        for c in range(cols):
            x0 = min_x + c * cell_m
            y0 = min_y + r * cell_m
            x1 = x0 + cell_m
            y1 = y0 + cell_m

            ll0 = to_ll.transform(x0, y0)
            ll1 = to_ll.transform(x1, y0)
            ll2 = to_ll.transform(x1, y1)
            ll3 = to_ll.transform(x0, y1)

            polys.append(Polygon([ll0, ll1, ll2, ll3, ll0]))

    return gpd.GeoDataFrame({"cell_id": range(len(polys))}, geometry=polys, crs="EPSG:4326")