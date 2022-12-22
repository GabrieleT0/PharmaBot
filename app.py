import sys
import traceback
from datetime import datetime
from http import HTTPStatus

from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    MemoryStorage,
    BotFrameworkAdapter,
    ConversationState,
    UserState,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes
from cognitiveModels.pharmaBotRecognizer import PharmaBotRecognizer
from bots import PharmaBot
from config import DefaultConfig
from dialogs import MainDialog
from dialogs.side_effects_dialog import SideEffectsDialog
from dialogs.brochure_dialog import BrochureDialog
from dialogs.nearby_pharmacies_dialog import NearbyPharmaciesDialog

CONFIG = DefaultConfig()
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)
ADAPTER = BotFrameworkAdapter(SETTINGS)
RECOGNIZER = PharmaBotRecognizer(CONFIG)
SIDE_EFFECTS_DIALOG = SideEffectsDialog()
BROCHURE_DIALOG = BrochureDialog()
NEARBY_PHARMACY_DIALOG = NearbyPharmaciesDialog()
DIALOG = MainDialog(RECOGNIZER,SIDE_EFFECTS_DIALOG,BROCHURE_DIALOG,NEARBY_PHARMACY_DIALOG)

BOT = PharmaBot(CONVERSATION_STATE,USER_STATE,DIALOG)

# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )

ADAPTER.on_turn_error = on_error

BOT = PharmaBot(CONVERSATION_STATE, USER_STATE, DIALOG)

async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)

APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error