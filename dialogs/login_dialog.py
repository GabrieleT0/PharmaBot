from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import InputHints
from PharmaBot.utility.pdf_parser import PdfParser
from PharmaBot.servicesResources.info_medicine import InfoMedicine
from PharmaBot.utility import util_func
from PharmaBot.servicesResources import db_interface

class LoginDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(LoginDialog,self).__init__(dialog_id or LoginDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.email_step,
                    self.password_step,
                    self.result_step,
                    self.final_step
                ],
            )
        )   

        self.initial_dialog_id = WaterfallDialog.__name__
    
    async def email_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        account_info = step_context.options

        if account_info.email is None:
            message_text = 'Inserisci la tua email'
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(account_info.email)
    
    async def password_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        account_info = step_context.options

        # Capture the response to the previous step's prompt
        account_info.email = step_context.result

        if account_info.password is None:
            message_text = 'Inserisci la password'
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(account_info.password)

    async def result_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        account_info = step_context._options

        # Capture the response to the previous step's prompt
        account_info.password = step_context.result

        pwd = db_interface.get_pwd(account_info.email)
        result = util_func.check_pwd(account_info.password,pwd.encode('utf-8'))
        if result == True:
            account_info = db_interface.login(account_info.email)

            message = f'Benvenuto {account_info.firstName}'
            prompt_message = MessageFactory.text(
                    message, message, InputHints.expecting_input
                )
            #returning the results at the users
            await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        #call the final_step to end this convesation and call MainDialog.final_step. At this point the conversation is restarted
        return await step_context.end_dialog(account_info)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        if step_context.result:
            account_info = step_context.options

            return await step_context.end_dialog(account_info)
        return await step_context.end_dialog()