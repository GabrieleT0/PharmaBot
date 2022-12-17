#Class that use bing search for search medicine info
import requests
import http.client, urllib.parse
import json

SUBSCRIPTION_KEY = "47e87f10209e4e9faf4edb816d2b7e2d"

class InfoMedicine:
    def __init__(self):
        self.headers = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}
        self.search_url = 'https://api.bing.microsoft.com/v7.0/search'

    
    def get_brochure(self,medicine_info):
        query = f"{medicine_info}+site:farmaci.agenziafarmaco.gov.it+ext:pdf+filetype:pdf"
        params = {"q":query,"textDecorations":True,"textFormat":"HTML",'setLang':'it-IT','mkt':'it-IT','count':'3'}
        response = requests.get(self.search_url,headers=self.headers,params=params)
        response.raise_for_status()
        response_results = response.json()
        return (json.dumps(response_results,indent=4))

    def get_personal(self,medicine_info):
        query = f"{medicine_info}"
        params = {"q":query,"textDecorations":True,"textFormat":"HTML",'setLang':'it-IT','mkt':'it-IT','count':'3'}
        response = requests.get(self.search_url,headers=self.headers,params=params)
        response.raise_for_status()
        response_results = response.json()
        return (json.dumps(response_results,indent=4))
    
# (?i)\d.+Possibili effetti indesiderati(?=\ \n+\d)
med = InfoMedicine()
print(med.get_personal("possibili effetti indesiderati brufen"))
    