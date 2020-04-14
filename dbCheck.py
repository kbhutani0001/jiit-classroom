import pymongo
import config

def getAttendance(classroomId):
  print("Classroom ID  ", classroomId)
  client = pymongo.MongoClient(config.mlabURI, connectTimeoutMS=30000)
  db = client.jiitclassroom
  col = db["attendance"]
  meetingData = col.find_one({'classroomId': classroomId})
  if(meetingData):
    return [True, meetingData["attendance"]]
  return [False]

def checkFacultyLogin(facultyId, facultyPassword):
  client = pymongo.MongoClient(config.mlabURI, connectTimeoutMS=30000)
  db = client.jiitclassroom
  col = db["facultyLogin"]
  if(col.find_one({'id': facultyId, 'password': facultyPassword})):
    return True
  return False

