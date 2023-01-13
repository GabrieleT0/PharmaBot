import base64
import os
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
from utility.pdf_parser import PdfParser
from servicesResources.info_medicine import InfoMedicine
from utility import util_func 
import requests
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardAction,
    CardImage,
    ActivityTypes,
    Attachment,
    AttachmentData,
    Activity,
    ActionTypes,
)
from servicesResources.pharmacy_location import PharmacyLocation

class NearbyPharmaciesDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(NearbyPharmaciesDialog,self).__init__(dialog_id or NearbyPharmaciesDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.location_name_step,
                    self.address_step,
                    self.house_number_step,
                    self.cap_step,
                    self.result_step,
                    self.final_step,
                ],
            )
        )   

        self.initial_dialog_id = WaterfallDialog.__name__
    
    async def location_name_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        location_info = step_context.options

        if location_info.location_name is None:
            message_text = 'Qual è il nome della città in cui ti trovi?'
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(location_info.location_name)
    
    async def address_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        location_info = step_context.options

        location_info.location_name = step_context.result

        if location_info.address is None:
            message_text = "Qual è l'indirizzo dove ti trovi?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(location_info.address)
    
    async def house_number_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        location_info = step_context.options

        location_info.address = step_context.result

        if location_info.house_number is None:
            message_text = "Qual è il tuo numero civico?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(location_info.house_number)
    
    async def cap_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        location_info = step_context.options

        location_info.house_number = step_context.result

        if location_info.cap is None:
            message_text = "Qual è il tuo CAP?"
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(location_info.cap)

    async def result_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        location_info = step_context.options

        location_info.cap = step_context.result

        meassage_text = f'Informazioni inserite\n Localita:{location_info.location_name}, indirizzo:{location_info.address}, numero civico:{location_info.house_number}, CAP:{location_info.cap}  '
        prompt_message = MessageFactory.text(
                meassage_text, meassage_text, InputHints.expecting_input
            )

        azure_map_api = PharmacyLocation()
        lat,lon = azure_map_api.get_lat_long(location_info.location_name,location_info.address +' '+ location_info.house_number + ', ' + location_info.cap)
        azure_map_api.get_nearby_pharma(lat,lon)
        name,phone,address = azure_map_api.get_nearest_pharma(lat,lon)

        message = MessageFactory.attachment(self.hero_card_map(name,phone,address))
        

        #returning the results at the users
        await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=message)
        )
        #call the final_step to end this convesation and call MainDialog.final_step. At this point the conversation is restarted
        return await step_context.end_dialog(location_info)
    
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        if step_context.result:
            location_info = step_context.options

            return await step_context.end_dialog(location_info)
        return await step_context.end_dialog()
    

    def hero_card_map(self,name,phone,address):
        
        here = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(here,'../map')
        save_path = os.path.join(save_path,"nearest_pharma.png")
        with open(save_path,'rb') as file:
            base64_img = base64.b64encode(file.read()).decode()
        att = Attachment(name='Ciao',content_type='image/png',
        content_url=f"data:image/png;base64,{base64_img}",)
        if isinstance(phone,str) and phone != '':
            nearest_pharma_info = f'La farmacia più vicina a te si chiama **{name}**. \n\n Si trova in **{address}**\n\n Questo è il suo numero di telefono: **{phone}**'
        else:
            nearest_pharma_info = f'La farmacia più vicina a te si chiama **{name}**. \n\n Si trova in **{address}**\n\n'
        card = HeroCard(images=[CardImage(url=f"data:image/png;base64,{base64_img}")],text=nearest_pharma_info)

        return CardFactory.hero_card(card)
        
