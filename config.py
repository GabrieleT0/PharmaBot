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
    LUIS_APP_ID = os.environ.get("LuisAppId","38a20b4d-9fdb-4c7d-a847-bc2430d711cf")
    LUIS_API_KEY = os.environ.get("LuisAPIKey","2783e238a9c5401382fa8b7b2fe7627b")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","pharmabotnlp-authoring.cognitiveservices.azure.com/")
    BING_SEARCH_API_KEY = os.environ.get("BingSubscriptionKey","12222c27d52343edab82905cdac1189b")
    COMPUTER_VISION_KEY = os.environ.get("ComputerVisonKey","59587ffc503946ea91b35e727ebfbc01")
    COMPUTER_VISION_ENDPOINT = os.environ.get("ComputerVisionEndpoint","https://pharmarecognizer.cognitiveservices.azure.com/")
    AZURE_MAP = os.environ.get("MapKey","gV42Tjj2pfZpxYocIl2isYzFd8BrgfoZJD1dJxI12-o")