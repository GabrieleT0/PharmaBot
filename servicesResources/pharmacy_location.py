import json
import os
import requests

PRIMARY_KEY = 'UMBo4xFK3pFCO8pQ_cwL-Bsmwu6YHnbhFFC_YAEUPeg'

class PharmacyLocation:
    def __init__(self):
        self.subscription_key = PRIMARY_KEY
    
    def get_lat_long(self,location,address):
        url = f'https://atlas.microsoft.com/search/address/json?api-version=1.0&query={address} {location}&subscription-key={self.subscription_key}'
        response = requests.get(url)
        response = response.json()
        position = response['results'][0]['position']
        lat = position['lat']
        lon = position['lon']

        return lat,lon
    
    def get_nearby_pharma(self,lat,lon):
        url = f'https://atlas.microsoft.com/search/poi/category/json?api-version=1.0&query=PHARMACY&typeahead=&limit=5&countrySet=IT&lat={lat}&lon={lon}&radius=5000&language=it-IT&extendedPostalCodesFor=PAD,Addr,POI&openingHours=nextSevenDays&subscription-key={self.subscription_key}'
        response = requests.get(url)
        response = response.json()
        results = response['results']
        nearby_pharma = []

        for poi in results:
            position = poi['position']
            latitude = position['lat']
            longitude = position['lon']
            poiValue = poi['poi']
            name = poiValue.get('name','').replace("'","")
            phone = poiValue.get('phone','')

            nearby_pharma.append((latitude,longitude,name,phone))

        #la is the x and y coordinate for the text position. ls is for the size of the labels. lc for label color. co for the pin color
        pinsOrg = f"default|la10 2|ls9|coFF3333|lc000000||'Tu sei qui'{lon} {lat}"
        layer = 'basic'
        style = 'main'
        zoom = '16'
        center = f'{lon},{lat}'
        height = '600'
        width = '600'
        pins = 'default|ls7|co00E600|lc000000|la0 1||'

        for i in range(len(nearby_pharma)-1):
            lat,lon,name,phone = nearby_pharma[i]
            pins +=f"'{name}'{lon} {lat}|"
        lat,lon,name,phone = nearby_pharma[len(nearby_pharma)-1]
        pins += f"'{name}'{lon} {lat}"

        image_request_url = f'https://atlas.microsoft.com/map/static/png?subscription-key={self.subscription_key}&api-version=1.0&layer={layer}&style={style}&zoom={zoom}&center={center}&height={height}&width={width}&language=Unified&view=Unified&pins={pins}&pins={pinsOrg}'
        resp = requests.get(image_request_url)

        here = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(here,'../map')
        save_path = os.path.join(save_path,"nearest_pharma.png")
    
        #Write the image with the nearest pharmacies in the map folder
        with open(save_path,'wb') as f:
            f.write(resp.content)

    def get_nearest_pharma(self,lat,lon):
        url = f'https://atlas.microsoft.com/search/poi/category/json?api-version=1.0&query=PHARMACY&typeahead=&limit=5&countrySet=IT&lat={lat}&lon={lon}&radius=5000&language=it-IT&extendedPostalCodesFor=PAD,Addr,POI&openingHours=nextSevenDays&subscription-key={self.subscription_key}'
        response = requests.get(url)
        response = response.json()
        results = response['results']

        #in the first position in the list there is the nearest pharmacy, then get all the information about it
        poi = results[0]
        name = poi['poi'].get('name','')
        phone = poi['poi'].get('phone','')
        address = poi.get('address','')

        return(name,phone,address)

azure_maps_api = PharmacyLocation()
latitude,longitude = azure_maps_api.get_lat_long('San Gregorio Magno','Via Roma,12 84020')
azure_maps_api.get_nearby_pharma(latitude,longitude)