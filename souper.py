__author__ = 'bison'

import urllib
#import BeautifulSoup4
import requests
from bs4 import BeautifulSoup
import os
import sys
import datetime
import json

class souperDuper(object):
    def __init__(self, soupAccount):
        self.account = soupAccount
        self.counter = 0
        #self.knownUrlsFile = os.path.join("images", self.account + ".knownUrls.txt")
        self.knownUrlsFile = self.account + ".knownUrls.txt"
        self.knownUrls = {}

        self.lastPage = ""
        self.doResume = False
        self.imageTypes = ['.jpg', '.jpeg', '.gif']

    def loadKnownUrls(self, fullPath=""):
        if fullPath == "":
            fullPath = self.knownUrlsFile

        if os.path.isfile(fullPath):
            fh = open(fullPath, 'r')
            tmpJson = fh.read()
            if tmpJson != "":
                self.knownUrls = json.loads(tmpJson)
            fh.close()

    def saveKnownUrls(self, fullPath=""):
        if fullPath == "":
            fullPath = self.knownUrlsFile

        fh = open(fullPath, 'w')
        fh.write(json.dumps(self.knownUrls))
        fh.close()

    def grabPart(self, max=1):
        self.loadKnownUrls()

        html = self.grabPage()

        foundNext = True
        cnt = 0
        while foundNext:
            self.saveKnownUrls()

            nextSegment = self.getNextEndless(html)
            if not nextSegment:
                foundNext = False
            else:
                self.debug("got: " + str(len(self.knownUrls)) + " next: " + nextSegment)
                html = self.grabPage(nextSegment)
            cnt += 1
            if cnt >= max:
                self.saveKnownUrls()
                yield None
                cnt = 0

        self.saveKnownUrls()


    def grabAll(self):
        self.loadKnownUrls()

        html = self.grabPage()

        foundNext = True
        while foundNext:
            self.saveKnownUrls()

            nextSegment = self.getNextEndless(html)
            if not nextSegment:
                foundNext = False
            else:
                self.debug("got: " + str(len(self.knownUrls)) + " next: " + nextSegment)
                html = self.grabPage(nextSegment)

        self.saveKnownUrls()

    def grabPage(self, urlExt=""):
        grabUrl = 'http://' + self.account + '.soup.io'
        prettyHtml = ""
        #SOUP.Endless.next_url
        if urlExt != "":
            grabUrl += "/" + urlExt

        try:
            response = requests.get(grabUrl)
            html = response.content
            #print(html)
            soup = BeautifulSoup(html)

            #print(soup.prettify())
            #exit()
            #for link in soup.findAll('a'):
            #    print(link.get('href'))

            for img in soup.findAll('img'):
                imgUrl = str(img.get('src'))
                if "asset" in imgUrl and not "square" in imgUrl:
                    if not imgUrl in self.knownUrls and self._isValidFile(imgUrl):
                        self.counter += 1
                        self.knownUrls[imgUrl] = self.counter

                        self.debug(str(self.counter) + ' > ' + imgUrl)
            prettyHtml = soup.prettify()
        except Exception as ex:
            self.debug("ERROR: " + grabUrl + "\n" + str(ex))

        return prettyHtml

    def _isValidFile(self, url):
        if not self.imageTypes:
            return True

        #fileExt = imgUrl.split('.')
        #fileExt = fileExt[len(fileExt)-1]
        fileName, fileExt = os.path.splitext(url)
        #print fileName,"#", fileExt, fileExt in self.imageTypes
        if fileExt.lower() in self.imageTypes:
            return True

        return False

    def getSaveFileName(self, url=""):
        #tmp = url.replace('http://', '')
        tmp = url.split('/')
        return str(self.counter) + '#' + tmp[len(tmp)-2] + "#" + tmp[len(tmp)-1]

    def getNextEndless(self, html):
        #http://user.soup.io/since/294388231
        pret = html.split("SOUP.Endless.next_url = '")

        if len(pret) == 2:
            part = pret[1].split('?')[0]
            return part
        return ""

    def debug(self, txt):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S|"+txt))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sd = souperDuper(sys.argv)
        sd.grabAll()
    else:
        print("first parameter must be the user you want to dupe")