from flask import (
  Flask,
  flash,
  Response,
  render_template,
  request,
  redirect,
  url_for,
  send_from_directory,
  jsonify,
  abort,
  session,
  g
  )
import os
from checkWebkiosk import checkWebkioskLogin
from dbCheck import (
  getAttendance,
  checkFacultyLogin,
  markAttendance,
  createAccount
  )
import pymongo
import config


app = Flask(__name__)
app.secret_key = "jiit128jiitclassroomforonlineclasses"

client = pymongo.MongoClient(config.mlabURI, connectTimeoutMS=50000)

@app.route('/', methods=['GET'])
def home():
  return render_template('index.html')


@app.route('/join/', methods=['GET'])
def join():
  return render_template('join.html') 

@app.route('/create/', methods=['GET', 'POST'])
def create():
  if request.method == 'GET':
    return render_template('createLogin.html')
  else:
    facultyId = request.form['facultyId']
    facultyPassword = request.form['facultyPassword']
    if(checkFacultyLogin(client, facultyId, facultyPassword)):
      return render_template('create.html')
    else:
      flash('Wrong ID or Password, please try again.')
      return render_template('createLogin.html')


@app.route('/signup/faculty/<inviteCode>', methods=['GET', 'POST'])
def facultySignup(inviteCode):
  if(len(inviteCode)==8 and (int(inviteCode[2:4]) + int(inviteCode[4:6]))==128):
    if request.method == 'GET':
      return render_template('facultySignup.html', inviteCode=inviteCode)
    elif request.method == 'POST':
      facultyName = request.form['facultyName']
      facultyId = request.form['facultyId']
      facultyPassword = request.form['facultyPassword']
      if(createAccount(client, facultyName, facultyId, facultyPassword)):
        return "Account Create Successfully. Redirecting to Home Page. <script> setTimeout(function() { window.location = '/'}, 2000);</script>"
      else:
        return "Email ID already Exists. Redirecting Back. <script> setTimeout(function() { window.history.back()}, 2000);</script>"
  else:
    return "Invalid URL. Invite code does not exist."


@app.route('/join/<classroomId>', methods=['GET', 'POST'])
def joinClass(classroomId):
  if request.method == 'GET':
    return render_template("login.html", classroomId=classroomId)
  else:
    rollNo = request.form['rollNo']
    password = request.form['password']
    dob = request.form['dob']
    loginTime = request.form['currentTime']
    dob = dob.split('-')[2] + '-' + dob.split('-')[1] + '-' + dob.split('-')[0]
    webkioskLogin = checkWebkioskLogin(rollNo, dob, password)
    if(webkioskLogin[0]):
      studentName = webkioskLogin[1]
      markAttendance(client, classroomId, rollNo, studentName, loginTime)
      joinName = rollNo + '_' + studentName.replace(' ', '_')
      API_KEY = 'bbggBIchTf2B67Oue2QgFg'
      convertedClassroomId = int(classroomId) - 620128
      return render_template('meeting.html', API_KEY=API_KEY, convertedClassroomId=convertedClassroomId, joinName=joinName)
    else:
      flash('Wrong DOB or Password, Please try again or reset it on webkiosk. Trying more than 3 times might lock your webkiosk temporarily.')
      return render_template('login.html', classroomId=classroomId)

@app.route('/attendance/', methods = ['GET', 'POST'])
def attendance_login():
  if request.method == 'GET':
    return render_template("attendanceLogin.html")
  else: #req method post
    facultyId = request.form['facultyId']
    facultyPassword = request.form['facultyPassword']
    classroomId = request.form['classroomId']

    if(checkFacultyLogin(client, facultyId, facultyPassword)):
      meetingData = getAttendance(client, classroomId)
      if(meetingData[0]): #if attendance present
        attendance = meetingData[1]

        return render_template("attendance.html", attendance=attendance, classroomId=classroomId)
      else:
        flash('Meeting ID does not exist in Database. No one joined the meeting yet or Make sure you are using JIIT Classroom ID and not Zoom ID')
        return render_template('attendanceLogin.html')
    else:
      flash('Wrong ID or Password, please try again.')
      return render_template('attendanceLogin.html')


if(__name__=='__main__'):
	app.run(debug=True,use_reloader=True)
