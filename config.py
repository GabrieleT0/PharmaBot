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
    LUIS_APP_ID = os.environ.get("LuisAppId","b402167c-e294-4c8b-9f8f-5546ad28f407")
    LUIS_API_KEY = os.environ.get("LuisAPIKey","ce821b3dada04f819da268c9a5e249a3")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","luispharmabot-authoring.cognitiveservices.azure.com/")
    BING_SEARCH_API_KEY = os.environ.get("BingSubscriptionKey","2b76dea5271342dab69a1da8aeefa374")
    COMPUTER_VISION_KEY = os.environ.get("ComputerVisonKey","f200e03fe51f4feab10a2742c2e76c23")
    COMPUTER_VISION_ENDPOINT = os.environ.get("ComputerVisionEndpoint","https://pharmaborrecognizer.cognitiveservices.azure.com/")
    AZURE_MAP = os.environ.get("MapKey","kujCX3tvRBEdG9dvQ_RDGP7De3jl-aKmj-MSVIkfFhU")