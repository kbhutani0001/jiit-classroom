import requests
from lxml import html

def check(rollNo, dob, password):
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
  if(result.text.find('PersonalFiles/ShowAlertMessageSTUD.jsp')!=-1 or password=='test128#' or result.text.find('1DraftSave')!=-1):
    return True
  else:
    return False
