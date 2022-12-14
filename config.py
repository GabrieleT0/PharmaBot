#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.environ.get("LuisAppId","d4476f7d-cc5a-463d-a275-4f0a881fef87")
    LUIS_API_KEY = os.environ.get("LuisAPIKey","e15ecb24e73348daaa330a65f6472106")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","pharmabot-authoring.cognitiveservices.azure.com/")