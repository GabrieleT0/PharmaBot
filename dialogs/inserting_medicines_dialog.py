from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult
)
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, UserState
from botbuilder.schema import InputHints
from PharmaBot.utility.pdf_parser import PdfParser
from PharmaBot.servicesResources.info_medicine import InfoMedicine
from PharmaBot.utility import util_func
from PharmaBot.servicesResources import db_interface
from user_info import UserInfo
from PharmaBot.servicesResources import db_interface

class InsertingMedicinesDialog(ComponentDialog):
    def __init__(self, user_state:UserState,dialog_id: str = None):
        super(InsertingMedicinesDialog,self).__init__(dialog_id or InsertingMedicinesDialog.__name__)

        self.user_profile_accessor = user_state.create_property("UserInfo")

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.name_step,
                    self.type_step,
                    self.grams_step,
                    self.expiration_date_step,
                    self.confirmation_step,
                    self.final_step
                ],
            )
        )   

        self.initial_dialog_id = WaterfallDialog.__name__
        
    async def name_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context.options
        
        if medicine_info.name is None:
            message_text = 'Di quale medicina si tratta?'
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(medicine_info.name)
    
    async def type_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context._options

        medicine_info.name = step_context.result

        if medicine_info.type is None:
            message_text = 'Inserisci il tipo della medicina (pillola,granulato ecc...)'
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(medicine_info.type)

    async def grams_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context._options

        medicine_info.type = step_context.result

        if medicine_info.grams is None:
            message_text = 'Inserisci i grammi della medicina'
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(medicine_info.grams)

    async def expiration_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context._options

        medicine_info.grams = step_context.result

        if medicine_info.expiration_date is None:
            message_text = 'Inserisci la data di scadenza della medicina (formato dd/mm/aaaa, esempio: 13/01/2023)'
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(medicine_info.expiration_date)

    async def confirmation_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context._options

        medicine_info.expiration_date = step_context.result

        message_text = f"Hai inserito i suguenti dati per la medicina \n\n **Nome**: {medicine_info.name}\n\n **Tipo**: {medicine_info.type}\n\n **Grammi**: {medicine_info.grams}\n\n **Data scadenza**: {medicine_info.expiration_date}"
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )
        #returning the results at the users
        await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )
        #call the final_step to end this convesation and call MainDialog.final_step. At this point the conversation is restarted
        return await step_context.end_dialog(medicine_info)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        session_account = await self.user_profile_accessor.get(step_context.context,UserInfo)
        
        medicine_info = step_context.options
        
        result = db_interface.insert_medicine(session_account.email,medicine_info.name,medicine_info.type,medicine_info.grams,medicine_info.expiration_date)
        if result == True:
            message_text = f"Inserimento della medicina eseguito con successo. Ecco l'elenco aggiornato delle tue medicine:\n\n"
            user_info = db_interface.login(session_account.email)
            session_account.medicine = user_info.get_medicine()
            medicineLi = user_info.get_medicine()
            medicine_str = ''
            for medicine in medicineLi:
                medicine_str += medicine.capitalize() + '\n\n'
            session_account.medicine = medicine_str
            message_text += medicine_str
        else:
            message_text = "Errore nell'inserimento del medicinale, riprova."

        prompt_message = MessageFactory.text(message_text, message_text, InputHints.expecting_input)
        
        await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))
        
        return await step_context.end_dialog(medicine_info) 