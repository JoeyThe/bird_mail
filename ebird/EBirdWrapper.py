"""
All data collected with this wrapper for the eBird API is attributed to  eBird.org (https://ebird.org/home).
"""
import typing as t

import requests


class EBirdWrapper:
    def __init__(self, token):
        self.token = token
        self.headers = {}
        self.headers["X-eBirdApiToken"] = self.token

    def get_species_info_for_region(
        self,
        region_code: str,
        species_code: str,
        back: int = 30,
        max_results: int = 10000,
        debug: bool = False,
    ) -> list[t.Any]:
        params = {"back": back, "maxResults": max_results}
        headers = {"X-eBirdApiToken": self.token}
        url = f"https://api.ebird.org/v2/data/obs/{region_code}/recent/{species_code}"
        if debug:
            headers["X-eBirdApiToken"] = "*********"
            print(f"URL: {url}\n" + f"Parameters: {params}\n" + f"Headers: {headers}")
            return None
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        if len(data) == 0:
            data = []
        return data

    def get_region_info(self, region_code: str) -> dict[str, t.Any]:
        url = f"https://api.ebird.org/v2/ref/region/list/subnational2/{region_code}"
        r = requests.get(url, headers=self.headers)
        data = r.json()
        return data

    def get_ebird_taxonomy(self) -> str:
        url = "https://api.ebird.org/v2/ref/taxonomy/ebird"
        r = requests.get(url, headers=self.headers)
        return r.text
