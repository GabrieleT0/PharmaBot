from typing import Dict
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
from botbuilder.schema import InputHints,ConversationReference
from PharmaBot.utility.pdf_parser import PdfParser
from PharmaBot.servicesResources.info_medicine import InfoMedicine
from PharmaBot.servicesResources import db_interface
from PharmaBot.utility import util_func 
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


class ReminderDialog(ComponentDialog):
    def __init__(self,conversation_references: Dict[str, ConversationReference],dialog_id: str = None):
        super(ReminderDialog,self).__init__(dialog_id or ReminderDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.medicine_name_step,
                    self.time_step,
                    self.result_step,
                    self.final_step,
                ],
            )
        )   
        self.conversation_references = conversation_references
        self.initial_dialog_id = WaterfallDialog.__name__

    async def medicine_name_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        reminder_info = step_context.options
        
        if reminder_info.medicine_name is None:
            message_text = 'Di quale medicina si tratta?'
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(reminder_info.medicine_name)
    
    async def time_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        reminder_info = step_context.options

        reminder_info.medicine_name = step_context.result

        if reminder_info.time is None:
            message_text = 'A che ora devi prendere la medicina ?'
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(reminder_info.time)

    async def result_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        reminder_info = step_context._options

        # Capture the response to the previous step's prompt
        reminder_info.time = step_context.result
        
        """
        This populates the shared Dictionary that holds conversation references. In this sample,
        this dictionary is used to send a message to members when /api/notify is hit.
        :param activity:
        :return:
        """
        conversation_reference = TurnContext.get_conversation_reference(step_context.context.activity)
        self.conversation_references[
            conversation_reference.user.id
        ] = conversation_reference

        reminder_str = f'Ricordati di prendere {reminder_info.medicine_name} alle {reminder_info.time}'
        
        result = db_interface.insert_reminder_info(conversation_reference.user.id,reminder_str)
        if result == False:
            message = MessageFactory.text("Errore nell'inserimento del reminder, riprova")
        else:
            message = MessageFactory.text('Reminder inserito, ogni giorno ti invierò un messaggio come promemoria')

        await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=message)
        )
        #call the final_step to end this convesation and call MainDialog.final_step. At this point the conversation is restarted
        return await step_context.end_dialog(reminder_info)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        if step_context.result:
            medicine_info = step_context.options

            return await step_context.end_dialog(medicine_info)
        return await step_context.end_dialog()
