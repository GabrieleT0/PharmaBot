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
    BING_SEARCH_API_KEY = os.environ.get("BingSubscriptionKey","7cb1c8d822dc42c7bc0e603b36db15be")
    COMPUTER_VISION_KEY = os.environ.get("ComputerVisonKey","2781518279d74380ad95e81a046831b5")
    COMPUTER_VISION_ENDPOINT = os.environ.get("ComputerVisionEndpoint","https://pharmarecognizer.cognitiveservices.azure.com/")
    AZURE_MAP = os.environ.get("MapKey","CK0LKTUA-9yz96r8lg1YUV2qATp-Uw8LvW-1kMtSUVI")