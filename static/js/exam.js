
class questionElement {

  constructor(questionCount){
    this.questionDiv = `
    <div class="questionDiv">
    <p><b>${questionCount}. Question: </b></p>
    <textarea required class="form-control" rows="2" placeholder="Add Question text here"></textarea>
    <br>
    <p><b>Answer: </b></p>
    </div>`
    this.answerDiv = document.createElement("div")
    this.answerDiv.classList.add('answerDiv')
    this.questionElement = document.createElement("div")
    this.questionElement.classList.add(`question`)

    /* Sequence
    questionElement main
    then questionDiv
    then answerDiv -> inside all answerOption
    */
  }
  createAnswerElement = (answerNumber) => {
    return `<div class="answerOption">
    <b class="inlineBlock">${answerNumber}. </b> <textarea required class="form-control inlineBlock" rows="1" placeholder="Add answer option ${answerNumber}"></textarea>
    <p class="inlineBlock grayText">This is the correct answer</p>
    <input type="checkbox">
    </div>`
  }

  generateAnswerElement = () => {
    for(let i = 1 ; i<=4 ; i++){
      this.answerDiv.innerHTML += this.createAnswerElement(i)
    }
    this.questionElement.innerHTML = this.questionDiv
    this.questionElement.append(this.answerDiv)
    this.questionElement.append(document.createElement("br"))
    return this.questionElement

  }
}

addQuestion = () => {
  let questionCount = $('.question').length
  var el = document.getElementById('examQuestions')
  questionEl = new questionElement(questionCount+1)
  final = questionEl.generateAnswerElement()
  el.append(final)
  window.scroll(0, window.scrollY + 50)
  document.getElementById('createTestBtn').style.display = `inline`
}
apiRequest = (examData) => {
  axios.post(`/create/test/make/${examData.testId}/`, { examData: examData })
  .then(function (response) {
    console.log(response);
    window.alert(response.data)
    window.location = '/dashboard/exams/'
  })
  .catch(function (error) {
    window.alert('Some error occurred while creating Exam.')
  });

}

createTest = (examId, examName, subjectCode, examDate, examStartTime, examEndTime, facultyId, examDescription) => {
  examData = {
    "examId": examId,
    "examName": examName,
    "subjectCode": subjectCode,
    "examDescription": examDescription,
    "examDate": examDate,
    "examStartTime": examStartTime,
    "examEndTime": examEndTime,
    "facultyId": facultyId,
    "exam": {

    }
  }
  examData.formHtml = document.getElementsByClassName(`mainDiv`)[0].innerHTML
  examQuestions = $('.question')
  let checkboxes = $("input[type='checkbox']")
  let checkboxCount = 0
  for (let k = 0; k<checkboxes.length; k++ ){
    if(checkboxes[k].checked) { checkboxCount++ }
  } // see how many answers have been checked
  if(examQuestions.length != checkboxCount) {
    alert("Please select right number of correct answers.")
    return
    // correct answer count should be equal to number of questions
  }
  else {
    document.getElementsByClassName(`loadingDiv`)[0].style.display = `Block`
    for (let i=0; i<examQuestions.length; i++){
      let question = examQuestions[i].getElementsByClassName('questionDiv')[0].getElementsByTagName('textarea')[0].value
      let answersDiv = examQuestions[i].getElementsByClassName('answerDiv')[0]
      answerOptions = answersDiv.getElementsByClassName(`answerOption`)
      answers = []
      for( let j =0 ; j< answerOptions.length ; j++){
        let answerText = answerOptions[j].getElementsByTagName('textarea')[0].value
        let flag = answerOptions[j].getElementsByTagName('input')[0].checked //check if answer right or wrong
        answers.push([answerText, flag])
      }
      examData.exam[`question${i+1}`] = { question: question, answers: answers}
    }
    apiRequest(examData)
  }
}