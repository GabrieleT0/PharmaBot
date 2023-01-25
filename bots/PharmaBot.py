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
                #message = MessageFactory.attachment(self.welcome_card())
                message = MessageFactory.text('Benvenuto su **PharmaBot**, se non sai cosa posso fare, digita aiuto.')
                await turn_context.send_activity(message)
                await DialogHelper.run_dialog(
                    self.dialog,
                    turn_context,
                    self.conversation_state.create_property("DialogState"),
                )
                
        conversation_reference = TurnContext.get_conversation_reference(turn_context.activity)
        self.conversation_references[
            conversation_reference.user.id
        ] = conversation_reference

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
        here = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(here,'../utility')
        img_path = os.path.join(save_path,"logo.png")
        card = HeroCard(images=[CardImage(url=img_path)],title='Benvenuto su PharmaBot!',subtitle='Cosa so fare?',text='Posso cercare per te info sulle medicine, puoi creare un tuo account dove tener traccia delle medicine che stai assumendo e mostrarti le farmacie nelle vicinanze ... e non solo. Inizia subito ad usarmi.',buttons=buttons,)
        
        return CardFactory.hero_card(card)