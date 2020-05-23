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
  setFeatureOpen,
  getMeetingPassword,
  addExam,
  getExamTable,
  getExamDetails,
  submitExam,
  getExamResults
  )
from datetime import timedelta
import pymongo
import config
from methods import (
  createExamId,
  getTimeStampFromDT,
  randomizeQuestions,
  separateQuestions,
  computeResults
)
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
      # g.survey = getSurvey(client, g.facultyId)
  if not 'examData' in g:
    g.examData = None
# @app.context_processor
# def my_utility_processor():
#   def setSurveyStatus():
#     setSurvey(client, g.facultyId)
#     session['survey'] = True
#     g.survey = True
#   return dict(setSurveyStatus=setSurveyStatus)

@app.route('/', methods=['GET'])
def home():
  ip_address = request.remote_addr
  print(ip_address)
  return render_template('index.html')


@app.route('/join/', methods=['GET'])
def join():
  print(request.remote_addr, request.remote_user)
  return render_template('join.html') 

@app.route('/join/test/', methods=['GET'])
def joinExamHome():
  return render_template('joinExam.html') 


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
      meetingPassword = request.form['meetingPassword']
      if(len(zoomId)<8):
        flash("Invalid Zoom ID")
        return render_template('create.html', classroomId = None, flashType='warning')
      classroomId = int(zoomId) + 6201280
      facultyId = session['facultyId']
      addMeetingRes = addMeeting(client, facultyId, classroomId, meetingPassword)
      if(addMeetingRes[0]):
        return render_template('create.html', classroomId = classroomId)
      else:
        error = addMeetingRes[1]
        flash(error)
        return render_template('create.html', classroomId = None, flashType="warning")

@app.route('/create/test/', methods=['GET', 'POST'] )
def createTest():
  if not g.facultyId:
    flash("You need to Log In to view this page")
    return render_template('facultyLogin.html', flashType='warning')
  else:
    if request.method == 'GET':
      return render_template('createTest.html')
    else:
      data = request.form
      examId = createExamId()
      examStartTime = getTimeStampFromDT(data['examDate'], data['examStartTime'] )
      examEndTime = getTimeStampFromDT(data['examDate'], data['examEndTime'] )
      examDuration = examEndTime - examStartTime
      randomQuestions = True if 'randomQuestions' in data else False
      videoMonitoring = True if 'videoMonitoring' in data else False
      examData = {
        'examId': examId,
        'examName': data['examName'],
        'subjectCode': data['subjectCode'],
        'examDate': data['examDate'],
        'examStartTime': examStartTime,
        'examEndTime': examEndTime,
        'examDescription': data['examDescription'],
        'randomQuestions': randomQuestions,
        'videoMonitoring': videoMonitoring
      }
      return render_template('makeTest.html', examData = examData, examDuration = examDuration, facultyId = g.facultyId)

@app.route('/create/test/make/<testId>/', methods=['POST'])
def saveTest(testId):
  if not g.facultyId:
    flash("You need to Log In to view this page")
    return render_template('facultyLogin.html', flashType='warning')
  else:
    examData = request.get_json()['examData']
    print(examData)
    randomQuestions = True if examData['randomQuestions'] == "True" else False
    videoMonitoring = True if examData['videoMonitoring'] == "True" else False
    examData['randomQuestions'] = randomQuestions
    examData['videoMonitoring'] = videoMonitoring

    addExamRes = addExam(client, g.facultyId, examData)
    if addExamRes[0]:
      return 'Successfully added exam. Redirecting to Dashboard'
    else:
      return addExamRes[1]

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
    return render_template("studentLogin.html", classroomId=classroomId, postUrl = '/join/{}'.format(classroomId))
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
      meetingPassword = getMeetingPassword(client, classroomId)
      print(meetingPassword)
      joinName = rollNo + '_' + studentName.replace(' ', '_')
      session['studentName'] = joinName
      API_KEY = 'DoRcyU-qTfmmZ5nX0atdWA'
      convertedClassroomId = int(classroomId) - 6201280
      return render_template('meeting.html', API_KEY=API_KEY, convertedClassroomId=convertedClassroomId, meetingPassword=meetingPassword, rollNo=rollNo, studentName=studentName, joinName=joinName)
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


@app.route('/dashboard/exams/', methods = ['GET'])
def examDashboard():
  if not g.facultyId:
    flash("You need to Log In to view this page")
    return render_template('facultyLogin.html', flashType='warning')
  else:
    examTable = getExamTable(client, g.facultyId)
    return render_template("examDashboard.html", examTable=examTable)

@app.route('/check/exams/results/<examId>', methods = ['GET'])
def examResults(examId):
  if not g.facultyId:
    flash("You need to Log In to view this page")
    return render_template('facultyLogin.html', flashType='warning')
  else:
    examResults = getExamResults(client, examId)
    return render_template("results.html", examId=examId,  examResults=examResults, studentCount = len(examResults))



@app.route('/join/test/<examId>/', methods=['GET', 'POST'])
def joinExam(examId):
  if request.method == 'GET':
    return render_template("studentLogin.html", examId=examId, postUrl = '/join/test/{}/'.format(examId))
  else:
    rollNo = request.form['rollNo']
    password = request.form['password']
    dob = request.form['dob']
    webkioskLogin = checkWebkioskLogin(rollNo, dob, password, client)
    if(webkioskLogin[0]):
      studentName = webkioskLogin[1]
      examData = getExamDetails(client, examId)
      if (examData[0]):
        if( examData[1]['randomQuestions'] ):
          examData, questions = randomizeQuestions(examData[1])
        else:
          examData, questions = separateQuestions(examData[1])
        flash("Succesfully logged in as {} ({})".format(studentName, rollNo))
        return render_template('startExam.html' ,flashType = "success", rollNo=rollNo, studentName=studentName , examData = examData, questions=questions , timeLeft = 120)
      flash(examData[1])
      return render_template("studentLogin.html", flashType="danger", postUrl = '/join/test/{}/'.format(examId))
    else:
      flash('Wrong DOB or Password, Please try again or reset it on webkiosk. Trying more than 3 times might lock your webkiosk temporarily.')
      return render_template('studentLogin.html', examId=examId, flashType="danger")
      

@app.route('/join/test/submit/', methods = ['POST'])
def submitTest():
  studentExamData = request.form.to_dict()
  examId = studentExamData['examId']
  examData = getExamDetails(client, examId)[1]
  score = computeResults(examData, studentExamData)
  response = submitExam(client, studentExamData, score)
  if(response[0]):
    flash('Successfully submitted your exam!')
    return render_template('index.html', flashType="success")
  flash(response[1])
  return render_template('index.html', flashType="danger")

@app.route('/preview/exam/<examId>/', methods=['GET'])
def previewExam(examId):
  if not g.facultyId:
    flash("You need to Log In to view this page")
    return render_template('facultyLogin.html', flashType='warning')
  else:
    examData = getExamDetails(client, examId)
    if (examData[0]):
      if( examData[1]['randomQuestions'] ):
        examData, questions = randomizeQuestions(examData[1])
      else:
        examData, questions = separateQuestions(examData[1])
      studentName = 'Test_{}'.format(g.facultyId)
      rollNo = 'Test'
      flash("Succesfully logged in as {} ({}).".format(studentName, rollNo))
      flash("Time duration for preview: 2 mins")
      return render_template('startExam.html' ,flashType = "success", rollNo=rollNo, studentName=studentName , examData = examData, questions=questions , timeLeft = 120)
    flash(examData[1])
    return redirect(url_for('examDashboard'))

if(__name__=='__main__'):
	app.run(debug=True,use_reloader=True)
