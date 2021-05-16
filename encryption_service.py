import os
import sys
import hashlib

class EncryptionService:

    def __init__(self):
        return

    def getSongFileName(trackInfos, trackQuality):
        step1 = [trackInfos.MD5_ORIGIN, trackQuality, trackInfos.SNG_ID, trackInfos.MEDIA_VERSION].join('¤')
        return None

    def getBlowfishKey(self, trackInfos):
        SECRET = b'g4el58wc0zvf9na1'
        md5 = hashlib.md5()
        md5.update(trackInfos['SNG_ID'])
        idMd5 = md5.hexdigest()
        bfKey = ""
        for i in range(0, 16):
            # print(str(SECRET.decode('utf-8')[i]))
            bfKey += str(ord(str(idMd5[i])) ^ ord(str(idMd5[i + 16])) ^ ord(str(SECRET.decode('utf-8')[i])))
        return bfKey

    def decryptTrack(self, trackBuffer):
        blowFishKey = self.getBlowfishKey()

        progress = 0
        while (progress < trackBuffer.length):

e = EncryptionService()
e.getBlowfishKey()