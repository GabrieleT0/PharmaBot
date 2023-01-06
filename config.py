#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "31315b52-b5d9-4b32-9346-12b4d3445d7c")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "pharmabotproject!")
    LUIS_APP_ID = os.environ.get("LuisAppId","e8d4a0b6-f422-4990-8a98-117942c0829d")
    LUIS_API_KEY = os.environ.get("LuisAPIKey","5efe6b0cf85640038a946ca1e6086ef1")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","intentrecognizerpharmabot-authoring.cognitiveservices.azure.com/")
    BING_SEARCH_API_KEY = os.environ.get("BingSubscriptionKey","0eb55333dfea49a9bfa16d6a1a502684")
    COMPUTER_VISION_KEY = os.environ.get("ComputerVisonKey","2e27ac7a95824bc2b25ed1ed555ff1e3")
    COMPUTER_VISION_ENDPOINT = os.environ.get("ComputerVisionEndpoint","https://pharmavisiontzz.cognitiveservices.azure.com/")
    AZURE_MAP = os.environ.get("MapKey","3AHSHFUgZh5cpY6WKUyYGYyOJl6eSe43YvNGO5nNI2s")

    #e7b7eea1-309e-453f-98bb-7a6b535fc27d