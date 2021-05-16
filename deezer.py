import atexit
import json
import os
import requests
import threading

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
            'content-type': 'text/plain;charset=UTF-8',
            'cookie': 'arl=' + self.arl
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
        arl = self.arl
        if arl:
            return arl
        else:
            arl = self.arl
            self.initRequest()
            return arl

    def getDeezerUrlParts(self, deezerUrl):
        urlParts = deezerUrl.split("/")[-3:]
        return {
            'type': urlParts[1],
            'id': urlParts[2]
        }

    def getTrackDownloadUrl(self, trackInfos, trackQuality):
        pass

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
            if len(content['data']) == 0:
                return "No close song found"
            print(content['data'][0]['preview'])
            return(content['data'][0]['link'])
        else:
            return "response wasn't in json"

    def downloadSong(self, url):
        self.requestWithoutCache = {
            "url": url,
            "headers": self.httpHeaders,
            "jar": True,
            "encoding": None
        }

        # requestParams = {
        #     'method': 'POST',
        #     'url': self.unofficialApiUrl,
        #     'qs': requestQueries,
        #     'body': requestBody,
        #     'json': True,
        #     'jar': True
        # }
        request = self.requestWithoutCache
        response = request.get(url, type='application/json')
        print(response)


    def readQueue(self):
        while(True):
            if len(self.queue != 0):
                song = self.queue[0]
                del self.queue[0]
                self.downloadSong(song)
    
    def addToQueue(self, song):
        self.queue.append(song)

    def startService(self):
        self.initRequest()
        self.initDeezerCredentials()

    def __init__(self):
        self.arl = os.getenv('DEEZER_ARL_COOKIE')
        self.queue = []
        self.startService()
        self.unofficialApiQueries = {
            'api_version': '1.0',
            'api_token': '',
            'input': 3
        }
        atexit.register(self.exit_handler)
        # self.queue_thread = threading.Thread(target=self.readQueue, args=None)


d = Deezer()
print(d.searchForSong("Faded Heart"))
# d.downloadSong("https://www.deezer.com/track/446685592")