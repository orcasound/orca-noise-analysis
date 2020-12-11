"""
Example of downloading and decoding one of Virgil's M2 json requests via:
 https://m2.protectedseas.net/php/utils/closestApproach.php? with various parameters after the ?

Virgil's documentation via e_mail:
End Point:
https://m2.protectedseas.net/php/utils/closestApproach.php

Defaults:
- +- 10 minutes from Current Time
- 15km max distance
- Radar and AIS targets
- Targets with and without photos

Optional Arguments (as URL parameters):
ts = <unix timestamp>, pick the center time to search
example: https://m2.protectedseas.net/php/utils/closestApproach.php?ts=1607104728

window = <seconds>, change the time window before / after ts to search
example: https://m2.protectedseas.net/php/utils/closestApproach.php?ts=16071047281Vr2pHn9vo300

source = radar OR ais, only return radar or ais targets
example: https://m2.protectedseas.net/php/utils/closestApproach.php?ts=1607104728&ais

photos = 1 , only return targets with photos IN THE selected time window
example: https://m2.protectedseas.net/php/utils/closestApproach.php?ts=1607104728&window=300&photos=1

Output (json):
- m2_id = human readable id that is the same as displayed in the M2 cloud viewer
- server_track_id = internal M2 unique track id
- radar_track_id = radar track id (0 - 30 for orcasound for radar, MMSI number for AIS)
- closest_approach = minimum distance in km from radar to target in time window
- tracked_distance = total tracked distance in km
- minimum_speed = min speed in kts within time window
- maximum_speed = max speed in kts within time window
- average_heading = circular mean of heading (-180 - 180) in True North
- processed = 0, track is still active, processed = 1, track no longer active
- source = radar or ais

IF a target has photos within the time window, there is a photos array with:
- timestamp = unix timestamp of the photo
- key = URL to get the JPG

Keys only used with AIS vessels:
- vessel_name = Vessel Name if AIS
- association_strength = how many correspondences to a radar detection
- associated_target_id = server_target_id of corresponded radar target


Caveats:
- Only works with orcasound M2 site
- Only returns photos for targets that are no longer being actively tracked
- Photo links assume only 2020 data and not prior year(s)

- Virgil


Virgil Zetterlind
Director, Protected Seas
Anthropocene Institute

"""
import datetime
import json
import time
import urllib.request
import pytz  # time zones -- install via python -m pip install pytz
import os

localDir = os.getcwd()
print('local directory is ', localDir)
dateStr = '12/09/2020 12:00'
timeWindow = 300
outputDir = '/M2_output/'


pst = pytz.timezone('America/Los_Angeles')
dt = datetime.datetime.strptime(dateStr, "%m/%d/%Y %H:%M")
dt = pst.localize(dt)    #localize to time zone
gmtSec = time.mktime(dt.timetuple())  # convert to gmt seconds since epoch
a = dateStr.replace(' ', '-')
dateStr = a.replace('/', '_')   # fix for outputting

outFilename = 'AIS_at_{}.csv'.format(dateStr)
outFullFilename = localDir + outputDir + outFilename
outFile = open(outFullFilename, 'w')
#build the php request
url = 'https://m2.protectedseas.net/php/utils/closestApproach.php?ts={}&window={}'.format(gmtSec, timeWindow)

with urllib.request.urlopen(url) as response:
   html = response.read()

jsonData = json.loads(html)
#print("jsonData is of type ", type(jsonData))
print("jsonData list has length=", len(jsonData))

dictTyp = type({'a':1})   # defined here to get a class 'dict' object for testing in isinstance  (Likely a better way to do this.)

# list all the keys
for key in jsonData[0]:
    print("key= ", key)
outFileHeader = 'datetime\tgmtSec\tmmsi\tvesselName\taveSpeed\tclosestApproach\tphotoLinks\n'
outFile.write(outFileHeader)
for item in jsonData:
    if isinstance(item, dictTyp):   # likely don't need this check, but so well.
        try:
#            print('m2_id=', item['m2_id'])  # print a few key's values, just for fun
            mmsi = 0
            try:
                mmsi = item['m2_id'].split('-')[0]
#                if int(mmsi) > 10000:           #  first part of m2_id and radar_track_id is MMSI if one was reported via AIS otherwise a small integer track number
#                    print('mmsi number = {}'.format(mmsi))
#                print('vessel_name=', item['vessel_name'], 'min and max speeds=',item['minimum_speed'], item['maximum_speed'])

            except:
                []
            try:
                photos = item['photos']
            except:
                photos = []
#            for photo in photos:
#                print('photos= ', photo['key'])
            if int(mmsi) > 1000:
                aveSpeed = (float(item['minimum_speed']) + float(item['maximum_speed'])) / 2
                if photos != []:
                    outDataline = dateStr + '\t' + str(gmtSec) + '\t' + mmsi + '\t' + item['vessel_name'] + '\t' + str(
                        aveSpeed) + '\t' + item['closest_approach'] + '\t' + photos[0]['key'] + '\n'
                else:
                    outDataline = dateStr + '\t' + str(gmtSec) + '\t' + mmsi + '\t' + item['vessel_name'] + '\t' + str(
                        aveSpeed) + '\t' + item['closest_approach'] + '\t' + 'no Photos' + '\n'
                print('before', outDataline)
                outFile.write(outDataline)
                print('after', outDataline)
        except:
            input('????')
#    print('json record')
#    print(json.dumps(item, sort_keys=True))  # dump the entire json record
    outFile.close()




