from opensea import OpenseaAPI
import json
import requests
import time

def load_config():
    with open('config.json') as f:
        return json.load(f)

class Opensea:
    def __init__(self):
        config = load_config()
        self.api = OpenseaAPI(apikey=config["opensea_api_key"])
        self.headers = {"accept": 'application/json', 'X-API-KEY': config["opensea_api_key"]}
        self.addresses = []
        self.new_rows = []
    def get_collection(self, collection_name):
        res = {}
        results = self.api.collection(collection_slug=collection_name)
        editors = results["collection"]["editors"]
        if not editors:
            return res
        editor = editors[0]
        user = ""
        verified = False
        while True:
            try:
                result = requests.get(f"https://api.opensea.io/api/v1/user/{editor}", headers=self.headers).json()
                user = result["username"]
                if user == None:
                    return res
                if result["account"]["config"] == "verified":
                    verified = True
            except:
                return res
            break
        res = {"user": user, "address": editor, "verified": verified}
        return res

        return res
    def get_collections(self, number_of_collection):
        res = []
        url  = "https://api.opensea.io/api/v1/collections?offset={}&limit=300".format(number_of_collection)
        while True:
            try:
                results = requests.get(url, headers=self.headers).json()
                for collection in results["collections"]:
                    res.append(collection["slug"])
                return res
            except:
                time.sleep(3)
                continue
            break
