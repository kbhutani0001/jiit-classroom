from flask import Flask, Response, render_template,request,redirect,url_for,send_from_directory,jsonify,abort,send_file
import os
import pymongo
import config
from checkWebkiosk import check
app = Flask(__name__)

@app.route('/<classroomId>', methods=['GET', 'POST'])
def home(classroomId):
  if request.method == 'GET':
    return render_template("index.html", classroomId=classroomId)
  else:
    rollNo = request.form['rollNo']
    password = request.form['password']
    dob = request.form['dob']
    if(check(rollNo, dob, password)):
      return render_template('meeting.html')
    else:
      return Response('''
        <h1>Wrong Details, Try again!</h1>
        <button onclick="window.location = "/''' + classroomId + '''">Home</button>'''
        )



if(__name__=='__main__'):
	app.run(debug=True,use_reloader=True)
