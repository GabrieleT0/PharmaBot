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
    LUIS_APP_ID = os.environ.get("LuisAppId","b2def22c-5386-4a5d-9145-8c7a1722d1ef")
    LUIS_API_KEY = os.environ.get("LuisAPIKey","54e619791a4d484fa7159e2ab38e9081")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","pharmabotnlpgabriele-authoring.cognitiveservices.azure.com/")
    BING_SEARCH_API_KEY = os.environ.get("BingSubscriptionKey","b78481d45ad64ec5b9f2fc8c23fe8f8d")
    COMPUTER_VISION_KEY = os.environ.get("ComputerVisonKey","e835e89aa2c24dd089db94c23ecfd288")
    COMPUTER_VISION_ENDPOINT = os.environ.get("ComputerVisionEndpoint","https://pharmavision.cognitiveservices.azure.com/")
    AZURE_MAP = os.environ.get("MapKey","gj59d2CqK7KUlZB_-Y7QNS1QcpmBXE1GOwknJNidPHs")