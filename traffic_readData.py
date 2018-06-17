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
              '22':data_22,'23':data_23,'24':data_24}
    
    # 'lineOfData' is a 'trafficInfo' struture, which is define above
    processLine = lambda lineOfData:dateId.get(str(lineOfData['date'].day)).append(lineOfData)
    
    list(map(processLine,detectorValues))
    return [data_18,data_19,data_20,data_21,data_22,data_23,data_24]

'''
@brief   : To remove the duplicate datas
@variable: the whole series of data read by a single dector, e.g.'NHNX39_1'
@return  : None
@others  : 

def removeRedundancy(lineOfData):
'''
    
list(map(readSheet,allSheets))

# sort all the datas stored in those user-defined lists in the order of time
for detectors in groupId.values():
    detectors.sort(key = lambda lineOfData:lineOfData['date'].timestamp())


# distribute the datas into an array of each day, that is to say, now e.g. NHNX39_1 is an list
# of seven lists of the trafficInfo on one single day
NHNX39_1    = detectorTiming(NHNX39_1)
NHNX39_2    = detectorTiming(NHNX39_2) 
NHNX40_1    = detectorTiming(NHNX40_1)
NHNX40_2    = detectorTiming(NHNX40_2)
NHNX41_1    = detectorTiming(NHNX41_1)
NHNX41_2    = detectorTiming(NHNX41_2)
NHWN_NI_1_1 = detectorTiming(NHWN_NI_1_1)
NHWN_NI_1_2 = detectorTiming(NHWN_NI_1_2)
NHWN_NI_2_1 = detectorTiming(NHWN_NI_2_1)
NHWN_NI_2_2 = detectorTiming(NHWN_NI_2_2)    
NHZP_NO_1_1 = detectorTiming(NHZP_NO_1_1)   
NHZP_NO_1_2 = detectorTiming(NHZP_NO_1_2)
NHZP_NO_2_1 = detectorTiming(NHZP_NO_2_1)
NHZP_NO_2_2 = detectorTiming(NHZP_NO_2_2)

