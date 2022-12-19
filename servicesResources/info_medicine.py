#Class that use bing search for search medicine info
import requests
import http.client, urllib.parse
import json
from PharmaBot.utility import util_func
from PharmaBot.utility.pdf_parser import PdfParser
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

SUBSCRIPTION_KEY = "47e87f10209e4e9faf4edb816d2b7e2d"

class InfoMedicine:
    def __init__(self):
        self.headers = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}
        self.search_url = 'https://api.bing.microsoft.com/v7.0/search'
        self.search_url_img = 'https://api.bing.microsoft.com/v7.0/images/search'

    '''
    Search for the pdf of the medicine brouchure.
    '''
    def get_brochure(self,medicine_info):
        query = f"{medicine_info} foglio illustrativo+site:farmaci.agenziafarmaco.gov.it+ext:pdf+filetype:pdf"
        params = {"q":query,"textDecorations":True,"textFormat":"HTML",'setLang':'it-IT','mkt':'it-IT','count':'3'}
        response = requests.get(self.search_url,headers=self.headers,params=params)
        response.raise_for_status()
        response_results = response.json()
        web_pages = response_results['webPages']
        web_pages_values = web_pages['value']
        urls = []
        for value in web_pages_values:
            urls.append(value['url'])
        pdf_link = util_func.get_pdf_link(urls)
        
        return pdf_link

    def get_img(self,medicine_info):
        query = f"{medicine_info} medicinale"
        params = {"q":query,'setLang':'it-IT','mkt':'it-IT','imageType':'photo'}
        response = requests.get(self.search_url_img,headers=self.headers,params=params)
        response.raise_for_status()
        response_results = response.json()
        thumbnail_urls = [img["thumbnailUrl"] for img in response_results["value"][:16]]
        
        return thumbnail_urls[0]
    
    def get_what(self,medicine_info):
        query = f"a cosa serve {medicine_info}"
        params = {"q":query,"textDecorations":True,"textFormat":"HTML",'setLang':'it-IT','mkt':'it-IT','count':'3'}
        response = requests.get(self.search_url,headers=self.headers,params=params)
        response.raise_for_status()
        response_results = response.json()

        print(response_results)



bing_api = InfoMedicine()
bing_api.get_what('oki')
