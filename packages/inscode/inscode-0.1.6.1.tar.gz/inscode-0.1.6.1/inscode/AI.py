# -*- coding: utf-8 -*-

import json
import os
import requests

API_URL = "https://inscode-api.csdn.net/api/v1/gpt/"
INSCODE_API_KEY = os.getenv("INSCODE_API_KEY")


def ai(prompt, content):
    if content is None or len(content) == 0:
        raise ValueError("parameter 'content' cannot be empty")

    messages = []
    if prompt is not None and len(prompt) > 0:
        messages.append({"role": "system", "content": prompt})

    messages.append({"role": "user", "content": content})

    body = {
        "messages": messages,
        "apikey": INSCODE_API_KEY,
    }
    response = requests.post(API_URL, json=body)

    if response.status_code == 200:
        if response.text:
            try:
                response_parts = response.text.strip().split("\n")[:-1]
                full_response = ""
                for part in response_parts:
                    if part.startswith("data:"):
                        json_part = json.loads(part[5:])
                        rep_content = json_part["choices"][0]["delta"].get("content", "")
                        full_response += rep_content
                return full_response
            except json.JSONDecodeError as e:
                print("Unable to parse JSON-formatted data returned by the API:")
                print(response.text)
                print("Error details:", str(e))
                return None
        else:
            print("The API did not return any results.")
            return None
    else:
        print("Error:", response.status_code, response.text)
        return None
