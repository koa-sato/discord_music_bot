import atexit
import json
import os
import requests
import deezer

from typing import List

class Deezer():
    def exit_handler(self):
        with open("queue.txt", "w") as queue_file:
            for url in self.queue:
                queue_file.write(url + "\n")


    def initRequest(self):
        self.httpHeaders = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'cache-control': 'max-age=0',
            'accept-language': 'en-US,en;q=0.9,en-US;q=0.8,en;q=0.7',
            'accept-charset': 'utf-8,ISO-8859-1;q=0.8,*;q=0.7',
            'content-type': 'text/plain;charset=UTF-8'
        }

        self.requestConfig = {
            'retry': {
                'attempts': 9999999999,
                'delay': 1000, # 1 second
            },
            'defaults': {
                'headers': self.httpHeaders,
            }
        }
        self.requestWithCache = requests.Session()
        self.requestWithCache.headers.update(self.requestConfig['defaults']['headers'])
        self.requestWithoutCache = requests.Session()
        self.requestWithoutCache.headers.update(self.requestConfig['defaults']['headers'])
        self.requestConfigWithoutCacheAndRetry = {
            'defaults': {
                'headers': self.httpHeaders
            }
        }

        with open("queue.txt", "r") as queue_file:
            lines = queue_file.readlines()
            for line in lines:
                line = line.replace("\n", "")
                if line is not "":
                    self.queue.append(line)
        
    def initDeezerCredentials(self):
        self.deezer_client = deezer.Client(app_id=os.getenv('DEEZER_APP_ID'), app_secret=os.getenv('DEEZER_SECRET'))

    def getDeezerUrlParts(self, deezerUrl):
        urlParts = deezerUrl.split("/")[-3:]
        return {
            'type': urlParts[1],
            'id': urlParts[2]
        }

    def searchForSong(self, song):
        song = song.replace(" ", "%20")
        unofficialApiUrl = 'https://api.deezer.com/search?q=' + song
        requestBody = None
        requestQueries = self.unofficialApiQueries
        requestParams = {
            'method': 'GET',
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
            if len(content['data']) == 0:
                return "No close song found"
            return(content['data'][0]['link'])
        else:
            return "response wasn't in json"
    
    def addToQueue(self, song):
        self.queue.append(song)

    def startService(self):
        self.initRequest()
        self.initDeezerCredentials()

    def __init__(self):
        self.queue = []
        self.startService()
        self.unofficialApiQueries = {
            'api_version': '1.0',
            'api_token': '',
            'input': 3
        }
        atexit.register(self.exit_handler)