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
from PharmaBot.utility.pdf_parser import PdfParser
from PharmaBot.servicesResources.info_medicine import InfoMedicine
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

