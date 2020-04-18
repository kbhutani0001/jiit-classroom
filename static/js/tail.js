loc = window.location.href
if(loc.includes("create")){
  var temp = document.getElementById('createNav')
  temp.classList.add('active')
}
else if(loc.includes("join")){
  var temp = document.getElementById('joinNav')
  temp.classList.add('active')
}
else if(loc.includes("attendance")){
  var temp = document.getElementById('attendanceNav')
  temp.classList.add('active')
}