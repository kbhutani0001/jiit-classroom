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
    window.location = `https://jiitclassroom.herokuapp.com/join/${classroomId}`
  }
  else {
    window.alert("Please enter a valid Classroom ID")
  }
}

const redirectToExam = () => {
  examId = document.getElementById('examId').value
  if(examId.length >= 5){
    window.location = `https://jiitclassroom.herokuapp.com/join/test/${examId}`
  }
  else {
    window.alert("Please enter a valid Exam ID")
  }
}

const validateSignup = () => {
  if(document.getElementById('facultyPassword').value!=document.getElementById('facultyPassword2').value) {
    alert('Please enter same password again')
    event.preventDefault()

  }
}

const checkAndRemove = () => {
  var element = document.querySelector('[aria-label="open invite dialog"]')
  if(!element) {
    setTimeout(() => {
      checkAndRemove()
    }, 500);
  }
  removeBtn() 
  return;
}

const removeBtn = () => {
  try {
    var element = document.querySelector('[aria-label="open invite dialog"]')
    if(element){
      try {
        element.style.display = 'None'
      }
      catch(err) {
        console.log("err.. couldnt remove")
        console.log(err)
      }
    }
  }
  catch(err) {console.log(err)}
  }

hideLoading = () => {
  document.getElementsByClassName(`loadingDiv`)[0].style.display = `None`
}