import azure.functions as func
import requests
import logging

URL = 'https://pharmabotappgab.azurewebsites.net'

def main(mytimer: func.TimerRequest) -> None:
    requests.get(f'{URL}/api/notify')    
    logging.info('Python timer triggr function executed, reminder sended')