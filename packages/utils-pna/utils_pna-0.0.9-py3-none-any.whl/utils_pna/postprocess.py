import pandas as pd
from tqdm import tqdm
from utils_pna.static import StaticAPI

class Postprocessor:
    def __init__(self, gis, api_url):
        self.static_api = StaticAPI(gis, api_url)

    def __get_static_info_df(self, df):
        mmsis = df["mmsi"].apply(str).unique().tolist()
        static_info_mmsis = []

        for mmsi in tqdm(mmsis):
            try:
                # TODO: quitar este try-catch
                static_info = self.static_api.static_info_mmsi(mmsi)
                if static_info is not None:
                    static_info_mmsis.append(static_info)
            except:
                pass

        df = pd.DataFrame(static_info_mmsis)
        df["mmsi"] = df["mmsi"].apply(str)

        return df
    
    def expand_vessel_info(self, df):
        static_df = self.__get_static_info_df(df)

        return pd.merge(
            df, static_df, 
            how='left', left_on='mmsi',
            right_on='mmsi',
            left_index=False, right_index=False
        )

    def postprocess(self, df):
        return self.expand_vessel_info(df)