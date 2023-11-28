# -*- coding: utf-8 -*-

import os
import requests
import base64
import sys

API_URL = "https://inscode-api.csdn.net/api/openapi/speech"
INSCODE_API_KEY = os.getenv("INSCODE_API_KEY")
DEFAULT_RATE = 16000
default_type = ["pcm", "wav", "amr", "m4a"]


def speech(type, speech):
    body = {
        "apikey": INSCODE_API_KEY,
    }

    if type not in default_type:
        raise ValueError("parameter 'type' is not supported, only pcm/wav/amr/m4a file format")

    body.update({"speech": file2base64(speech),
                 "format": type,
                 "rate": DEFAULT_RATE,
                 "channel": 1,
                 "cuid": INSCODE_API_KEY,
                 "len": get_file_size(speech)
                 })

    response = requests.post(API_URL, json=body)
    if response.status_code == 200:
        resp = response.json()
        if resp["code"] == 200:
            full_response = ""
            if resp:
                data = resp["data"]
                if data["err_no"] == 0:
                    result = data["result"]
                    for word in result:
                        full_response = full_response + "\n" + word
                    return full_response
                else:
                    return resp
            else:
                return "The API did not return any results."
        return resp
    else:
        return response


def file2base64(file_path):
    if isinstance(file_path, bytes):
        data = file_path
    elif hasattr(file_path,"read") and callable(getattr(file_path, "read")):
        data = file_path.read()
    else:
        with open(file_path, "rb") as f:
            data = f.read()
    content = base64.b64encode(data).decode()
    return content


def get_file_size(file_path):
    if isinstance(file_path, bytes):
        size = sys.getsizeof(file_path)
    elif hasattr(file_path, 'size'):
        size = file_path.size
    else:
        size = os.path.getsize(file_path)
    size = size
    return size
