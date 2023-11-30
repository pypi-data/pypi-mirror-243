import requests
import time
from tqdm import tqdm
from datetime import datetime, timedelta
from geopandas import GeoDataFrame, GeoSeries
from shapely.geometry import Point
from utils_pna.dates import get_dates_in_intervals, to_tmsp

def get_lims_aoi(aoi):
    if (aoi is not None) and isinstance(aoi, list):
        down_left, top_right = aoi[0], aoi[1]
    elif (aoi is None) or (aoi.lower() == "areas pna"):
        down_left = [-63.67, -48.71]
        top_right = [-49.87, -37.74]
    elif aoi.lower() == "mar argentino":
        down_left = [-72.251941, -57.833594]
        top_right = [-50.806628, -35.658120]
    elif aoi.lower() == "amp":
        down_left = [-69.07, -58.87]
        top_right = [-55.01, -53.39]

    return [(down_left[0], '>'), (top_right[0], '<')], [(down_left[1], '>'), (top_right[1], '<')]

def format_value(value):
    """ Formatea el valor con o sin comillas dependiendo de su tipo. """
    if isinstance(value, str):
        return f"'{value}'"
    return str(value)

def parse_dates(dates):
    if dates is None:
        end_date = datetime.now()
        start_date = end_date - timedelta(minutes=5)
    else:
        start_date, end_date = dates[0], dates[1]

    return [(str(to_tmsp(start_date)), '> TIMESTAMP'), (str(to_tmsp(end_date)), '< TIMESTAMP')]

def parse_query(dates=None, aoi=None, custom_query=None, **args):
    args["Longitude"], args["Latitude"] = get_lims_aoi(aoi)
    
    args["msgTime"] = parse_dates(dates)

    l = []
    if custom_query is not None:
        l.append(custom_query)

    for k, v in args.items():
        if isinstance(v, list):  # Si es una lista, procesa cada condición en la lista
            conditions = []
            for condition in v:
                if isinstance(condition, tuple):
                    value, comparator = condition
                    conditions.append(f"{k} {comparator} {format_value(value)}")
                else:
                    conditions.append(f"{k}={format_value(condition)}")
            l.append(f"({' AND '.join(conditions)})")
        elif isinstance(v, tuple):  # Para una única condición en forma de tupla
            value, comparator = v
            l.append(f"{k} {comparator} {format_value(value)}")
        else:  # Para una condición simple de igualdad
            l.append(f"{k}={format_value(v)}")

    return ' AND '.join(l)

def data_list_to_gdf(data_list):    
    attributes_list = []
    geometry_list = []
    
    for data in data_list:
        try:
            attributes = data.get('attributes', {})
            geometry = data.get('geometry', {})
            lon = geometry.get('x')
            lat = geometry.get('y')
            point = Point(lon, lat)
            attributes_list.append(attributes)
            geometry_list.append(point)
        except:
            pass
    
    gdf = GeoDataFrame(attributes_list, geometry=GeoSeries(geometry_list))
    return gdf

def parse_positions(data_list):
    gdf = data_list_to_gdf(data_list)
    gdf = gdf.sort_values(by="msgTime")
    gdf.columns = [c.lower() for c in gdf.columns]

    return gdf

class QueryAPI:
    def __init__(self, gis, api):
        self.gis = gis
        self.token = gis._con.token
        self.api = api

    def __api_get_request(self, query_str):
        api_url = self.api
        api_url += f"/query?f=json&token={self.token}&where={query_str}&outFields=*"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                return response.json()
            else:
                raise ValueError(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            return f"Exception occurred: {e}"
        
    def __query_with_retries(self, query_str, max_retries=5, time_wait=1):
        result = None
        retries = 0
        
        while result is None and retries < max_retries:
            try:
                try_result = self.__api_get_request(query_str)
                try_result["features"]
                result = try_result
            except Exception as e:
                print(e)
                time.sleep(time_wait)
                retries += 1

        return result
        
    def __query_api(self, unpack, **args):
        query_str = parse_query(**args)

        results_query = self.__query_with_retries(query_str)
        if unpack:
            return results_query["features"]
        else:
            return results_query
        
    def query(self, step_dates=5, dates=None, unpack=True, **args):
        if dates is None:
            end_date = datetime.now()
            start_date = end_date - timedelta(minutes=step_dates)
        elif not isinstance(dates, list):
            start_date = dates
            end_date = datetime.now()
        else:
            start_date, end_date = dates[0], dates[1]

        dates_intervals = get_dates_in_intervals(start_date, end_date, interval_minutes=step_dates)

        results_query = []
        for i in tqdm(range(len(dates_intervals)-1)):
            r = self.__query_api(unpack, dates=[dates_intervals[i], dates_intervals[i+1]], **args)
            results_query.extend(r)

        return results_query