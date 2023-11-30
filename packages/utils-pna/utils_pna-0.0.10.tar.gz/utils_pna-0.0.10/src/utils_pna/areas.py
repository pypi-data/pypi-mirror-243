import pandas as pd
from shapely.geometry import Polygon
from geopandas import GeoDataFrame, sjoin

class AreaFinder:
    def __init__(self, gis, id_layer):
        self.gis = gis
        self.areas_gdf = self.__get_areas_geodataframe(id_layer)

    def __get_areas_geodataframe(self, id_layer):
        layer_areas = self.gis.content.get(id_layer).layers[0]
        areas = layer_areas.query().sdf
        areas['geom'] = areas.SHAPE.apply(lambda r: Polygon(r["rings"][0]))
        areas_gdf = GeoDataFrame(areas.drop("SHAPE", axis=1).rename(columns={"geom": "geometry"}))

        return areas_gdf[["fna", "geometry"]].rename(columns={"fna": "area_name"})

    def find_areas(self, gdf, join_type="inner"):
        gdf_areas = sjoin(gdf, self.areas_gdf, how=join_type, op='within')

        return gdf_areas.drop("index_right", axis=1)