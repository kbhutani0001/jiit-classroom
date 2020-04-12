from flask import Flask, Response, render_template,request,redirect,url_for,send_from_directory,jsonify,abort,send_file
import os
import pymongo
import config
from checkWebkiosk import check
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
  return render_template('index.html')


@app.route('/join', methods=['GET'])
def join():
  return render_template('join.html')

@app.route('/join/<classroomId>', methods=['GET', 'POST'])
def joinClass(classroomId):
  if request.method == 'GET':
    return render_template("login.html", classroomId=classroomId)
  else:
    rollNo = request.form['rollNo']
    password = request.form['password']
    dob = request.form['dob']
    if(check(rollNo, dob, password)):
      return render_template('meeting.html', classroomId=classroomId, rollNo=rollNo)
    else:
      return Response('''
        <h1>Wrong Webkiosk Details, Try again!</h1>'''
        )



if(__name__=='__main__'):
	app.run(debug=True,use_reloader=True)
