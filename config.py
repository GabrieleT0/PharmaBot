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
    LUIS_APP_ID = os.environ.get("LuisAppId","27d3c9c0-7a73-4ec8-887f-b5c7123601bb")
    LUIS_API_KEY = os.environ.get("LuisAPIKey","92b5c1608b844dc6b6c3732b1d32b0a2")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","pharmabotnlpgab-authoring.cognitiveservices.azure.com/")
    BING_SEARCH_API_KEY = os.environ.get("BingSubscriptionKey","9e9b2cee8e4e40179194ee4cd890358a")
    COMPUTER_VISION_KEY = os.environ.get("ComputerVisonKey","2d8b077e041a41969f91fd83864fb466")
    COMPUTER_VISION_ENDPOINT = os.environ.get("ComputerVisionEndpoint","https://computervisionpharma.cognitiveservices.azure.com/")
    AZURE_MAP = os.environ.get("MapKey","EsgffZzPRRWBNz5hinKWBonYn0T7KywfV0u-HW77mHM")