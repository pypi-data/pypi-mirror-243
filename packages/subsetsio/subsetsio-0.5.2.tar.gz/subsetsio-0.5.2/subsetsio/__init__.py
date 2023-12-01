import requests
import pandas as pd

class Client:
    def __init__(self, api_key: str, base_url: str = 'https://server.subsets.io'):
        self.api_key: str = api_key
        self.base_url: str = base_url

    def search_tables(self, query: str, k: int = 5):
        response = requests.get(
            f"{self.base_url}/deep_search",
            params={'query': query, 'k': k, 'api_key': self.api_key}
        )
        response.raise_for_status()
        return response.json() 

    def text2sql(self, query: str, table_summaries):
        response = requests.post(
            f"{self.base_url}/text2sql",
            json={'query': query, 'table_summaries': table_summaries, 'api_key': self.api_key}
        )
        response.raise_for_status()
        return response.json()
    
    def query(self, sql_query: str) -> pd.DataFrame:
        data = {'query': sql_query, 'api_key': self.api_key}
        response = requests.post(
            f"{self.base_url}/execute",
            json=data
        )
        response.raise_for_status()
        results = response.json()
        return pd.DataFrame(results)