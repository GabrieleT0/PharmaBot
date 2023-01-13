# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Dict
from botbuilder.core import ActivityHandler, ConversationState, UserState, TurnContext
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper
from botbuilder.core import MessageFactory, TurnContext, CardFactory
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
    SuggestedActions,
    ConversationReference
)
from servicesResources.computer_vision import ComputerVision
from servicesResources.info_medicine import InfoMedicine
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions


#Bot used for conversation
class DialogBot(ActivityHandler):
    def __init__(
        self,
        conversation_references: Dict[str, ConversationReference],
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        if conversation_state is None:
            raise Exception(
                "[DialogBot]: Missing parameter. conversation_state is required"
            )
        if user_state is None:
            raise Exception("[DialogBot]: Missing parameter. user_state is required")
        if dialog is None:
            raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_references = conversation_references
        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have occurred during the turn.
        await self.conversation_state.save_changes(turn_context, False)
        await self.user_state.save_changes(turn_context, False)

    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.attachments is not None:
            await self._send_suggested_actions(turn_context,)
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )

    
    async def _send_suggested_actions(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """
        attach_obj = turn_context.activity.attachments[0]
        computer_vision = ComputerVision()
        img_text = computer_vision.get_text_from_img(attach_obj.content_url)
        bing_api = InfoMedicine()
        pdf_link = bing_api.get_brochure(img_text)
        img_url = bing_api.get_img(img_text)
        card = HeroCard(images=[CardImage(url=img_url)],buttons=[CardAction(type=ActionTypes.download_file,title=f'Clicca e visualizza il foglio illustrativo di {img_text.capitalize()} in pdf',value=pdf_link)],)
        card = CardFactory.hero_card(card)
        message = MessageFactory.attachment(card)
        await turn_context.send_activity(message)