import json
import os.path

from typing import Dict, List
from botbuilder.core import (
    ConversationState,
    MessageFactory,
    UserState,
    TurnContext,
    CardFactory
)
from botbuilder.dialogs import Dialog
from botbuilder.schema import Attachment, ChannelAccount,ConversationReference,HeroCard,CardImage,CardAction,ActionTypes
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
                message = MessageFactory.attachment(self.welcome_card())
                await turn_context.send_activity(message)
                await DialogHelper.run_dialog(
                    self.dialog,
                    turn_context,
                    self.conversation_state.create_property("DialogState"),
                )
    #TODO:INSERT PATH FOR FIND FILE EVEN IF THE APP ISN'T ON THIS PC
    def welcome_card(self) -> Attachment:
        buttons = [
            CardAction(
                title='Foglio illustrativo',
                type=ActionTypes.im_back,
                value='foglio illustrativo',
            ),
            CardAction(
                title='Effetti indesiderati',
                type=ActionTypes.im_back,
                value='effetti indesiderati',
            ),
            CardAction(
                title='Registra un account',
                type=ActionTypes.im_back,
                value='registrazione',
            ),
            CardAction(
                title='Login',
                type=ActionTypes.im_back,
                value='login',
            ),
            CardAction(
                title='Farmacie nelle vicinanze',
                type=ActionTypes.im_back,
                value='farmacie vicine',
            ),
            CardAction(
                title='Sto assumendo un nuovo farmaco',
                type=ActionTypes.im_back,
                value='nuovo farmaco assunto',
            )
        ]
        card = HeroCard(images=[CardImage(url='D:/Desktop/PharmaBot/utility/logo.png')],title='Benvenuto su PharmaBot!',subtitle='Cosa so fare?',text='Posso cercare per te info sulle medicine, puoi creare un tuo account dove tener traccia delle medicine che stai assumendo e mostrarti le farmacie nelle vicinanze ... e non solo. Inizia subito ad usarmi.',buttons=buttons)
        return CardFactory.hero_card(card)