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
    LUIS_APP_ID = os.environ.get("LuisAppId","8742e0bc-8bba-4af3-bfae-a51eba0f49cb")
    LUIS_API_KEY = os.environ.get("LuisAPIKey","49d1ca646ffd4ab4998c11b700442e04")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","pharmabotnlpgab-authoring.cognitiveservices.azure.com/")
    BING_SEARCH_API_KEY = os.environ.get("BingSubscriptionKey","0e9421b3c34e4a669c0e2f1583a12d86")
    COMPUTER_VISION_KEY = os.environ.get("ComputerVisonKey","7eb696fd3a124d4f841cd1e4e45d51b6")
    COMPUTER_VISION_ENDPOINT = os.environ.get("ComputerVisionEndpoint","https://photorecognizer.cognitiveservices.azure.com/")
    AZURE_MAP = os.environ.get("MapKey","mu5KReYECrE7Xmge20oj4XJK1x1sJelpAGPABY40h5Y")

