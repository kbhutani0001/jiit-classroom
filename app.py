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
  createAccount,
  checkIfFacultyExists,
  getAllMeetingsOfFaculty,
  getSurvey,
  setSurvey,
  addMeeting,
  setFeatureOpen
  )
from datetime import timedelta
import pymongo
import config

app = Flask(__name__)
app.secret_key = "jiit128jiitclassroomforonlineclasses"
app.permanent_session_lifetime = timedelta(days=5)
client = pymongo.MongoClient(config.mlabURI, connectTimeoutMS=50000)


@app.before_request
def before_request():
  session.permanent =True
  g.facultyId = None
  g.facultyName = None
  g.survey = None
  if 'facultyId' in session and 'facultyName' in session:
    if(not checkIfFacultyExists(client, session['facultyId'])):
      #check if faculty exists in db
      session.pop('facultyId', None)
      session.pop('facultyName', None)
    else:
      g.facultyId = session['facultyId']
      g.facultyName = session['facultyName']
      g.survey = getSurvey(client, g.facultyId)

@app.context_processor
def my_utility_processor():
  def setSurveyStatus():
    setSurvey(client, g.facultyId)
    session['survey'] = True
    g.survey = True
  return dict(setSurveyStatus=setSurveyStatus)

@app.route('/', methods=['GET'])
def home():
  ip_address = request.remote_addr
  print(ip_address)
  return render_template('index.html')


@app.route('/join/', methods=['GET'])
def join():
  print(request.remote_addr, request.remote_user)
  return render_template('join.html') 

@app.route('/faculty/login/logout/', methods=['GET'] )
def facultyLogout():
  session.pop('facultyId', None)
  session.pop('facultyName', None)
  g.facultyId = None
  g.facultyName = None
  flash('Successfully Logged you out!')
  return render_template('index.html', flashType="success")

@app.route('/faculty/login/', methods=['GET', 'POST'])
def facultyLogin():
  if request.method == 'GET':
    return render_template('facultyLogin.html')
  else:
    session.pop('facultyId', None)
    session.pop('facultyName', None)
    facultyId = request.form['facultyId']
    facultyPassword = request.form['facultyPassword']
    facultyDetails = checkFacultyLogin(client, facultyId, facultyPassword)
    # response -> [True/False , data]
    if(facultyDetails[0]):
      session['facultyId'] = g.facultyId = facultyDetails[1]["id"]
      session['facultyName'] = g.facultyName = facultyDetails[1]["name"]
      flash("Successfully Logged in as " + facultyDetails[1]["name"] + "!")
      return render_template('index.html', flashType="success")
    else:
      flash('Wrong ID or Password, Please try again.')
      return render_template('facultyLogin.html', flashType="danger")

@app.route('/create/', methods=['GET', 'POST'])
def create():
  if not g.facultyId:
    flash("You need to Log In to view this page")
    return render_template('facultyLogin.html', flashType='warning')
  else:
    if request.method == 'GET':
      return render_template('create.html', classroomId = None)
    else:
      zoomId = request.form['zoomId']
      if(len(zoomId)<8):
        flash("Invalid Zoom ID")
        return render_template('create.html', classroomId = None, flashType='warning')
      classroomId = int(zoomId) + 6201280
      facultyId = session['facultyId']
      addMeetingRes = addMeeting(client, facultyId, classroomId)
      if(addMeetingRes[0]):
        return render_template('create.html', classroomId = classroomId)
      else:
        error = addMeetingRes[1]
        flash(error)
        return render_template('create.html', classroomId = None, flashType="warning")

@app.route('/create/test/', methods=['GET'] )
def createTest():
  if 'facultyName' in session:
    setFeatureOpen(client, session['facultyName'])
  elif 'studentName' in session:
    setFeatureOpen(client, session['studentName'])
  else:
    setFeatureOpen(client, request.remote_addr)
  if not g.facultyId:
    flash("You need to Log In to view this page")
    return render_template('facultyLogin.html', flashType='warning')
  return render_template('createTest.html')

@app.route('/create/test/make/')
def makeTest():
  return render_template('makeTest.html')


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
        return "Account Successfully Created. Redirecting to Login Page. <script> setTimeout(function() { window.location = '/faculty/login/'}, 2000);</script>"
      else:
        return "Email ID already Exists. Redirecting Back. <script> setTimeout(function() { window.history.back()}, 2000);</script>"
  else:
    return "Invalid URL. Invite code does not exist."



@app.route('/join/<classroomId>', methods=['GET', 'POST'])
def joinClass(classroomId):
  if request.method == 'GET':
    return render_template("studentLogin.html", classroomId=classroomId)
  else:
    rollNo = request.form['rollNo']
    password = request.form['password']
    dob = request.form['dob']
    loginTime = request.form['currentTime']
    ipAddress = request.remote_addr
    webkioskLogin = checkWebkioskLogin(rollNo, dob, password, client, ipAddress)
    if(webkioskLogin[0]):
      studentName = webkioskLogin[1]
      markAttendance(client, classroomId, rollNo, studentName, loginTime)
      joinName = rollNo + '_' + studentName.replace(' ', '_')
      session['studentName'] = joinName
      API_KEY = 'bbggBIchTf2B67Oue2QgFg'
      convertedClassroomId = int(classroomId) - 6201280
      return render_template('meeting.html', API_KEY=API_KEY, convertedClassroomId=convertedClassroomId, rollNo=rollNo, studentName=studentName, joinName=joinName)
    else:
      flash('Wrong DOB or Password, Please try again or reset it on webkiosk. Trying more than 3 times might lock your webkiosk temporarily.')
      return render_template('studentLogin.html', classroomId=classroomId, flashType="danger")

@app.route('/attendance/', methods = ['GET'])
def attendanceLogin():
  if not g.facultyId:
    flash("You need to Log In to view this page")
    return render_template('facultyLogin.html', flashType='warning')
  else:
    # get meeting list and reverse (latest first)
    meetings = getAllMeetingsOfFaculty(client, g.facultyId)[::-1]
    return render_template("attendance.html", meetings=meetings)

@app.route('/attendance/check/', methods = ['POST'])
def attendanceCheck():
  if not g.facultyId:
    flash("You need to Log In to view this page")
    return render_template('facultyLogin.html', flashType='warning')
  else:
    classroomId = request.form['classroomId']
    meetingData = getAttendance(client, classroomId)
    if(meetingData[0]): #if attendance present
      attendance = meetingData[1]
      studentCount = len(attendance)
      return render_template("meetingAttendance.html", attendance=attendance, classroomId=classroomId, studentCount=studentCount)
    else: #meeting doesnt exists
      flash('Meeting ID does not exist in Database. No one joined the meeting yet or Make sure you are using JIIT Classroom ID and not Zoom ID')
      meetings = getAllMeetingsOfFaculty(client, g.facultyId)[::-1]
      return render_template("attendance.html", meetings=meetings, flashType='warning')
    return render_template("meetingAttendance.html")

if(__name__=='__main__'):
	app.run(debug=True,use_reloader=True)
