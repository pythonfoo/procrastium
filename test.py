__author__ = 'bison'

print('FOO')
import souper
soup = souper.souperDuper('bison')
soupNext = soup.grabPart()
soupNext.__next__()
exit()

import pychromecast
from pychromecast.controllers.youtube import YouTubeController
from pychromecast.controllers.media import MediaController
import time

myIp = '172.22.27.204' #'172.22.27.48'

print('start discovery')
allCastNames = pychromecast.get_chromecasts_as_dict().keys()
allCasts = {}
video="C_XyuvPE9t4"
print('end discovery')

castIndex = {}
for castName in allCastNames:
    cast = pychromecast.get_chromecast(friendly_name=castName)
    allCasts[castName] = cast
    castIndex[castName] = len(castIndex)

for castName, cast in allCasts.items():
    #cast.quit_app()
    pass

print(castIndex)

while True:
    mypath = '/home/bison/Dropbox/Photos/Motivation'
    from os import listdir
    from os.path import isfile, join
    import random
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    imgFile = random.choice(onlyfiles)
    for castName, cast in allCasts.items():
        if castName != 'Plantcastf':
            #cast.quit_app()

            #cast.quit_app()
            #print(cast.device)

            castMc = cast.media_controller
            print(castMc.status)

            mc = MediaController()
            cast.register_handler(mc)

            imgFile = onlyfiles[castIndex[castName]]
            castIndex[castName] += 1
            print(castName + ' http://'+ myIp +':8000/'+ imgFile)
            mc.play_media('http://'+ myIp +':8000/'+ imgFile, 'Image/jpg')
            #mc.play_media('http://172.22.27.48:8000/TMP/my whole brain is crying - panic - DuBMDLP.gif', 'Image/gif')
            #mc.play_media('http://172.22.27.48:8000/TMP/stupid%20human%20race%20-%20tumblr_mfoumwtO6I1ryw1t1o1_500.gif', 'Image/gif')
            #mc.play_media('https://pbs.twimg.com/media/CNbowwpWIAEe1Sm.jpg', 'Image/jpeg')

            #mi = MediaImage('http://asset-2.soupcdn.com/asset/12903/9698_26b1.jpeg', 100, 100)
            #mi.url
            #mc.play()

            #yt = YouTubeController()
            #cast.register_handler(yt)
            #yt.play_video(video)
    time.sleep(8.8)