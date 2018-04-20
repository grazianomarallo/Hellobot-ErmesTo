# -*- coding: utf-8 -*-

import googleapiclient.discovery
from oauth2client.client import GoogleCredentials
credentials = GoogleCredentials.get_application_default()

import logging
import base64

#PHRASES = ZONE.keys() + FERMATE.keys() + STOPS

def getTranscriptionTelegram(file_id, choices):
    import requests
    import key

    r = requests.get(key.TELEGRAM_API_URL + 'getFile', params={'file_id': file_id})
    rdict = r.json()
    #logging.debug('getFile response dict: {}'.format(rdict))
    file_path = rdict['result']['file_path']
    urlFile = key.TELEGRAM_BASE_URL_FILE + file_path
    #logging.debug('url: {}'.format(urlFile))
    fileContent = requests.get(urlFile).content
    speech_content = base64.b64encode(fileContent)
    #logging.debug('speech_content: {}'.format(speech_content))

    service = googleapiclient.discovery.build('speech', 'v1', credentials=credentials)
    service_request = service.speech().recognize(
        body={
            "config": {
                "encoding": 'OGG_OPUS',  # enum(AudioEncoding)
                "sampleRateHertz": 16000,
                "languageCode": 'it-IT',
                "maxAlternatives": 1,
                "speechContexts": {
                    "phrases": choices
                }
            },
            "audio": {
                "content": speech_content
            }
        })

    r_dict = service_request.execute()
    logging.debug('speech api response: {}'.format(r_dict))

    if 'results' in r_dict:
        return r_dict['results'][0]['alternatives'][0]['transcript']
    return None

'''
def getTranscriptionFacebook(voice_url, choices):
    import requests
    fileContent = requests.get(voice_url).content
    speech_content = base64.b64encode(fileContent)

    service = googleapiclient.discovery.build('speech', 'v1', credentials=credentials)
    service_request = service.speech().recognize(
        body={
            "config": {
                "encoding": 'OGG_OPUS',  # enum(AudioEncoding)
                "sampleRateHertz": 16000,
                "languageCode": 'it-IT',
                "maxAlternatives": 1,
                "speechContexts": {
                    "phrases": choices
                }
            },
            "audio": {
                "content": speech_content
            }
        })

    r_dict = service_request.execute()
    logging.debug('speech api response: {}'.format(r_dict))

    if 'results' in r_dict:
        return r_dict['results'][0]['alternatives'][0]['transcript']
    return None
'''
