from flask import Flask, flash, Response, render_template,request,redirect,url_for,send_from_directory,jsonify,abort,send_file
import os
from checkWebkiosk import check
from dbCheck import getAttendance, checkFacultyLogin, markAttendance
import pymongo
import config


app = Flask(__name__)
app.secret_key = "jiit128sucks"

client = pymongo.MongoClient(config.mlabURI, connectTimeoutMS=50000)

@app.route('/', methods=['GET'])
def home():
  return render_template('index.html')


@app.route('/join/', methods=['GET'])
def join():
  return render_template('join.html') 

@app.route('/create/', methods=['GET'])
def create():
  return render_template('create.html')


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
    if(check(rollNo, dob, password)):
      markAttendance(client, classroomId, rollNo, loginTime)
      return render_template('meeting.html', classroomId=classroomId, rollNo=rollNo)
    else:
      flash('Wrong DOB or Password, Please try again or reset it on webkiosk.')
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
        flash('Meeting ID does not exist in Database. Make sure you are using JIIT Classroom ID and not Zoom ID')
        return render_template('attendanceLogin.html')
    else:
      flash('Wrong ID or Password, please try again.')
      return render_template('attendanceLogin.html')


if(__name__=='__main__'):
	app.run(debug=True,use_reloader=True)
