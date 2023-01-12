import requests
import json


class MongoAPI:
    def __init__(self, collection_name, database_name, api_key):
        self.url = "https://data.mongodb-api.com/app/data-alcsg/endpoint/data/v1/action/find"
        self.collection_name = collection_name
        self.database_name = database_name
        self.api_key = api_key
        
    def _make_request(self, payload):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Request-Headers': '*',
            'api-key': self.api_key,
        }
        try:
            response = requests.request("POST", self.url, headers=headers, data=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'A request exception occurred: {e}')
            raise           

        
    def last_four_docs(self):
        payload = json.dumps({
            "collection": self.collection_name,
            "database": self.database_name,
            "dataSource": "Cluster0",
            "projection": {},
            "filter": {},
            "sort": {"timestamp": -1},
            "limit": 4
        })
        try:
            response = self._make_request(payload)
            return response["documents"]
        except Exception as e:
            print(f'An error occurred: {e}')
            return None
    

        
    def last_one_doc(self):
        payload = json.dumps({
            "collection": self.collection_name,
            "database": self.database_name,
            "dataSource": "Cluster0",
            "projection": {},
            "filter": {},
            "sort": {"timestamp": -1},
            "limit": 1
        })
        try:
            response = self._make_request(payload)
            return response["documents"]
        except Exception as e:
            print(f'An error occurred: {e}')
            return None

    def all_docs(self):
        payload = json.dumps({
            "collection": self.collection_name,
            "database": self.database_name,
            "dataSource": "Cluster0",
            "projection": {},
            "filter": {},
            "sort": {"timestamp": 1}            
        })
        try:
            response = self._make_request(payload)
            return response["documents"]
        except Exception as e:
            print(f'An error occurred: {e}')
            return None




# api_key = "wFjkxYNfwGybC7gsuz6rZ91tDNlg32aIkcJsTscPQKyR8iF7jcxfBEdBrTzM8ibA"
# api = MongoAPI("all_data", "zero", api_key)
# print(api.last_four_docs())
# print(api.last_one_doc())
