from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult
)
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, UserState,CardFactory
from botbuilder.schema import InputHints,Attachment, ChannelAccount,ConversationReference,HeroCard,CardImage,CardAction,ActionTypes
from utility.pdf_parser import PdfParser
from servicesResources.info_medicine import InfoMedicine
from utility import util_func

class HelpDialog(ComponentDialog):
    def __init__(self,dialog_id: str = None):
        super(HelpDialog,self).__init__(dialog_id or HelpDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.help_step,
                ],
            )
        )   

        self.initial_dialog_id = WaterfallDialog.__name__
    
    async def help_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        message_text = 'Ecco le mie principali funzioni:\n\n'
        message_text = ' Posso darti le seguenti informazioni sulle medicine\n\n'
        message_text += '  **1.** Recupero del foglio illustrativo.\n\n' \
                        '  **2.** Effetti indesiderati.\n\n' \
                        '  **3.** Come assumerlo.\n\n' \
                        '  **4.** Cose da sapere prima di assumerlo.\n\n' \
                        '  **5.** Come conservarlo.\n\n'
        message_text += '- Se crei un account, puoi inserire le medicine che stai assumendo e ' \
                        'inserire la relativa data di scadenza\n\n'
        message_text += '- Posso mostrarti le farmacie nelle vicinanze\n\n'
        message_text +=' - Posso inviarti un promemoria per ricordati di assumere le medicine'

        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.ignoring_input
        )
        await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

        card = HeroCard(title='Inizia subito ad usarmi!',buttons=[
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
                title='Come assumere farmaco',
                type=ActionTypes.im_back,
                value='come prendere farmaco',
            ),
            CardAction(
                title="Cose da sapere prima dell'assunzione",
                type=ActionTypes.im_back,
                value='avvertenze assunzione farmaco',
            ),
            CardAction(
                title='Registrati',
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
            ),
            CardAction(
                title='Modifica farmaci assunti',
                type=ActionTypes.im_back,
                value='modifica farmaco',
            ),
            CardAction(
                title='Elimina farmaco registrato',
                type=ActionTypes.im_back,
                value='elimina farmaco',
            ),
            CardAction(
                title='Elimina il mio account',
                type=ActionTypes.im_back,
                value='elimina account',
            ),
            CardAction(
                title='Imposta nuovo promemoria per medicina',
                type=ActionTypes.im_back,
                value='nuovo promemoria',
            ),
            ],
        )

        #message = MessageFactory.attachment(CardFactory.hero_card(card))
        #await step_context.context.send_activity(message)
        return await step_context.end_dialog()
    