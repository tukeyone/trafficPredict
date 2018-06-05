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
    trafficInfo = {'volume':dataLine[3].value,'speed':dataLine[4].value,
                   'occupy':dataLine[5].value}
    
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
    # Giving that 'thisSheet' is not Iterable, first extract the data 
    # in an array 'values' and restore it
    values = thisSheet.get_rows()
    # exclude the first row
    next(values)
    
    list(map(readLine,values))
    
list(map(readSheet,allSheets))