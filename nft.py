import web3
from web3 import Web3
from web3._utils.events import get_event_data
import requests
import json
from bs4 import BeautifulSoup as bs

def load_config():
    with open('config.json') as f:
        return json.load(f)

def abi_ftm(contract):
    soup = bs(requests.get(f'https://api.polygonscan.com/api?module=contract&action=getabi&address={contract}&format=raw').content, 'html.parser')
    print(soup)
    return str(soup)

class Nft:
    def __init__(self):
        config = load_config()
        self.contract_addr = config["nft_contract_address"]
        infura_url = config["infura_url"]
        self.abi = abi_ftm(self.contract_addr)
        print(self.abi)
        self.w3 = Web3(Web3.HTTPProvider(infura_url))
        self.account = self.w3.eth.account.from_key(config["private_key"])
        self.contract = self.w3.eth.contract(self.contract_addr, abi=self.abi)

    def transfer_nft(self, token_id, address):
        if True:
            address = Web3.toChecksumAddress(address)
            gas_price = self.w3.eth.gas_price
            print("gas price: ", gas_price)
            nonce = self.w3.eth.getTransactionCount(self.account.address)
            data = str.encode("0x01")
            amount = 1
            calldata = self.contract.encodeABI(fn_name="safeTransferFrom", args=[self.account.address, address ,token_id, amount, data])
            tx = {
                'from': self.account.address,
                'to': self.contract.address,
                'nonce':  nonce,
                'value': 0,
                'data': calldata,
                'gasPrice': gas_price,
                'chainId': 137
            }
            # tx = self.contract.functions.safeTransferFrom(self.account.address, address, token_id).build_transaction({
            #     'gasPrice': gas_price,
            #     'nonce': nonce,
            # })
            gas = self.w3.eth.estimate_gas(tx)
            tx['gas'] = gas
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.account.key)
            print("signed tx: ", signed_tx)
            print("sending tx...")
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print("waiting for tx to be mined...")
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(tx_receipt)
            return True
        # except Exception as e:
        #     print(e)
        #     return False    
