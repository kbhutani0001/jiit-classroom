import datetime

def currentTimeIST(): #returns current time in Indian standard time
    utcTime =  int(datetime.datetime.utcnow().timestamp())
    istTime = utcTime + 19800
    return istTime
def createExamId():
    return int(datetime.datetime.utcnow().timestamp())
def getTimeStampFromDT(date, time): #dd/mm/yyyy and 24 hour format
    return int(datetime.datetime.now().timestamp()) # temporary