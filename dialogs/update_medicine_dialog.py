from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, UserState
from botbuilder.schema import InputHints,CardAction,SuggestedActions,ActionTypes
from PharmaBot.servicesResources import db_interface
from PharmaBot.servicesResources.info_medicine import InfoMedicine
from PharmaBot.utility import util_func
from user_info import UserInfo

class UpdateMedicineDialog(ComponentDialog):
    def __init__(self, user_state:UserState,dialog_id: str = None):
        super(UpdateMedicineDialog,self).__init__(dialog_id or UpdateMedicineDialog.__name__)

        self.user_profile_accessor = user_state.create_property("UserInfo")

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.name_step,
                    self.field_step,
                    self.field_value_step,
                    self.update_step,
                ],
            )
        )   

        self.initial_dialog_id = WaterfallDialog.__name__
    
    async def name_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context.options

        session_account = await self.user_profile_accessor.get(step_context.context,UserInfo)

        message_text = "Ecco l'elenco delle medicine che hai registrato\n\n"
        medicineLi = session_account.medicine
        if medicineLi is not None:
            message_text += medicineLi
            if medicine_info.name is None:
                message_text += '**Inserisci il nome della medicina che vuoi modificare.**'
                prompt_message = MessageFactory.text(
                    message_text, message_text, InputHints.expecting_input
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
    
    async def field_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context.options

        medicine_info.name = step_context.result

        reply = MessageFactory.text("Quale campo vuoi modificare?")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Nome",
                    type=ActionTypes.im_back,
                    value="Nome",
                    image_alt_text="R",
                ),
                CardAction(
                    title="Tipo",
                    type=ActionTypes.im_back,
                    value="Tipo",
                    image_alt_text="Y",
                ),
                CardAction(
                    title="Grammi",
                    type=ActionTypes.im_back,
                    value="Grammi",
                    image_alt_text="B",
                ),
                CardAction(
                    title="Data della scadenza",
                    type=ActionTypes.im_back,
                    value="Data",
                    image_alt_text="B",
                ),   
            ]
        )
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )

    async def field_value_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context._options

        # Capture the response to the previous step's prompt
        #used medicine type filed to store the filed to update in the medicine
        medicine_info.type = step_context.result
        
        if medicine_info.type != 'Nome' and medicine_info.type != 'Tipo' and medicine_info.type != 'Grammi' and medicine_info.type != 'Data della scadenza':
            message_text = '**Operazione non supportata**'
            prompt_message = MessageFactory.text(message_text, message_text, InputHints.ignoring_input)
            await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))
            return await step_context.end_dialog(medicine_info)


        if medicine_info.type == 'Data':
            message_text = f'Inserisci il nuovo valore per il campo {medicine_info.type}, ricordati di rispettare il seguente formato: gg/mm/aaaa (ad esempio 13/01/2023)'
        else:
            message_text = f'Inserisci il nuovo valore per il campo {medicine_info.type}'
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def update_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context._options

        # Capture the response to the previous step's prompt
        new_value = step_context.result

        field_to_update = medicine_info.type
        #print(f'Campo da aggiornare: {medicine_info.type}, Medicina da aggiornare: {medicine_info.name}, Nuovo valore:{new_value}')
        
        session_account = await self.user_profile_accessor.get(step_context.context,UserInfo)

        if field_to_update == 'Nome':
            field_to_update = 'medicineName'
            result = db_interface.update_medicine(medicine_info.name,field_to_update,new_value,session_account.email)
            if result is True:
                message_text = '**Modifica eseguita.**'
            else:
                message_text = '**Errore nella fase di modifica, riprova**'
        elif field_to_update == 'Tipo':
            field_to_update = 'medicineType'
            result = db_interface.update_medicine(medicine_info.name,field_to_update,new_value,session_account.email)
            if result is True:
                message_text = '**Modifica eseguita.**'
            else:
                message_text = '**Errore nella fase di modifica, riprova**'
        elif field_to_update == 'Grammi':
            field_to_update = 'medicineGrams'
            result = db_interface.update_medicine(medicine_info.name,field_to_update,new_value,session_account.email)
            if result is True:
                message_text = '**Modifica eseguita.**'
            else:
                message_text = '**Errore nella fase di modifica, riprova**'
        elif field_to_update == 'Data':
            field_to_update = 'expirationDate'
            result = db_interface.update_medicine(medicine_info.name,field_to_update,new_value,session_account.email)
            if result is True:
                message_text = '**Modifica eseguita.**'
            else:
                message_text = '**Errore nella fase di modifica, riprova**'

        message_text = ''
        medicineLi = db_interface.get_all_medicine(session_account.email)
        session_account.medicine = util_func.printMedicineLi(util_func.medicine_parser(medicineLi))
        medicine_txt = "Ecco l'elenco aggiornato delle tue medicine \n\n"
        medicine_txt += session_account.medicine
        message_text += '\n\n' + medicine_txt
        prompt_message = MessageFactory.text(message_text, message_text, InputHints.ignoring_input)
        
        await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))
        return await step_context.end_dialog(medicine_info)
        