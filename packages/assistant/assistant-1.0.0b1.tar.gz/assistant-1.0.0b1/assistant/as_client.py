#!/usr/bin/env python

import os
import requests
import json
import websockets
import asyncio
import random

from requests.exceptions import RequestException
from websockets.exceptions import ConnectionClosedOK

from assistant import (
    USERNAME,
    HOME,
)

ASSISTANT_HOST, ASSISTANT_PORT = "0.0.0.0", "5068"

def is_assistant_up():
    try:
        r = requests.get(f"http://{ASSISTANT_HOST}:{ASSISTANT_PORT}")
        if r.status_code == 200:
            return True
        else:
            raise Exception()
    except Exception as e:
        return False

def is_listen_service_up():
    try:
        r = requests.get(f"http://localhost:5063/")
        if r.status_code == 200:
            return True
        else:
            raise Exception()
    except Exception as e:
        return False

def is_assistant_listening():
    if os.path.isfile(f'{HOME}/.config/systemd/user/default.target.wants/assistant.listen.service'):
        return True
    else:
        return False

def is_auth_to_listen():
    if is_assistant_listening():
        return True
    else:
        return False

def is_allowed_to_speak():
    try:
        r = requests.get(f"http://localhost:5067/")
        if r.status_code == 200:
            return True
        else:
            raise Exception()
    except Exception as e:
        return False

def nlp_intent_hello_version():
    try:
        r = requests.get(f"http://localhost:5005/")
        if r.status_code == 200:
            return r.text
        else:
            raise Exception(f"{r.status_code}: {r.text}")
    except Exception as e:
        return None

def nlp_intent_hello():
    response = None
    headers = {'content-type': 'application/json'}
    m = random.choice(["hello"])
    payload = { 'message': m, 'sender': f"{USERNAME}" }
    r = requests.post(f"http://localhost:5005/webhooks/rest/webhook", json=payload, headers=headers)
    if r.status_code == 200:
        rj = r.json()
        if rj:
            response = "\n".join(x.get('text', "") for x in rj)
        else:
            pass
    else:
        pass
    return response

def nlp_intent_exit():
    response = None
    headers = {'content-type': 'application/json'}
    m = random.choice(["exit"])
    payload = { 'message': m, 'sender': f"{USERNAME}" }
    try:
        r = requests.post(f"http://localhost:5005/webhooks/rest/webhook", json=payload, headers=headers)
        if r.status_code == 200:
            rj = r.json()
            if rj:
                response = "\n".join(x.get('text', "") for x in rj)
    except requests.exceptions.ConnectionError:
        pass

    return response

async def nlp(query: str, user: str, host=ASSISTANT_HOST, port=ASSISTANT_PORT):
    try:
        async with websockets.connect(f"ws://{host}:{port}/api/v1/assistant") as ws:
            req = {'query': query, 'user': user}
            
            await ws.send(json.dumps(req).encode('utf-8'))
            r = json.loads(await ws.recv())
            await ws.close()
            if r.get('message'):
                return r.get('message')
            elif r.get('answer'):
                return r.get('answer')
    except ConnectionClosedOK:
        return

async def query(question: str, user: str):
    return await nlp(question, user)

def request_conversation(user, base_url="/api/v1/conversation/", host=ASSISTANT_HOST, port=ASSISTANT_PORT):
	url = f"http://{host}:{port}{base_url}{user}"
	try:
		response = requests.get(url)

		# Consider any status other than 2xx an error
		if not response.status_code // 100 == 2:
			return {}, "<red>Error requesting conversation: Unexpected response</red>"

		json_obj = json.loads(response.json())
		return json_obj, ""
	except RequestException as e:
		# A serious problem happened, like an SSLError or InvalidURL
		return {}, "<red>Error requesting conversation: Could not reach server</red>"

