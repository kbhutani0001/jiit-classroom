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

def addMeeting(client, facultyId, classroomId):
  db = client.jiitclassroom
  col = db["facultyLogin"]
  data = col.find_one({'id': facultyId})
  if(data):
    if "meetings" in data:
      meetings = data["meetings"].copy()
      if(str(classroomId) in meetings):
        return [False, "Meeting with same ID already Exists"]
      meetings.append(str(classroomId))
      updatedData = { "$set": {
          "id": data["id"],
          "meetings": meetings,
          "name": data["name"],
          "password": data["password"]
        }
      }
      col.update_one(data,updatedData)
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

def createAccount(client, facultyName, facultyId, facultyPassword):
  db = client.jiitclassroom
  col = db["facultyLogin"]
  if(col.find_one({'id': facultyId})):
    return False
  else:
    data = {"id": facultyId,
            "meetings": [],
            "name": facultyName,
            "password": facultyPassword
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
    print(name)
    col.insert_one({"name": name})