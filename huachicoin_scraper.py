import requests
import bs4
import re
import json
from currency_converter import CurrencyConverter


JSON_FILE = './huachicoin_data.json'


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

    url_pancake_swap_BNB = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c&address=0x6f8546EB8b92e6F8f927A0A5B2f90A1D5b8E52ee&tag=latest&apikey=49R78GV1AM594JYGRPZXMZYX4I83WZ522K")
    url_pancake_swap_HCN = requests.get("https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0863d3605f2b16183b500e3b5fe205b46739e3e6&address=0x6f8546EB8b92e6F8f927A0A5B2f90A1D5b8E52ee&tag=latest&apikey=49R78GV1AM594JYGRPZXMZYX4I83WZ522K")
    url_price_BNB = requests.get("https://api.bscscan.com/api?module=stats&action=bnbprice&apikey=49R78GV1AM594JYGRPZXMZYX4I83WZ522K")
    
    #BeautifulSoup para extrae informacion 
    soup_BNB = bs4.BeautifulSoup(url_pancake_swap_BNB.content, "html.parser").string
    soup_HCN = bs4.BeautifulSoup(url_pancake_swap_HCN.content, "html.parser").string
    soup_price_BNB = bs4.BeautifulSoup(url_price_BNB.content, "html.parser").string
    
    #JSON a Diccionario
    bnb_pancake = json.loads(soup_BNB)
    hcn_pancake = json.loads(soup_HCN)
    usd_price_BNB = json.loads(soup_price_BNB)["result"]
    
    #Liquidez BNB
    bnb_pancake = int(bnb_pancake["result"])/10**18
    
    #HCN Encerrado
    hcn_pancake = int(hcn_pancake["result"])/10**9
    
    #Precio HCN en BNB
    hcn_price_BNB = '%.16f' %(bnb_pancake/hcn_pancake)
    
    #Precio HCN en USD
    hcn_price_USD = '%.16f' %(float(hcn_price_BNB) * float(usd_price_BNB["ethusd"]))
    
    #Precio HCN en MXN
    hcn_price_MXN = float(hcn_price_USD) * CurrencyConverter().convert(1, 'USD', 'MXN')

    data = {
        "liquidez_BNB":bnb_pancake,
        "HCN_encerrado":hcn_pancake,
        "precio_BNB":usd_price_BNB["ethusd"],
        "precio_HCN_BNB":hcn_price_BNB,
        "precio_HCN_USD":hcn_price_USD,
        "precio_HCN_MXN":str(hcn_price_MXN)
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
