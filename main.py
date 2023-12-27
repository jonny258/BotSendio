import json 
from gsheet import GSheet
from openseaa import Opensea
from nft import Nft
import time

def load_config():
    with open('config.json') as f:
        return json.load(f)

def main(): 
    config = load_config()
    only_verified = config["only_verified"]
    excluded_collections = config["exclude_collections_slugs"]
    token_ids = config["tokens_ids"]
    nft = Nft()
    opensea = Opensea()
    gsheet = GSheet()
    if config["ONLY_collections_provided"]:
        for collection in config["collections_slugs"]:
            try:
                collection_data = opensea.get_collection(collection)
            except:
                time.sleep(2)
                continue
            if collection_data:
                print(collection_data)
                if collection_data["address"] not in gsheet.addresses:
                    if token_ids:
                        token_id = token_ids[0]
                        print("start transfer to ", collection_data["address"])
                        res = nft.transfer_nft(token_id, collection_data["address"])
                        if res:
                            token_ids.remove(token_id)
                            gsheet.add_to_sheet(collection, collection_data["user"], collection_data["address"])
                    else:
                        break
    else:
        counter = 0
        number_of_collection = config["number_of_collections"]
        while True:
            if counter == number_of_collection:
                break 
            try:
                collections = opensea.get_collections(number_of_collection)
            except:
                time.sleep(2)
                continue
            for collection in collections:
                if collection in excluded_collections:
                    continue
                try:
                    collection_data = opensea.get_collection(collection)
                except:
                    time.sleep(2)
                    continue

                if collection_data:
                    print(collection_data)
                    if collection_data["address"] in gsheet.addresses:
                        continue
                    if only_verified and not collection_data["verified"]:
                        continue
                    if token_ids:
                        token_id = token_ids[0]
                        print("start transfer to ", collection_data["address"])
                        res = nft.transfer_nft(token_id, collection_data["address"])
                        if res:
                            print("transfered")
                            token_ids.remove(token_id)
                            gsheet.add_to_sheet(collection, collection_data["user"], collection_data["address"])
                            counter += 1
                            if counter == number_of_collection:
                                break
                    else:
                        break
                 
if __name__ == '__main__':
    main()
    
