import azure.functions as func
import requests
import logging

URL = 'http://localhost:3978'

def main(mytimer: func.TimerRequest) -> None:
    requests.get(f'{URL}/api/notify')    
    logging.info('Python timer triggr function executed, reminder sended')