import pymongo
import config


def markAttendance(client, classroomId, rollNo, loginTime):
  try:
    db = client.jiitclassroom
    col = db["attendance"]
    data = col.find({'classroomId': classroomId})
    if(data.count()): #classroom exists
      currentAttendance = data[0]["attendance"].copy()
      if(not rollNo in currentAttendance.keys()): #if logging in first time
        print("Updating Attendance")
        currentAttendance[rollNo] = loginTime
        updatedData = { "$set": {
          "classroomId": classroomId,
          "attendance": currentAttendance
          }
        }
        col.update_one(data[0],updatedData)
    else: #if class doesnt exists 
      data = {"classroomId": classroomId,
        "attendance": {
        rollNo: loginTime
        }
      }
      col.insert_one(data)
  except:
    None


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
  if(col.find_one({'id': facultyId, 'password': facultyPassword})):
    return True
  return False

