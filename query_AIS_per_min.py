def generate_data(dateStr='2020-12-09 00:01'):
    import datetime
    import json
    import time
    import urllib.request
    import pytz  # time zones -- install via python -m pip install pytz

    localDir = '/Users/homz/Downloads/'  # this is OUTSIDE the repo
    print('local directory is ', localDir)
    # dateStr = '12/09/2020 00:01'
    timeWindow = 300
    outputDir = 'ais/'

    pst = pytz.timezone('America/Los_Angeles')
    dt = datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M")
    dt = pst.localize(dt)    #localize to time zone
    gmtSec = time.mktime(dt.timetuple())  # convert to gmt seconds since epoch
    a = dateStr.replace(' ', '-')
    dateStr = a.replace('/', '_')   # fix for outputting

    outFilename = 'AIS_at_{}.csv'.format(dateStr)
    outFullFilename = localDir + outputDir + outFilename
    print("output file is ",outFullFilename)


    #build the php request
    url = 'https://m2.protectedseas.net/php/utils/closestApproach.php?ts={}&window={}'.format(gmtSec, timeWindow)

    with urllib.request.urlopen(url) as response:
       html = response.read()

    jsonData = json.loads(html)
    #print("jsonData is of type ", type(jsonData))
    print("jsonData list has length=", len(jsonData))

    dictTyp = type({'a':1})   # defined here to get a class 'dict' object for testing in isinstance  (Likely a better way to do this.)

    # list all the keys
    if len(jsonData) > 0: 
        for key in jsonData[0]:
            print("key= ", key)
        outFileHeader = 'datetime\tgmtSec\tmmsi\tvesselName\taveSpeed\tclosestApproach\tphotoLinks\n'
        with open(outFullFilename, 'w+') as outFile:
            outFile.write(outFileHeader)
            for item in jsonData:
                print('json record')
                print(json.dumps(item, sort_keys=True))  # dump the entire json record
                try:
                    mmsi = item['m2_id'].split('-')[0]
                except:
                    mmsi = 0
        #        if int(mmsi) > 10000:           #  first part of m2_id and radar_track_id is MMSI if one was reported via AIS otherwise a small integer track number
        #            print('mmsi number = {}'.format(mmsi))
        #        print('vessel_name=', item['vessel_name'], 'min and max speeds=',item['minimum_speed'], item['maximum_speed'])

                try:
                    photos = item['photos']
                except:
                    photos = []
            #            for photo in photos:
            #                print('photos= ', photo['key'])
                if int(mmsi) > 1000:
                    aveSpeed = (float(item['minimum_speed']) + float(item['maximum_speed'])) / 2
                    if photos != []:
                        outDataline = '{}\t{}\t{}\t{:0.1f}\t{:0.1f}\t{:0.1f}\t{}\n'.format(dateStr,gmtSec,mmsi,aveSpeed,
                                                                            float(item['closest_approach']),
                                                                            float(item['closest_approach']), photos[0]['key'])
                    else:
                        outDataline = '{}\t{}\t{}\t{:0.1f}\t{:0.1f}\t{:0.1f}\t{}\n'.format(dateStr, gmtSec, mmsi, aveSpeed,
                                                                            float(item['closest_approach']),
                                                                            float(item['closest_approach']), 'no photo')
                    outFile.write(outDataline)


            #
            outFile.close()

import time
import datetime
import pytz
datetime_list = []
start = datetime.datetime(2020, 12, 9)
pst = pytz.timezone('America/Los_Angeles')
for i in range(1440):
    dt = str(datetime.datetime(2020, 12, 9) + i * datetime.timedelta(seconds=60))[:-3]
    datetime_list.append(dt)

for i, d in enumerate(datetime_list):
    print(i)
    generate_data(d)

