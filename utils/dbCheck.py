import pymongo
import config


def markAttendance(client, classroomId, rollNo, studentName, loginTime):
  try:
    print("Marking attendance for " + classroomId)
    db = client.jiitclassroom
    col = db["attendance"]
    data = col.find({'classroomId': classroomId})
    if(data.count()): #classroom exists
      currentAttendance = data[0]["attendance"].copy()
      if(not rollNo in currentAttendance.keys()): #if logging in first time
        print("Updating Attendance")
        currentAttendance[rollNo] = [studentName,loginTime]
        updatedData = { "$set": {
          "classroomId": classroomId,
          "attendance": currentAttendance
          }
        }
        col.update_one(data[0],updatedData)
    else: #if class doesnt exists 
      print("Creating class and marking attendance for " + classroomId)
      data = {"classroomId": classroomId,
        "attendance": {
        rollNo: [studentName,loginTime]
        }
      }
      col.insert_one(data)
  except Exception as e:
    print("Could not mark attendance")
    print(e)
    None

def addMeeting(client, facultyId, classroomId, meetingPassword):
  db = client.jiitclassroom
  col = db["facultyLogin"]
  data = col.find_one({'id': facultyId})
  if(data):
    if "meetings" in data:
      meetings = data["meetings"].copy()
      meetingPasswordData = data["meetingPassword"].copy()
      meetingPasswordData[str(classroomId)] = meetingPassword      
      if(str(classroomId) in meetings):
        return [False, "Meeting with same ID already Exists"]
      meetings.append(str(classroomId))
      updatedData = { "$set": {
          "id": data["id"],
          "meetings": meetings,
          "meetingPassword": meetingPasswordData,
          "name": data["name"],
          "password": data["password"]
        }
      }
      col.update_one(data,updatedData)
      meetingPasswordCol = db["meetingPassword"]
      meetingPasswordData = {"classroomId": str(classroomId), "meetingPassword": meetingPassword}
      meetingPasswordCol.insert_one(meetingPasswordData)
    return [True]
  else:
    return [False, "Some error occurred. Couldn't create meeting."]

def getAllMeetingsOfFaculty(client, facultyId):
  db = client.jiitclassroom
  col = db["facultyLogin"]
  data = col.find_one({'id': facultyId})
  if(data):
    return data["meetings"]
  else:
    return False

def getAttendance(client, classroomId):
  db = client.jiitclassroom
  col = db["attendance"]
  meetingData = col.find_one({'classroomId': classroomId})
  if(meetingData):
    return [True, meetingData["attendance"]]
  return [False]

def checkFacultyLogin(client, facultyId, facultyPassword):
  db = client.jiitclassroom
  col = db["facultyLogin"]
  data = col.find_one({'id': facultyId, 'password': facultyPassword})
  if(data):
    return [True, data]
  return [False]

def checkStudentLogin(client, rollNo, password):
  db = client.jiitclassroom
  col = db["studentLogin"]
  data = col.find_one({'rollNo': rollNo, 'password': password})
  if(data):
    return [True, data['name']]
  return [False]

def createAccount(client, facultyName, facultyId, facultyPassword):
  db = client.jiitclassroom
  col = db["facultyLogin"]
  if(col.find_one({'id': facultyId})):
    return False
  else:
    data = {"id": facultyId,
            "meetings": [],
            "exams": [],
            "meetingPassword": {},
            "name": facultyName,
            "password": facultyPassword
      }
    col.insert_one(data)
    return True

def createStudentAccount(client, studentName, studentRollNo, studentPassword):
  db = client.jiitclassroom
  col = db["studentLogin"]
  if(col.find_one({'rollNo': studentRollNo})):
    return False
  else:
    data = {"rollNo": studentRollNo,
            "name": studentName,
            "password": studentPassword
      }
    col.insert_one(data)
    return True

def checkIfFacultyExists(client, facultyId):
  db = client.jiitclassroom
  col = db["facultyLogin"]
  data = col.find_one({'id': facultyId})
  if(data):
    return True
  else:
    return False


def getSurvey(client, facultyId):
  db = client.jiitclassroom
  col = db["facultyLogin"]
  data = col.find_one({'id': facultyId})
  if 'survey' in data:
    if(data['survey'] == False):
      return False
    else:
      return True
  return False

def setSurvey(client, facultyId):
  db = client.jiitclassroom
  col = db["facultyLogin"]
  data = col.find_one({'id': facultyId})
  if(data):
    updatedData = { "$set": {
        "id": data["id"],
        "meetings": data["meetings"],
        "name": data["name"],
        "password": data["password"],
        "survey": True
      }
    }
    col.update_one(data,updatedData)
    return True
  else:
    return False

def setFeatureOpen(client, name):
  db = client.jiitclassroom
  col = db["featureOpen"]
  data = col.find_one({"name" : name})
  if not data:
    col.insert_one({"name": name})
  
def getMeetingPassword(client, classroomId):
  db = client.jiitclassroom
  col = db["meetingPassword"]
  data = col.find_one({"classroomId": classroomId})
  if(data):
    return data["meetingPassword"]
  return ""

def getExamDetails(client, examId):
  db = client.jiitclassroom
  col = db["examDetails"]
  data = col.find_one({"examId": examId})
  if(data):
    return [True, data]
  return [False, "Exam ID Doesn't Exist"]

def addExam(client, facultyId, examData):
  db = client.jiitclassroom
  col = db["facultyLogin"]
  data = col.find_one({'id': facultyId})
  if(data):
    exams = data["exams"].copy()     
    if(str(examData["examId"]) in data["exams"]):
      return [False, "Exam with same Exam ID already exists"]
    exams.append(str(examData["examId"]))
    updatedData = { "$set": {
        "id": data["id"],
        "exams": exams,
        "meetings": data["meetings"],
        "meetingPassword": data["meetingPassword"],
        "name": data["name"],
        "password": data["password"]
        }
      }
    col.update_one(data,updatedData)
    getExamDetailsDb = db["examDetails"]
    getExamDetailsDb.insert_one(examData)
    examResultsDb = db["examResults"]
    examResultsDb.insert_one({
      'examId': examData['examId'],
      'examResults': {}
    })
    return [True]
  else:
    return [False, "Some error occurred. Couldn't create Exam."]

def getExamResults(client, examId):
  db = client.jiitclassroom
  col = db["examResults"]
  examIdData = col.find_one({'examId': examId})
  examIdResults = examIdData['examResults']
  return examIdResults

def getExamTable(client, facultyId):
  db = client.jiitclassroom
  col = db["facultyLogin"]
  data = col.find_one({'id': facultyId})
  if(data):      
    tableData = []
    if "exams" in data:
      exams = data["exams"]
      for examId in exams:
        try:
          examData = getExamDetails(client, examId)[1]
          givenBy = getExamResults(client, examId)
          tableData.append({"examId": examId,
          "examName": examData["examName"],
          "examDate": examData["examDate"],
          "givenBy": len(givenBy)
          })
        except Exception as e:
          print(e)
          pass
    return tableData

def submitExam(client, studentExamData, examScore):
  rollNo = studentExamData['rollNo']
  studentName = studentExamData['studentName']
  examId = studentExamData['examId']
  del studentExamData['rollNo']
  del studentExamData['studentName']
  del studentExamData['examId']
  data = {
    'studentName': studentName,
    'examData': studentExamData,
    'examScore': examScore
  }
  db = client.jiitclassroom
  col = db["examResults"]
  examIdData = col.find_one({'examId': examId})
  examIdResults = examIdData['examResults']
  newExamIdResults = examIdResults.copy()
  newExamIdResults[rollNo] = data
  updatedData = { "$set": {
                  "examId": examId,
                  "examResults": newExamIdResults
        }
      }
  col.update_one(examIdData,updatedData)
  return [True]