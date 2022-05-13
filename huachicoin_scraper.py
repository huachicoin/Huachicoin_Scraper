import requests
import bs4
import re
import json
import os
from currency_converter import CurrencyConverter

# Global Variables
JSON_FILE = './huachicoin_data.json'

BSCSCAN_API_KEY = os.environ['BSCSCAN_API_KEY']

URL_PANCAKE_SWAP_BNB = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c&address=0xd074f75a329e348629e13ea05bf379b299f7714e&tag=latest&apikey={}".format(BSCSCAN_API_KEY)
URL_PANCAKE_SWAP_HCN = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0863d3605f2b16183b500e3b5fe205b46739e3e6&address=0xd074f75a329e348629e13ea05bf379b299f7714e&tag=latest&apikey={}".format(BSCSCAN_API_KEY)
URL_PRICE_BNB = "https://api.bscscan.com/api?module=stats&action=bnbprice&apikey={}".format(BSCSCAN_API_KEY)


def write_file(file, data):
    """writes the log file.
    Parameters
    ----------
    file : str
        The file to write down.
    data : str
        The data to log.
    """

    with open(file, 'w', encoding='utf-8') as fw:
        fw.write(json.dumps(data, indent=4))


if __name__ == '__main__':

    #JSON a Diccionario
    try:
        bnb_pancake = requests.get(URL_PANCAKE_SWAP_BNB).json()["result"]
        hcn_pancake = requests.get(URL_PANCAKE_SWAP_HCN).json()["result"]
        usd_price_BNB = requests.get(URL_PRICE_BNB).json()["result"]
    except Exception as e:
        print(str(e))
        exit(0)

    #Liquidez BNB
    bnb_pancake = int(bnb_pancake)/10**18
    
    #HCN Encerrado
    hcn_pancake = int(hcn_pancake)/10**9
    
    #Precio HCN en BNB
    hcn_price_BNB = '%.16f' %(bnb_pancake/hcn_pancake)
    
    #Precio HCN en USD
    hcn_price_USD = '%.16f' %(float(hcn_price_BNB) * float(usd_price_BNB["ethusd"]))
    
    print("precio USD en MXN es {}".format(CurrencyConverter().convert(1, 'USD', 'MXN')))
    
    #Precio HCN en MXN
    hcn_price_MXN = float(hcn_price_USD) * CurrencyConverter().convert(1, 'USD', 'MXN')

    data = {
        "liquidez_BNB":bnb_pancake,
        "HCN_encerrado":hcn_pancake,
        "precio_BNB":usd_price_BNB["ethusd"],
        "precio_HCN_BNB":hcn_price_BNB,
        "precio_HCN_USD":hcn_price_USD,
        "precio_HCN_MXN": '{:.10f}'.format(hcn_price_MXN)
    }

    write_file(JSON_FILE, data)

    print("Liquidez BNB")
    print(bnb_pancake)
    print("HCN Encerrado")
    print(hcn_pancake)
    print("Precio BNB")
    print(usd_price_BNB["ethusd"])
    print("Precio HCN en BNB")
    print(hcn_price_BNB)
    print("Precio HCN en USD")
    print(hcn_price_USD)
    print("Precio HCN en MXN")
    print(hcn_price_MXN)
