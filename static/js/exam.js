
class questionElement {

  constructor(questionCount){
    this.questionDiv = `
    <div class="questionDiv">
    <p><b>${questionCount}. Question: </b></p>
    <textarea class="form-control" rows="2" placeholder="Add Question text here"></textarea>
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
    <b class="inlineBlock">${answerNumber}. </b> <textarea class="form-control inlineBlock" rows="1" placeholder="Add answer option ${answerNumber}"></textarea>
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
  if(questionCount > 0 ){
    document.getElementById('createTestBtn').style.display = `inline`
  }
}

createTest = () => {
    examData = {
      "testId": "12345678910",
      "testName": "ABC QUIZ",
      "subjectCode": "12ABC34",
      "testDescription": "Any description",
      "testDate": "dd/mm/yyyy",
      "testStartTime": "12345678910",
      "testEndTime": "12345678910",
      "facultyId": "test@test.com",
      "exam": {
        "question1": {
          "question": "question text here",
          "answers": [ ["optionValue", false], ["optionValue", false], ["optionValue", true], ["optionValue", false] ]
        },
        "question2": {
          "question": "question text here",
          "answers": [ ["optionValue", false], ["optionValue", false], ["optionValue", true], ["optionValue", false] ]
        },
        "question3": {
          "question": "question text here",
          "answers": [ ["optionValue", false], ["optionValue", false], ["optionValue", true], ["optionValue", false] ]
        },
        "question4": {
          "question": "question text here",
          "answers": [ ["optionValue", false], ["optionValue", false], ["optionValue", true], ["optionValue", false] ]
        },
        "question5": {
          "question": "question text here",
          "answers": [ ["optionValue", false], ["optionValue", false], ["optionValue", true], ["optionValue", false] ]
        }
      }
    }
  examQuestions = $('.question')
  for (i=0; i<examQuestions.length; i++){
    let question = examQuestions[i].getElementsByClassName('questionDiv')[0].getElementsByTagName('textarea')[0].value
  }
  return
}