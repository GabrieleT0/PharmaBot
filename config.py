#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "fd0c970f-aa6b-466d-8084-81489c77b686")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "RhY8Q~ZgSUr.D5CGjakCT_JqchgXa3zOk0tzWaqM")
    LUIS_APP_ID = os.environ.get("LuisAppId","339a8857-bcf4-4af8-9920-abe414b569f0")
    LUIS_API_KEY = os.environ.get("LuisAPIKey","40c4f8451f0f48c3af8cfc9c66f1f9bf")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","https://luisbotres-authoring.cognitiveservices.azure.com/")
    BING_SEARCH_API_KEY = os.environ.get("BingSubscriptionKey","5100efc3ae4743419d2d8d1447ed05e6")
    COMPUTER_VISION_KEY = os.environ.get("ComputerVisonKey","0aec1dee0fca425c824e72e6acff66c8")
    COMPUTER_VISION_ENDPOINT = os.environ.get("ComputerVisionEndpoint","https://pharmarecognization.cognitiveservices.azure.com/")
    AZURE_MAP = os.environ.get("MapKey","7N5UWI3tf7dTH5vJ3bIbkkSFnLOiKwumQKm5QqP2bJE")

