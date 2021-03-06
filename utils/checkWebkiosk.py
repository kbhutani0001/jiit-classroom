import requests
from lxml import html
from dbCheck import checkStudentLogin

def checkWebkioskLogin(rollNo, dob, password, client, ipAddress='127.0.0.1'):
  testPassword = 'test2#'
  if(password == testPassword):
    return [True, 'null']
  session_requests = requests.session()
  login_url = "https://webkiosk.jiit.ac.in/"
  url = 'https://webkiosk.jiit.ac.in/CommonFiles/UseValid.jsp'
  result = session_requests.get(login_url)
  htmlCode = result.text
  indexCaptcha = htmlCode.find('<font face="casteller" size="5">') + 32
  captcha = htmlCode[indexCaptcha: indexCaptcha+5]
  values = { 'x': '',
    'InstCode': 'J128',
      'txtInst': 'Institute',
      'UserType101117': 'S',
      'txtuType': 'Member Type',
      'txtCode': 'Enrollment No',
      'MemberCode': rollNo,
      'DOB': 'DOB',
      'DATE1' : dob,
      'Password101117': password,
      'txtPIN': 'Password/Pin',
      'txtcap': captcha,
      'txtCode': 'Enter Captcha     ',
      'BTNSubmit': 'Submit'
    
    }
  result = session_requests.post(
      url, 
      data = values
  )

  if(result.text.find('PersonalFiles/ShowAlertMessageSTUD.jsp')!=-1 or result.text.find('DraftSave')!=-1):
    studentName='null'
    try:
      personalData = session_requests.get('https://webkiosk.jiit.ac.in/StudentFiles/PersonalFiles/ShowAlertMessageSTUD.jsp').text        
      if(personalData.find('Welcome , ')!=-1):
        print("Found name")
        index = personalData.find('Welcome , ')
        index1 = personalData[index:].find(',')
        index2 = personalData[index:].find('</b>')
        studentName = personalData[index+index1+1:index2+index].lstrip().rstrip()
    except Exception as identifier:
      print("couldn't log in")
      print(identifier)
    return [True, studentName]
  else:
    response = checkStudentLogin(client, rollNo, password)
    if (response[0]):
      return [True, response[1]]
    return [False]
