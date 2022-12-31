from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext
from medicine_details import MedicineDetails
from location_info import LocationInfo
from user_info import UserInfo

class Intent(Enum):
    SIDE_EFFECTS = "effettiIndesiderati"
    BROCHURE_INFO = "foglioIllustrativo"
    NEARBY_PHARMA = "farmacieVicine"
    REGISTRATION = 'registrazione'
    INSERT_MEDICINE = 'inserisciMedicine'
    DELETE_MEDICINE = 'eliminaFarmaco'
    LOGIN = 'login'
    CANCEL = "Cancel"
    MEDICINE_LIST = 'visualizzaMedicine'
    GET_WEATHER = "GetWeather"
    NONE_INTENT = "NoneIntent"

def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)

class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> (Intent,object):
        """
            Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)
            
            intent = (
                sorted(
                    recognizer_result.intents,
                    key = recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )
            #Extract the data that we need from the LUIS JSON response
            if intent == Intent.SIDE_EFFECTS.value:
                result = MedicineDetails()
                medicine_name = recognizer_result.entities.get("$instance",{}).get("farmaco",[])
                medicine_type = recognizer_result.entities.get("$instance",{}).get("tipo",[])
                medicine_grams = recognizer_result.entities.get("$instance",{}).get("grammi",[])
                if len(medicine_name) > 0:
                    result.name = medicine_name[0]['text']
                if len(medicine_type) > 0:
                    result.type = medicine_type[0]['text']
                if len(medicine_grams) >0:
                    result.grams = medicine_grams[0]['text']
            
            if intent == Intent.BROCHURE_INFO.value:
                result = MedicineDetails()
                medicine_name = recognizer_result.entities.get("$instance",{}).get("farmaco",[])
                medicine_type = recognizer_result.entities.get("$instance",{}).get("tipo",[])
                medicine_grams = recognizer_result.entities.get("$instance",{}).get("grammi",[])
                if len(medicine_name) > 0:
                    result.name = medicine_name[0]['text']
                if len(medicine_type) > 0:
                    result.type = medicine_type[0]['text']
                if len(medicine_grams) >0:
                    result.grams = medicine_grams[0]['text']
            
            if intent == Intent.NEARBY_PHARMA.value:
                result = LocationInfo()
                location_name = recognizer_result.entities.get("$instance",{}).get("località",[])
                address = recognizer_result.entities.get("$instance",{}).get("via",[])
                house_number = recognizer_result.entities.get("$instance",{}).get("numeroCivico",[])
                if len(location_name) > 0:
                    result.location_name = location_name[0]['text']
                if len(address) > 0:
                    result.address = address[0]['text']
                if len(house_number) > 0:
                    result.house_number = house_number[0]['text']
            
            if intent == Intent.REGISTRATION.value:
                result = UserInfo()

            if intent == Intent.LOGIN.value:
                result = UserInfo()

            if intent == Intent.INSERT_MEDICINE.value:
                result = MedicineDetails()
                medicine_name = recognizer_result.entities.get("$instance",{}).get("farmaco",[])
                medicine_type = recognizer_result.entities.get("$instance",{}).get("tipo",[])
                medicine_grams = recognizer_result.entities.get("$instance",{}).get("grammi",[])
                if len(medicine_name) > 0:
                    result.name = medicine_name[0]['text']
                if len(medicine_type) > 0:
                    result.type = medicine_type[0]['text']
                if len(medicine_grams) >0:
                    result.grams = medicine_grams[0]['text']
            
            if intent == Intent.MEDICINE_LIST.value:
                result = UserInfo()

            if intent == Intent.DELETE_MEDICINE.value:
                result = MedicineDetails()
                medicine_name = recognizer_result.entities.get("$instance",{}).get("farmaco",[])
                medicine_type = recognizer_result.entities.get("$instance",{}).get("tipo",[])
                medicine_grams = recognizer_result.entities.get("$instance",{}).get("grammi",[])
                if len(medicine_name) > 0:
                    result.name = medicine_name[0]['text']
                if len(medicine_type) > 0:
                    result.type = medicine_type[0]['text']
                if len(medicine_grams) >0:
                    result.grams = medicine_grams[0]['text']
                



        except Exception as exception:
            print(exception)

        return intent, result