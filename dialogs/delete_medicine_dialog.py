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
from user_info import UserInfo
from PharmaBot.servicesResources import db_interface
from PharmaBot.utility import util_func

class DeleteMedicineDialog(ComponentDialog):
    def __init__(self, user_state:UserState,dialog_id: str = None):
        super(DeleteMedicineDialog,self).__init__(dialog_id or DeleteMedicineDialog.__name__)

        self.user_profile_accessor = user_state.create_property("UserInfo")

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.name_step,
                    self.confirmation_step,
                    self.result_step,
                    self.final_step,
                ],
            )
        )   

        self.initial_dialog_id = WaterfallDialog.__name__
    
    async def name_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context.options
        session_account = await self.user_profile_accessor.get(step_context.context,UserInfo)
        medicine_str = session_account.medicine
        if medicine_str is not None:
            if medicine_info.name is None:
                medicine_str += '**Inserisci il nome del farmaco da cancellare**'
                prompt_message = MessageFactory.text(
                    medicine_str, medicine_str, InputHints.expecting_input
                )
                return await step_context.prompt(
                    TextPrompt.__name__, PromptOptions(prompt=prompt_message)
                )
            return await step_context.next(medicine_info.name)
        else:
            message_text = 'Non hai ancora registrato alcun farmaco'
            message_text = MessageFactory.text(message_text,message_text,InputHints.ignoring_input)
            await step_context.context.send_activity(message_text)
            return await step_context.end_dialog(medicine_info)
    
    async def confirmation_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context._options

        medicine_info.name = step_context.result

        session_account = await self.user_profile_accessor.get(step_context.context,UserInfo)

        medicine_li = db_interface.get_all_medicine(session_account.email)
        
        
        #return await step_context.end_dialog(medicine_info)
        found = False
        for medicine in medicine_li:
            if medicine['name'].lower() == medicine_info.name.lower():
                found = True
                name = medicine['name']
                type = medicine['type']
                grams = medicine['grams']
                expiration_date = medicine['expirationDate']
                message_text = f'Vuoi davvero cancellare {name} {type} {grams} {expiration_date} ?'
                break
        if found == True:
            prompt_message = MessageFactory.text(
                    message_text, message_text, InputHints.expecting_input
                )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        else:
            message_text = 'Non ho trovato il farmaco che vuoi cancellare'
            prompt_message = MessageFactory.text(
                    message_text, message_text, InputHints.ignoring_input
                )
            await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))
            return await step_context.end_dialog(medicine_info)

    async def result_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context._options

        answer = step_context.result
        
        session_account = await self.user_profile_accessor.get(step_context.context,UserInfo)
        
        if isinstance(answer,str):
            if answer.lower() == 'si' or 'sì':
                result = db_interface.delete_medicine(medicine_info.name,session_account.email)
                if result == True:
                    message_text = "**Cancellazione eseguita con successo.** \n\nEcco l'elenco aggiornato delle medicine registrate\n\n"
                    medicineLi = db_interface.get_all_medicine(session_account.email)
                    session_account.medicine = util_func.medicine_parser(medicineLi)
                    message_text += util_func.printMedicineLi(session_account.medicine) 
                else:
                    message_text = 'Errore nella cancellazione del farmaco, riprova.'
                
                prompt_message = MessageFactory.text(
                        message_text, message_text, InputHints.ignoring_input
                    )
                await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))
                
            else:
                message_text = 'Operazione annullata'
                prompt_message = MessageFactory.text(
                        message_text, message_text, InputHints.ignoring_input
                    )
                await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))
                return await step_context.end_dialog(medicine_info) 

        return await step_context.end_dialog(medicine_info) 

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        if step_context.result:
            medicine_info = step_context.options

            return await step_context.end_dialog(medicine_info)
        return await step_context.end_dialog()




    