#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    #APP_ID = os.environ.get("MicrosoftAppId", "")
    #APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    APP_ID = os.environ.get("MicrosoftAppId", "fd0c970f-aa6b-466d-8084-81489c77b686")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "RhY8Q~ZgSUr.D5CGjakCT_JqchgXa3zOk0tzWaqM")
    LUIS_APP_ID = os.environ.get("LuisAppId","1c387b7d-bba0-47e2-a99a-107b00acbc51")
    LUIS_API_KEY = os.environ.get("LuisAPIKey","cc102b99957e41719a4bc01c8a711fdf")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","pharmabotnlp-authoring.cognitiveservices.azure.com/")
    BING_SEARCH_API_KEY = os.environ.get("BingSubscriptionKey","8d86a8dfefc34b07a3b966b381f63a06")
    COMPUTER_VISION_KEY = os.environ.get("ComputerVisonKey","3c93f5a9d86e4dc582650a1f7ec8a3b2")
    COMPUTER_VISION_ENDPOINT = os.environ.get("ComputerVisionEndpoint","https://photopharmarecognizer.cognitiveservices.azure.com/")
    AZURE_MAP = os.environ.get("MapKey","V8_Y_GhtVfbPKYp2cWNjZqO8sEbp-T3QNoehRACPCKw")

