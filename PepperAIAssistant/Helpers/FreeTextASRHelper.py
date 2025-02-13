# -*- coding: utf-8 -*-	
import time
import base64
import json
import httplib

class FreeTextASRHelper:
    shouldListen = False
    audioPath = "/data/home/nao/RecordedAudio.ogg"

    def __init__(self, session):
        self.timer = None
        self.audioDevice = session.service("ALAudioDevice")
        self.callback = None

    #Record audio for specific time before processing it. Unfortunately we cant do real time recording and processing.
    def Listen(self, callback, timeout):
        if self.audioDevice:
            self.callback = callback
            print("Listening for "+ str(timeout) + " seconds")
            self.StopListening()
            self.shouldListen = True
            self.audioDevice.startMicrophonesRecording(self.audioPath)
            time.sleep(timeout)
            self.audioDevice.stopMicrophonesRecording()
            self.PerformRequest()
    
    #Stop audio recording.
    def StopListening(self):
        if self.audioDevice:
            try:
                self.audioDevice.stopMicrophonesRecording()
                self.shouldListen = False
            except:
                print("Didn't need to stop listening.")

    #Perform a request to Google Transcribe so we can get the text from the audio.
    def PerformRequest(self):
        with open("/data/home/nao/googleapi.key", "r") as file:
            key = file.read()
        with open(self.audioPath, "rb") as file:
            data = file.read()
        base64Encoded = base64.b64encode(data)
        conn = httplib.HTTPSConnection("speech.googleapis.com")
        #Setup the Language for the transcription.
        payload = json.dumps(
        {
           "config": {
                   "languageCode": "en-US",
                   "encoding": "Linear16",
                   "sampleRateHertz": 16000,
                   "enableWordTimeOffsets": True
           },
           "audio": {
               "content": base64Encoded
           }
        })
        headers = {
           'Content-Type': 'application/json',
           'Accept': 'application/json',
        }
        conn.request("POST", "/v1/speech:recognize?key=" + key, payload, headers)
        res = conn.getresponse()
        #We need to do some hacks here to correct the transcription for greek language due to older version of python.
        data = res.read().replace("\\n", " ").replace("\\\"","").encode('raw_unicode_escape').decode()
        print("ASR Response: " + data)
        jdata = json.loads(data)
        print("Transcript:" + jdata['results'][0]['alternatives'][0]['transcript'])
        self.callback(jdata['results'][0]['alternatives'][0]['transcript'])
