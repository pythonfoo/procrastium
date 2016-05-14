__author__ = 'bison'

import os
import pychromecast
from pychromecast.controllers.media import MediaController
import time

if os.path.isfile('conf_local.py'):
    import conf_local as conf
else:
    import conf

#import subprocess
#proc = subprocess.Popen(['./startHttpServer.sh', conf.pathWithImages])

#tmp = input('wait')
#exit()

print('start discovery')
allCastNames = pychromecast.get_chromecasts_as_dict().keys()
allCasts = {}
print('end discovery')

if len(allCastNames) == 0:
    raise Exception('NO CHROMECASTS FOUND!')

castIndex = {}
for castName in allCastNames:
    cast = pychromecast.get_chromecast(friendly_name=castName)
    allCasts[castName] = cast
    castIndex[castName] = len(castIndex)

if conf.closeCurrentApp:
    for castName, cast in allCasts.items():
        cast.quit_app()

print(castIndex)

onlyfiles = []

soup = None
soupNext = None
if conf.imageSource == 'local':
    onlyfiles = [ f for f in os.listdir(conf.pathWithImages) if os.path.isfile(os.path.join(conf.pathWithImages,f)) ]
elif conf.imageSource == 'soup':
    import souper
    soup = souper.souperDuper(conf.soup)
    soupNext = soup.grabPart()

while True:
    if soupNext != None:
        soupNext.__next__()
        onlyfiles = list(soup.knownUrls.keys())

    from os import listdir
    from os.path import isfile, join
    import random

    imgFile = random.choice(onlyfiles)
    for castName, cast in allCasts.items():
        if not castName in conf.blacklist:
            castMc = cast.media_controller

            mc = MediaController()
            cast.register_handler(mc)

            if conf.castmode == 'different':
                imgFile = random.choice(onlyfiles)

            if conf.imageSource == 'soup':
                mc.play_media(imgFile, 'Image/jpg')
            else:
                mc.play_media('http://'+ conf.localIp +':8000/'+ imgFile, 'Image/jpg')

    time.sleep(conf.showImageTime)
