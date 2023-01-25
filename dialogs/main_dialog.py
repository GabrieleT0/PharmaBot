from typing import Dict
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, TurnContext, UserState
from botbuilder.schema import InputHints,ConversationReference
from helpers.luis_helper import LuisHelper, Intent
from cognitiveModels.pharmaBotRecognizer import PharmaBotRecognizer
from dialogs.side_effects_dialog import SideEffectsDialog
from medicine_details import MedicineDetails
from dialogs.brochure_dialog import BrochureDialog
from dialogs.nearby_pharmacies_dialog import NearbyPharmaciesDialog
from dialogs.registration_dialog import RegistrationDialog
from dialogs.login_dialog import LoginDialog
from dialogs.inserting_medicines_dialog import InsertingMedicinesDialog
from dialogs.delete_medicine_dialog import DeleteMedicineDialog
from dialogs.update_medicine_dialog import UpdateMedicineDialog
from dialogs.what_is_dialog import WhatIsDialog
from dialogs.how_take_dialog import HowTakeDialog
from dialogs.before_take import BeforeTake
from dialogs.preservation_dialog import PreservationDialog
from dialogs.reminder_dialog import ReminderDialog
from dialogs.remove_reminder_dialog import RemoveReminderDialog
from dialogs.delete_account_dialog import DeleteAccountDialog
from user_info import UserInfo
from dialogs.help_dialog import HelpDialog
from servicesResources import db_interface

class MainDialog(ComponentDialog):
    def __init__(self, luis_recognizer: PharmaBotRecognizer, side_effects_dialog: SideEffectsDialog, 
                    brochure_dialog: BrochureDialog, nerby_ph_dialog:NearbyPharmaciesDialog, 
                    registration_dialog:RegistrationDialog,login_dialog:LoginDialog, ins_medicine_dialog: InsertingMedicinesDialog,
                    delete_medicine_dialog:DeleteMedicineDialog, update_medicine_dialog:UpdateMedicineDialog, 
                    what_is_dialog:WhatIsDialog,how_take_dialog:HowTakeDialog,before_take_dialog:BeforeTake,
                    preservation_dialog:PreservationDialog,reminder_dialog:ReminderDialog,remove_reminder_dialog:RemoveReminderDialog,
                    delete_account_dialog:DeleteAccountDialog,help_dialog:HelpDialog,user_state:UserState):
        super(MainDialog, self).__init__(MainDialog.__name__)

        self.user_profile_accessor = user_state.create_property("UserInfo")

        self._luis_recognizer = luis_recognizer
        self._side_effects_dialog_id = side_effects_dialog.id
        self._brouchure_dialog_id = brochure_dialog.id
        self._nerby_ph_dialog_id = nerby_ph_dialog.id
        self._registration_dialog_id = registration_dialog.id
        self._login_dialog_id = login_dialog.id
        self._ins_medicine_id = ins_medicine_dialog.id
        self._delete_medicine_id = delete_medicine_dialog.id
        self._update_medicine_dialog_id = update_medicine_dialog.id
        self._what_is_dialog_id = what_is_dialog.id
        self._how_take_dialog_id = how_take_dialog.id
        self._before_take_dialog_id = before_take_dialog.id
        self._preservation_dialog_id = preservation_dialog.id
        self._reminder_dialog_id = reminder_dialog.id
        self._remove_reminder_dialog_id = remove_reminder_dialog.id
        self._delete_account_dialog_id = delete_account_dialog.id
        self._help_dialog_id = help_dialog.id

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(side_effects_dialog)
        self.add_dialog(brochure_dialog)
        self.add_dialog(nerby_ph_dialog)
        self.add_dialog(registration_dialog)
        self.add_dialog(login_dialog)
        self.add_dialog(ins_medicine_dialog)
        self.add_dialog(delete_medicine_dialog)
        self.add_dialog(update_medicine_dialog)
        self.add_dialog(what_is_dialog)
        self.add_dialog(how_take_dialog)
        self.add_dialog(before_take_dialog)
        self.add_dialog(preservation_dialog)
        self.add_dialog(reminder_dialog)
        self.add_dialog(remove_reminder_dialog)
        self.add_dialog(delete_account_dialog)
        self.add_dialog(help_dialog)
        self.add_dialog(
            WaterfallDialog(
                "WFDialog", [self.intro_step, self.act_step, self.final_step]
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def intro_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 
        if not self._luis_recognizer.is_configured:
            await step_context.context.send_activity(
                MessageFactory.text(
                    "NOTE: LUIS is not configured. To enable all capabilities, add 'LuisAppId', 'LuisAPIKey' and "
                    "'LuisAPIHostName' to the appsettings.json file.",
                    input_hint=InputHints.ignoring_input,
                )
            )

            return await step_context.next(None)
        message_text = (
            str(step_context.options)
            if step_context.options
            else "Come posso aiutarti?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text, InputHints.expecting_input
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def act_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        session_account = await self.user_profile_accessor.get(step_context.context,UserInfo)
        if not self._luis_recognizer.is_configured:
            # LUIS is not configured, we just run the side_effects_dialog path with an empty MedicieDetails.
            return await step_context.begin_dialog(
                self._side_effects_dialog_id, MedicineDetails()
            )

        # Call LUIS and gather any potential booking details. (Note the TurnContext has the response to the prompt.)
        intent, luis_result = await LuisHelper.execute_luis_query(
            self._luis_recognizer, step_context.context
        )

        if intent == Intent.SIDE_EFFECTS.value and luis_result:
            #here we can also show a warning
    
            # Run the SideEffectsDialog giving it whatever details we have from the LUIS call.
            return await step_context.begin_dialog(self._side_effects_dialog_id, luis_result)
        
        if intent == Intent.BROCHURE_INFO.value and luis_result:
            return await step_context.begin_dialog(self._brouchure_dialog_id,luis_result)
        
        if intent == Intent.NEARBY_PHARMA.value and luis_result:
            return await step_context.begin_dialog(self._nerby_ph_dialog_id,luis_result)

        if intent == Intent.REGISTRATION.value and luis_result:
            if session_account.email is None:
                return await step_context.begin_dialog(self._registration_dialog_id,luis_result)
            else:
                alredy_login = (f"Sei gia autenticato come {session_account.email}")
                alredy_login = MessageFactory.text(alredy_login, alredy_login, InputHints.ignoring_input)
                await step_context.context.send_activity(alredy_login)
                return await step_context.next(None)

        if intent == Intent.LOGIN.value and luis_result:
            if session_account.email is None or session_account.firstName is None or session_account.email == 'None' or session_account.firstName == 'None':
                return await step_context.begin_dialog(self._login_dialog_id,luis_result)
            else:
                alredy_login = (f"Hai già fatto il login come {session_account.firstName} {session_account.lastName}")
                alredy_login = MessageFactory.text(alredy_login, alredy_login, InputHints.ignoring_input)
                await step_context.context.send_activity(alredy_login)
                return await step_context.next(None)
        
        if intent == Intent.INSERT_MEDICINE.value and luis_result:
            if session_account.email is not None:
                return await step_context.begin_dialog(self._ins_medicine_id,luis_result)
            else:
                no_logged = (f"Devi eseguire il login o registrarti per usare questa funzionalità")
                no_logged = MessageFactory.text(no_logged, no_logged, InputHints.ignoring_input)
                await step_context.context.send_activity(no_logged)
                return await step_context.next(None)
        
        if intent == Intent.MEDICINE_LIST.value and luis_result:
            medicineList = True
            if session_account.email is not None or session_account.email != 'None':
                if session_account.medicine is not None:
                    message_text = 'Ecco le medicine salvate nel tuo account: \n\n'
                    message_text += session_account.medicine
                    message_text = MessageFactory.text(message_text,message_text,InputHints.ignoring_input)
                    await step_context.context.send_activity(message_text)
                    return await step_context.next(None)
                else:
                    message_text = 'Non hai ancora registrato alcun farmaco'
                    message_text = MessageFactory.text(message_text,message_text,InputHints.ignoring_input)
                    await step_context.context.send_activity(message_text)
                    return await step_context.next(None)
            else:
                no_logged = (f"Devi eseguire il login o registrarti per usare questa funzionalità")
                no_logged = MessageFactory.text(no_logged, no_logged, InputHints.ignoring_input)
                await step_context.context.send_activity(no_logged)
                return await step_context.next(None)

        if intent == Intent.DELETE_MEDICINE.value and luis_result:
            if session_account.email is not None:
                return await step_context.begin_dialog(self._delete_medicine_id,luis_result)
            else:
                no_logged = (f"Devi eseguire il login o registrarti per usare questa funzionalità")
                no_logged = MessageFactory.text(no_logged, no_logged, InputHints.ignoring_input)
                await step_context.context.send_activity(no_logged)
                return await step_context.next(None)
        
        if intent == Intent.UPDATE_MEDICINE.value and luis_result:
            if session_account.email is not None:
                return await step_context.begin_dialog(self._update_medicine_dialog_id,luis_result)
            else:
                no_logged = (f"Devi eseguire il login o registrarti per usare questa funzionalità")
                no_logged = MessageFactory.text(no_logged, no_logged, InputHints.ignoring_input)
                await step_context.context.send_activity(no_logged)
                return await step_context.next(None)
        
        if intent == Intent.WHAT_IS.value and luis_result:
            return await step_context.begin_dialog(self._what_is_dialog_id, luis_result)
        
        if intent == Intent.HOW_TAKE.value and luis_result:
            return await step_context.begin_dialog(self._how_take_dialog_id,luis_result)
        
        if intent == Intent.BEFORE_TAKE.value and luis_result:
            return await step_context.begin_dialog(self._before_take_dialog_id,luis_result)
        
        if intent == Intent.PRESERVATION.value and luis_result:
            return await step_context.begin_dialog(self._preservation_dialog_id,luis_result)
        
        if intent == Intent.REMINDER.value and luis_result:
            return await step_context.begin_dialog(self._reminder_dialog_id,luis_result)
        
        if intent == Intent.DELETE_REMINDER.value and luis_result:
            return await step_context.begin_dialog(self._remove_reminder_dialog_id,luis_result)
        
        if intent == Intent.SHOW_REMINDER.value and luis_result:
            conversation_references = TurnContext.get_conversation_reference(step_context.context.activity)
            reminders = db_interface.get_str_reminder(conversation_references.user.id)
            if isinstance(reminders,list):
                if len(reminders) > 0:
                    message_text = 'Ecco i promemoria che hai inserito nel tuo account: \n\n'
                    for reminder in reminders:
                        message_text += reminder[0] + '\n\n'
                    message_text = MessageFactory.text(message_text,message_text,InputHints.ignoring_input)
                    await step_context.context.send_activity(message_text)
                    return await step_context.next(None)
                else:
                    no_reminder = (f"Non hai registrato ancora nessun promemoria.")
                    no_reminder = MessageFactory.text(no_reminder, no_reminder, InputHints.ignoring_input)
                    await step_context.context.send_activity(no_reminder)
                    return await step_context.next(None)
            else:
                    no_reminder = (f"Non hai registrato ancora nessun promemoria.")
                    no_reminder = MessageFactory.text(no_reminder, no_reminder, InputHints.ignoring_input)
                    await step_context.context.send_activity(no_reminder)
                    return await step_context.next(None)
        
        if intent == Intent.DEL_ACCOUNT.value and luis_result:
            if session_account.email is not None:
                return await step_context.begin_dialog(self._delete_account_dialog_id,luis_result)
            else:
                no_logged = (f"Devi eseguire il login o registrarti per usare questa funzionalità")
                no_logged = MessageFactory.text(no_logged, no_logged, InputHints.ignoring_input)
                await step_context.context.send_activity(no_logged)
                return await step_context.next(None)
        
        if intent == Intent.HELP.value:
            return await step_context.begin_dialog(self._help_dialog_id)
        
        if intent == Intent.WELCOME.value:
            message = 'Ciao sono Pharma bot, lieto di conoscerti.'
            await step_context.context.send_activity(message)
            return await step_context.next(None)

        else:
            didnt_understand_text = (
                "Scusami, non ho capito. Prova a riformulare la richiesta."
            )
            didnt_understand_message = MessageFactory.text(
                didnt_understand_text, didnt_understand_text, InputHints.ignoring_input
            )
            await step_context.context.send_activity(didnt_understand_message)

        return await step_context.next(None)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # If the one dialog was cancelled or the user failed to confirm,
        # the Result here will be null.
        if step_context.result is not None:
            result = step_context.result

            # Now we have all the booking details call the booking service.

            # If the call to the booking service was successful tell the user.
            # time_property = Timex(result.travel_date)
            # travel_date_msg = time_property.to_natural_language(datetime.now())
            #msg_txt = f"Hai cercato informazioni su {result.name.capitalize()} {result.type} {result.grams}"
            #message = MessageFactory.text(msg_txt, msg_txt, InputHints.ignoring_input)
            #await step_context.context.send_activity(message)

        prompt_message = "Cos'altro posso fare per te?"
        return await step_context.replace_dialog(self.id, prompt_message)
