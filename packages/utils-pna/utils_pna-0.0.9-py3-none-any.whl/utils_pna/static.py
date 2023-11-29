import requests

class StaticAPI:
    def __init__(self, gis, api):
        self.gis = gis
        self.token = gis._con.token
        self.api = api
    
    def api_static_request(self, mmsi):
        url = f'{self.api}/elements/search?f=json&token={self.token}'

        headers = {'Content-Type': 'application/json'}
        data = {
            "criteria": {
                "MMSI": mmsi,
                "elementType": "buque"
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            r = response.json()
            return r
        return None

    def find_key_with_text(self, d, text):
        for key, value in d.items():
            if text == key:
                return value
            elif isinstance(value, dict):
                result = self.find_key_with_text(value, text)
                if result is not None:
                    return result
        return None

    def find_key_in_results(self, results, key):
        for result in results:
            value = self.find_key_with_text(result, key)
            if (value is not None) and (value is not '') and (value is not ' '):
                return value

        return 'DESCONOCIDO'

    def find_name(self, results, key):
        vessel_name = self.find_key_in_results(results, key)
        return vessel_name if (vessel_name is not None) and (vessel_name != '') and (vessel_name != ' ') else 'DESCONOCIDO'

    def static_info_mmsi(self, mmsi):
        r = self.api_static_request(mmsi)
        if r is not None:
            return {
                "mmsi": mmsi,
                "element_id": r[0]["elementId"],
                "vessel_name": self.find_name(r, "VesselName"),
                "imo": self.find_key_in_results(r, "IMO"),
                "true_mmsi": self.find_key_in_results(r, "TrueMMSI"),
                "flag_code": self.find_key_in_results(r, "VesselFlag_iso"),
                "flag_name": self.find_key_in_results(r, "VesselFlag_es"),
                "vessel_type": self.find_key_in_results(r, "VesselType"),
            }
        else:
            return None