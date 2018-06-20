# -*- coding: utf-8 -*-
"""
@author: Shine Wong
@brief:  This document is used to read and preprocess the data of traffic
         condition.
         The data processed will be presented in the order of time of 
         each detector of each day.
         For example, a single array of the data consists of 'VOLUME' 'SPEED'
         'OCCUPY' on 4/18/2010 obtained from detector NHNX39(1) in the order
         of time
"""
# imports
import xlrd
from datetime import datetime,timedelta

# read data & preprocess
fileDir = r'data.xls'
allSheets = xlrd.open_workbook(fileDir).sheets()
# exclude the last sheet
allSheets = allSheets[:-1]

# variable initialization
NHNX39_1 = []
NHNX39_2 = []  
NHNX40_1 = []
NHNX40_2 = []
NHNX41_1 = []
NHNX41_2 = []

NHWN_NI_1_1 = []
NHWN_NI_1_2 = []
NHWN_NI_2_1 = []
NHWN_NI_2_2 = []    
NHZP_NO_1_1 = []   
NHZP_NO_1_2 = [] 
NHZP_NO_2_1 = []
NHZP_NO_2_2 = [] 

# useless data
NHWX41_1 = []
NHWX41_2 = []
NHWX41_3 = []

# Due to 'groupId' dict, we can operate the corresponding array and store data,
# which is also a dict type with three leading traffic information, to that array.
groupId = {'NHNX39(1)      ':NHNX39_1,'NHNX39(2)      ':NHNX39_2,
           'NHNX40(1)      ':NHNX40_1,'NHNX40(2)      ':NHNX40_2,
           'NHNX41(1)      ':NHNX41_1,'NHNX41(2)      ':NHNX41_2,
           'NHWN-NI-1(1)   ':NHWN_NI_1_1,'NHWN-NI-1(2)   ':NHWN_NI_1_2,
           'NHWN-NI-2(1)   ':NHWN_NI_2_1,'NHWN-NI-2(2)   ':NHWN_NI_2_2,
           'NHZP-NO-1(1)   ':NHZP_NO_1_1,'NHZP-NO-1(2)   ':NHZP_NO_1_2,
           'NHZP-NO-2(1)   ':NHZP_NO_2_1,'NHZP-NO-2(2)   ':NHZP_NO_2_2,
           'NHWX41(3)      ':NHWX41_3,'NHWX41(2)      ':NHWX41_2,
           'NHWX41(1)      ':NHWX41_1
           }

'''
@brief   : To read a line of data and distribute it to the proper array
@variable: an array of a line of data, for example:sheet_1.row_values(1)
@return  : None
@others  : This function is to be called in map() in order to process a bunch
            of datas
'''
def readLine(dataLine):
    # obtain the ID and traffic infomation of current line of data
    currentId = dataLine[1].value
    # the raw data which stores date information  
    rawDate = dataLine[2].value
    # processed date information in 'datetime' format
    date = xlrd.xldate.xldate_as_datetime(rawDate,1)-timedelta(days = 1)
    
    trafficInfo = {'volume':dataLine[3].value,'speed':dataLine[4].value,
                   'occupy':dataLine[5].value,'date': date}
    
    # quote the corresponding array directly according to the detector id
    groupId.get(currentId).append(trafficInfo)
    
'''
@brief   : To read a sheet of data and store each line to a proper array
@variable: a sheet of data, for example: allSheets.sheets()[0]
@return  : None
@others  : This function is to be called in map() in order to process several
           sheets and it quote 'readLine()' inside
'''
def readSheet(thisSheet):
    # Here 'values' is a generator of all the datas in thisSheet
    values = thisSheet.get_rows()
    # exclude the first row
    next(values)
    
    list(map(readLine,values))
    
'''
@brief   : To separate the date read by each detector in the order of date
@variable: the whole series of data read by a single dector, e.g.'NHNX39_1'
@return  : None
@others  : 
'''
def detectorTiming(detectorValues):
    data_18,data_19,data_20,data_21,data_22,data_23,data_24 = [],[],[],[],[],[],[]
    # the same principle as 'groupId', however, this dict is used to separate the 
    # traffic data by date
    dateId = {'18':data_18,'19':data_19,'20':data_20,'21':data_21,
              '22':data_22,'23':data_23,'24':data_24
              }
    
    # 'lineOfData' is a 'trafficInfo' struture, which is defined above
    processLine = lambda lineOfData:dateId.get(str(lineOfData['date'].day)).append(lineOfData)
    
    list(map(processLine,detectorValues))
    return [data_18,data_19,data_20,data_21,data_22,data_23,data_24]

'''
@brief   : To remove the duplicate datas
@variable: the whole series of data read by a single dector, e.g.'NHNX39_1', _ordered_
@return  : None
@others  : this function should be called on the basis of sorting
'''
# This version of removeRedundancy would operate around 3 minutes for each list like NHNX39_1.......
def removeRedundancy(detectorValues):
    for element in detectorValues[:-1]:# remove the last element        
        # locate the real-time index of the current element
        index = detectorValues.index(element)
        print(index)
        # prevent index overflow due to removing some elements
        if index == len(detectorValues)-1:
            break
        nextElement = detectorValues[index+1]
        
        currentTime = element['date']
        nextTime    = nextElement['date']
        if currentTime == nextTime:
            detectorValues.pop(index)

# Well, this version using 'map' instead of 'for' loop operate two times quicker than the first one. 
# Still, it would take one minute and a half before it finishes processing.
def removeRedundance(detectorValues):
    def processLine(element):
        index =  detectorValues.index(element)  
        print(index)
        # prevent index overflow due to removing some elements
        if index >= len(detectorValues)-1:
            return
        nextElement = detectorValues[index+1]
        
        currentTime = element['date']
        nextTime    = nextElement['date']
        if currentTime == nextTime:
            detectorValues.pop(index)
    
    list(map(processLine,detectorValues))

# The ultimate version of 'removeRedundancy', it operates fast and the result is convincing.
# However, in order to settle various problems and bugs, the programme structure is somewhat unreadable
def removeRedund(detectorValues):
    listLength = len(detectorValues)
    for index in range(1,listLength-1):
        # prevent index overflow
        if index >= len(detectorValues):
            break
        
        prevTime    = detectorValues[index-1]['date']
        currentTime = detectorValues[index]['date']
        if index < len(detectorValues)-1:
            nextTime    = detectorValues[index+1]['date']
            
            if currentTime == nextTime:
                detectorValues.pop(index) 
                
        if currentTime == prevTime:
             detectorValues.pop(index)
    
'''
@brief   : To fix the missing data using lineal interpolation
@variable: the whole series of data read by a single dector, e.g.'NHNX39_1', _ordered_
@return  : None
@others  : this function should be called on the basis of sorting
'''
DATANUM = 4320*7
def linearInterp(detectorValues):
    for index in range(DATANUM-1):
        currData = detectorValues[index]
        nextData = detectorValues[index+1]
        currTimestamp = currData['date'].timestamp()
        nextTimestamp = nextData['date'].timestamp()
        
        if currTimestamp == nextTimestamp - 20:
            continue
        
        missingNum = (nextTimestamp-currTimestamp-20)/20
        # construct a new trafficInfo for inserting       
        newDate   = datetime.fromtimestamp(currTimestamp+20)
        newVolume = (nextData['volume']-currData['volume'])/(missingNum+1)+currData['volume']
        newSpeed  = (nextData['speed'] -currData['speed']) /(missingNum+1)+currData['speed']
        newOccupy = (nextData['occupy']-currData['occupy'])/(missingNum+1)+currData['occupy']
        trafficInfo = {'volume':newVolume, 'speed':newSpeed,
                       'occupy':newOccupy, 'date' : newDate}
        
        # insert constrcuted trafficInfo
        detectorValues.insert(index+1,trafficInfo)
        
'''
@brief   : To fix the datas read as 0, by taking the average value of the preceding and following data
@variable: a single dimension of data read by a single dector, e.g.'NHNX39_1[:]['volume']', _ordered_
@return  : None
@others  : this function should be called on the basis of sorting as well as linear interpolation
'''
def fixzero(oneTrafficInfo):
    return    [(oneTrafficInfo[index-1]+oneTrafficInfo[index+1])/2 
              if oneTrafficInfo[index]==0 and index > 1260 and index < 3420
              else oneTrafficInfo[index]
              for index in range(len(oneTrafficInfo)) ]
    
''' 
@brief   : To fix the datas read as 0, by taking the average value of the preceding and following data
@variable: the whole series of data read by a single dector on a single day, e.g.'NHNX39_1[0]', _ordered_
@return  : None
@others  : this function should be called on the basis of sorting as well as linear interpolation
           it calls fixzero() inside
'''
def fixZero(detectorValues):
    # obtain one-dimensional traffic infomation
    occupy = [lineOfData['occupy'] for lineOfData in detectorValues]
    speed  = [lineOfData['speed'] for lineOfData in detectorValues]
    volume = [lineOfData['volume'] for lineOfData in detectorValues]
    #date   = [lineOfData['date'] for lineOfData in detectorValues]
    
    # fix zero data on rush hours from 7:00 to 19:00
    occupy = fixzero(occupy)
    speed  = fixzero(speed)
    volume = fixzero(volume)
    
    # reconstruct data structure
    detectorDict = {}
    detectorDict['volume'] = volume
    detectorDict['speed']  = speed
    detectorDict['occupy'] = occupy
    #detectorDict['date']   = date
    
    return detectorDict

'''main program starts eventually.......'''

list(map(readSheet,allSheets))
# remove those useless datas
groupId.pop('NHWX41(3)      ')
groupId.pop('NHWX41(2)      ')
groupId.pop('NHWX41(1)      ')


# sort all the datas stored in those user-defined lists in the order of time, for loop version
'''
for detectors in groupId.values():
    detectors.sort(key = lambda lineOfData:lineOfData['date'].timestamp())
'''
# another solution without using for loop
list(map(lambda detector:detector.sort(key = lambda lineOfData:lineOfData['date'].timestamp()),groupId.values()))

# remove the duplicate datas in these lists
list(map(removeRedund,groupId.values()))

#fix the missing data using lineal interpolation
list(map(linearInterp,groupId.values()))
# distribute the datas into an array of each day, that is to say, now e.g. NHNX39_1 is an list
# of seven lists of the trafficInfo on one single day


NHNX39_1    = list(map(fixZero,detectorTiming(NHNX39_1)))
NHNX39_2    = list(map(fixZero,detectorTiming(NHNX39_2)))
NHNX40_1    = list(map(fixZero,detectorTiming(NHNX40_1)))
NHNX40_2    = list(map(fixZero,detectorTiming(NHNX40_2)))
NHNX41_1    = list(map(fixZero,detectorTiming(NHNX41_1)))
NHNX41_2    = list(map(fixZero,detectorTiming(NHNX41_2)))
NHWN_NI_1_1 = list(map(fixZero,detectorTiming(NHWN_NI_1_1)))
NHWN_NI_1_2 = list(map(fixZero,detectorTiming(NHWN_NI_1_2)))
NHWN_NI_2_1 = list(map(fixZero,detectorTiming(NHWN_NI_2_1)))
NHWN_NI_2_2 = list(map(fixZero,detectorTiming(NHWN_NI_2_2)))    
NHZP_NO_1_1 = list(map(fixZero,detectorTiming(NHZP_NO_1_1)))   
NHZP_NO_1_2 = list(map(fixZero,detectorTiming(NHZP_NO_1_2)))
NHZP_NO_2_1 = list(map(fixZero,detectorTiming(NHZP_NO_2_1)))
NHZP_NO_2_2 = list(map(fixZero,detectorTiming(NHZP_NO_2_2)))

'''
import matplotlib.pyplot as plt
import numpy as np
time = np.arange(len(NHNX39_1[0]))/3 # minute
occupy = [lineOfData['occupy'] for lineOfData in NHNX39_1[0]]
plt.plot(time,occupy)
'''