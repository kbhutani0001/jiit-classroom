import datetime
import random

def currentTimeIST(): #returns current time in Indian standard time
    utcTime =  int(datetime.datetime.utcnow().timestamp())
    istTime = utcTime + 19800
    return istTime
def createExamId():
    return int(datetime.datetime.utcnow().timestamp())

def getTimeStampFromDT(date, time): #dd/mm/yyyy and 24 hour format
    return int(datetime.datetime.now().timestamp()) # temporary

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
        