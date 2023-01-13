from typing import Dict
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult
)
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, UserState, TurnContext
from botbuilder.schema import InputHints, ConversationReference,CardAction,ActionTypes,SuggestedActions
from utility.pdf_parser import PdfParser
from servicesResources.info_medicine import InfoMedicine
from user_info import UserInfo
from servicesResources import db_interface
from utility import util_func

class RemoveReminderDialog(ComponentDialog):
    def __init__(self, conversation_references: Dict[str, ConversationReference],dialog_id: str = None):
        super(RemoveReminderDialog,self).__init__(dialog_id or RemoveReminderDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.reminders_step,
                    self.confirmation_step,
                ],
            )
        )   
        self.conversation_references = conversation_references
        self.initial_dialog_id = WaterfallDialog.__name__
    
    async def reminders_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        conversation_reference = TurnContext.get_conversation_reference(step_context.context.activity)
        reminders = db_interface.get_str_reminder(conversation_reference.user.id)
        if len(reminders) > 0:
            cards_list = []
            for reminder in reminders:
                card = CardAction(
                        title=reminder[0],
                        type=ActionTypes.post_back,
                        value=str(reminder[1]),
                    )
                cards_list.append(card)
            
            reply = MessageFactory.text("Quale reminder vuoi cancellare?")
            reply.suggested_actions = SuggestedActions(actions=cards_list)
        else:
            reply = 'Non hai registrato alcun promemoria'
            prompt_message = MessageFactory.text(
            reply, reply, InputHints.ignoring_input
            )
            await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
            return await step_context.end_dialog()
        
        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=reply)
        )
    
    async def confirmation_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        reminder_info = step_context.options

        choice = step_context.result

        result = db_interface.delete_reminder(choice)
        if result == True:
            reply = 'Promemoria cancellato con successo'
        else:
            reply = 'Errore nella cancellazione del reminder, riprova.'
        
        prompt_message = MessageFactory.text(
        reply, reply, InputHints.ignoring_input
        )
        await step_context.prompt(
        TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )
        return await step_context.end_dialog()


    