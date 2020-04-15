from flask import Flask, flash, Response, render_template,request,redirect,url_for,send_from_directory,jsonify,abort,send_file
import os
import pymongo
import config
from checkWebkiosk import check
app = Flask(__name__)
app.secret_key = "jiit128sucks"

@app.route('/', methods=['GET'])
def home():
  return render_template('index.html')


@app.route('/join/', methods=['GET', 'POST'])
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
    dob = dob.split('-')[2] + '-' + dob.split('-')[1] + '-' + dob.split('-')[0]
    if(check(rollNo, dob, password)):
      return render_template('meeting.html', classroomId=classroomId, rollNo=rollNo)
    else:
      flash('Wrong DOB or Password, Please try again or reset it on webkiosk.')
      return render_template('login.html')

@app.route('/attendance', methods = ['GET', 'POST'])
def attendance_login():
  if request.method == 'GET':
    return render_template("attendanceLogin.html")

@app.route('/enroll', methods = ['GET', 'POST'])
def attendance():
  if request.method == 'GET':
    attend = {
    9918102177 : "12:09",
    9211223093 : "12:65"
    }
    return render_template("attendance.html", attend=attend, classroomId=1234)

@app.route('/faculty', methods = ['GET', 'POST'])
def faculty():
  if request.method == 'GET':
    return render_template('faculty.html')

if(__name__=='__main__'):
	app.run(debug=True,use_reloader=True)
