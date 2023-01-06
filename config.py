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
    LUIS_APP_ID = os.environ.get("LuisAppId","a378ee5a-4629-4816-9a21-dcb815cb7ffa")
    LUIS_API_KEY = os.environ.get("LuisAPIKey","a5f713a1cc50454fb45a8c828c8e799e")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName","pharmabottuozzog-authoring.cognitiveservices.azure.com/")