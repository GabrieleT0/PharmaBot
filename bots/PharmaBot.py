import json
import os.path

from typing import Dict, List
from botbuilder.core import (
    ConversationState,
    MessageFactory,
    UserState,
    TurnContext,
)
from botbuilder.dialogs import Dialog
from botbuilder.schema import Attachment, ChannelAccount,ConversationReference
from helpers.dialog_helper import DialogHelper

from .dialog_bot import DialogBot

#bot used for welocome message
class PharmaBot(DialogBot):
    def __init__(
        self,
        conversation_references: Dict[str, ConversationReference],
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        super(PharmaBot, self).__init__(
            conversation_references,conversation_state, user_state, dialog
        )

    async def on_members_added_activity(
        self, members_added: List [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            # Greet anyone that was not the target (recipient) of this message.
            # To learn more about Adaptive Cards, see https://aka.ms/msbot-adaptivecards for more details.
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity('Ciao e benvenuto')
                await DialogHelper.run_dialog(
                    self.dialog,
                    turn_context,
                    self.conversation_state.create_property("DialogState"),
                )
