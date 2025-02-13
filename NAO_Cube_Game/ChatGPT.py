# -*- coding: utf-8 -*-	
import json
import httplib


class ChatGPT:

    def __init__(self):
        pass

    @staticmethod
    def Request(content):
        try:
            with open("/data/home/nao/chatgpt.key", "r") as file:
                key = file.read()
            #Setup Chat-GPT connection and payload.
            conn = httplib.HTTPConnection("api.openai.com")
            payload = json.dumps({
               "model": "gpt-3.5-turbo",
               "logprobs": True,
               "messages": [
                 {
                   "role": "user",
                   "content": content
                 }
               ],
               "temperature": 1,
               "top_p": 1,
               "n": 1,
               "stream": False,
               "max_tokens": 500,
               "presence_penalty": 0,
               "frequency_penalty": 0
            })
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json; charset=utf-8',
                'Authorization': 'Bearer ' + key
            }
            #Perform the request to chatGPT
            conn.request("POST", "/v1/chat/completions", payload, headers)
            res = conn.getresponse()
            #In Greek, we have special characters that don't work on the old version of python 2.7 used in NAO, thus we need to filter a bit the string to make it readable.
            data = res.read().replace("\\n", " ").replace("\\\"","").encode('raw_unicode_escape').decode()
            jdata = json.loads(data)
            #Return only the answer, skipping other irrelevant information on returned by ChatGPT
            print("ChatGPT Result: " + jdata["choices"][0]["message"]["content"].replace("\"", ""))
            return jdata["choices"][0]["message"]["content"]
        except Exception as e:
            print("Chat GPT Exception: " + str(e))
            return ""