import datetime
import time
from dateutil import tz
import random

def currentTimeIST(): #returns current time in Indian standard time
    utcTime =  int(datetime.datetime.utcnow().timestamp())
    istTime = utcTime
    return istTime
def createExamId():
    return int(datetime.datetime.utcnow().timestamp())

def stringTimeToISTTimestamp(date, time):
    dateTimeStr = "{} {}".format(date, time)
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz("Asia/Kolkata")
    dateTimeObject = datetime.datetime.strptime(dateTimeStr, '%d/%m/%Y %H:%M')
    dateTimeObjectUTC = dateTimeObject.replace(tzinfo = from_zone)
    dateTimeObjectIST = dateTimeObjectUTC.astimezone(to_zone)
    timestamp = int(datetime.datetime.timestamp(dateTimeObjectIST)) -19800
    return timestamp

def checkIfExamExist(examStartTime, examEndTime):
    currentIST = currentTimeIST()
    if(examStartTime <= currentIST and currentIST <= examEndTime):
        timeLeft = examEndTime - currentIST
        return [True, timeLeft]
    elif (currentIST <= examEndTime):
        return [False, 'Test has not started yet.']
    elif (examStartTime >= currentIST):
        return [False, 'Test has been ended.']



def randomizeQuestions(examData):
    questions = []
    for question in examData['exam']:
        answers = examData['exam'][question]['answers']
        random.shuffle(answers)
        questions.append({
            question: { 'question':  examData['exam'][question]['question'], 
                        'answers': answers
                        }
                    })
    random.shuffle(questions)
    return [examData, questions]

def separateQuestions(examData):
    questions = []
    for question in examData['exam']:
        answers = examData['exam'][question]['answers']
        questions.append({
            question: { 'question':  examData['exam'][question]['question'], 
                        'answers': answers
                        }
                    })
    return [examData, questions]

def computeResults(examData, studentExamData):
    score = 0
    questions = examData['exam']
    for ans in studentExamData:
        if ans in questions:
            answers = questions[ans]['answers']
            for i in answers:
                if studentExamData[ans] == i[0] and i[1] ==True:
                    score+=1
    print("Score computed")
    return score