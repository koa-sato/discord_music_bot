import json
import os
from typing import List
import requests

class Deezer():
    def __init__(self):
        self.arl = os.getenv('DEEZER_ARL_COOKIE')
        self.queue = []
        self.startService()
        self.unofficialApiQueries = {
            'api_version': '1.0',
            'api_token': '',
            'input': 3
        }

    def initRequest(self):
        httpHeaders = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'cache-control': 'max-age=0',
            'accept-language': 'en-US,en;q=0.9,en-US;q=0.8,en;q=0.7',
            'accept-charset': 'utf-8,ISO-8859-1;q=0.8,*;q=0.7',
            'content-type': 'text/plain;charset=UTF-8',
            'cookie': 'arl=' + self.arl
        }

        requestConfig = {
            'retry': {
                'attempts': 9999999999,
                'delay': 1000, # 1 second
            },
            'defaults': {
                'headers': httpHeaders,
            }
        }
        self.requestWithCache = requests.Session()
        self.requestWithCache.headers.update(requestConfig['defaults']['headers'])
        self.requestWithoutCache = requests.Session()
        self.requestWithoutCache.headers.update(requestConfig['defaults']['headers'])
        self.requestConfigWithoutCacheAndRetry = {
            'defaults': {
                'headers': httpHeaders
            }
        }

    def initDeezerCredentials(self):
        arl = self.arl
        if arl:
            return arl
        else:
            arl = self.arl
            self.initRequest()
            return arl


    # def convertContentToJson(self, content):
    #     if type(content) == List:
    #         content=json.loads(content)
    #     print(content)
    #     for key, value in content.items():
    #         if type(value) is List:
    #             value = self.convertContentToJson(value)
    #     return content

    def searchForSong(self, song):
        song = song.replace(" ", "%20")
        unofficialApiUrl = 'https://api.deezer.com/search?q=' + song
        requestBody = None
        requestQueries = self.unofficialApiQueries
        requestParams = {
            'method': 'POST',
            'url': unofficialApiUrl,
            'qs': requestQueries,
            'body': requestBody,
            'json': True,
            'jar': True
        }
        request = self.requestWithoutCache
        response = request.get(requestParams['url'])
        if "json" in response.headers['Content-Type']:
            content = json.loads(response.content.decode("utf-8"))
            return(content['data'][0]['link'])
        else:
            return "response wasn't in json"

    def readQueue(self):
        if len(self.queue != 0):
            song = self.queue[0]
            del self.queue[0]
            self.searchForSong(song)
    
    def addToQueue(self, song):
        self.queue.append(song)

    def startService(self):
        self.initRequest()
        self.initDeezerCredentials()

# d = Deezer()
# print(d.searchForSong("Faded Heart"))