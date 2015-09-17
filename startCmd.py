__author__ = 'bison'

import os
import pychromecast
from pychromecast.controllers.youtube import YouTubeController
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

castIndex = {}
for castName in allCastNames:
    cast = pychromecast.get_chromecast(friendly_name=castName)
    allCasts[castName] = cast
    castIndex[castName] = len(castIndex)

if conf.closeCurrentApp:
    for castName, cast in allCasts.items():
        cast.quit_app()

print(castIndex)

while True:
    from os import listdir
    from os.path import isfile, join
    import random
    onlyfiles = [ f for f in listdir(conf.pathWithImages) if isfile(join(conf.pathWithImages,f)) ]
    imgFile = random.choice(onlyfiles)
    for castName, cast in allCasts.items():
        if not castName in conf.blacklist:
            #cast.quit_app()

            castMc = cast.media_controller

            mc = MediaController()
            cast.register_handler(mc)

            if conf.castmode == 'random':
                imgFile = onlyfiles[castIndex[castName]]

            mc.play_media('http://'+ conf.localIp +':8000/'+ imgFile, 'Image/jpg')

    time.sleep(conf.showImageTime)