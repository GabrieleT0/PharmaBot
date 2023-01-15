from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult
)
from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, UserState
from botbuilder.schema import InputHints
from utility.pdf_parser import PdfParser
from servicesResources.info_medicine import InfoMedicine
from utility import util_func

class BeforeTake(ComponentDialog):
    def __init__(self,dialog_id: str = None):
        super(BeforeTake,self).__init__(dialog_id or BeforeTake.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.medicine_step,
                    self.result_step,
                    self.final_step,
                ],
            )
        )   

        self.initial_dialog_id = WaterfallDialog.__name__
    
    async def medicine_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context.options

        if medicine_info.name is None:
            message_text = 'Di quale medicina si tratta?'
            prompt_message = MessageFactory.text(
                message_text, message_text, InputHints.expecting_input
            )
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
        return await step_context.next(medicine_info.name)
    
    async def result_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        medicine_info = step_context._options

        # Capture the response to the previous step's prompt
        medicine_info.name = step_context.result

        bing_api = InfoMedicine()
        pdf_link = bing_api.get_brochure(medicine_info.name)
        pdf_file = PdfParser(pdf_link)
        before_take = pdf_file.before_take()
        if isinstance(before_take,str):
            before_take = util_func.duplicate_new_line(before_take)
        else:
            before_take = 'Mi dispiace, non sono riuscito a trovare questo farmaco'
            
        prompt_message = MessageFactory.text(
                before_take, before_take, InputHints.expecting_input
            )
        #returning the results at the users
        await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )
        #call the final_step to end this convesation and call MainDialog.final_step. At this point the conversation is restarted
        return await step_context.end_dialog(medicine_info)
    
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        if step_context.result:
            medicine_info = step_context.options

            return await step_context.end_dialog(medicine_info)
        return await step_context.end_dialog()