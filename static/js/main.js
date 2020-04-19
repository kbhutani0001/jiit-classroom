const copyToClipboard = (code) => {
  if(code==1){
    var str = document.getElementById('classroomId').value 
  }
  else{
    var str = document.getElementById('meetingUrl').value 
  }

  const el = document.createElement('textarea');
  el.value = str;
  document.body.appendChild(el);
  el.select();
  document.execCommand('copy');
  document.body.removeChild(el);


};

const redirectToClass = () => {
  classroomId = document.getElementById('classroomNumber').value
  if(classroomId.length >= 9){
    window.location = '/join/' + classroomId
  }
  else {
    window.alert("Please enter a valid Classroom ID")
  }
}

const validateSignup = () => {
  if(document.getElementById('facultyPassword').value!=document.getElementById('facultyPassword2').value) {
    alert('Please enter same password again')
    event.preventDefault()

  }
}

