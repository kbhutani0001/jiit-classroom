
class questionElement {

  constructor(questionCount){
    this.questionDiv = `
    <div class="questionDiv">
    <p><b>${questionCount}. Question: </b></p>
    <textarea class="form-control" rows="2" placeholder="Question Text"></textarea>
    <br>
    <p><b>Answer: </b></p>
    </div>`
    this.answerOption = `<div class="answerOption">
    <textarea class="form-control inlineBlock" rows="1" placeholder="Option"></textarea>
    <p class="inlineBlock grayText">This is the correct answer</p>
    <input type="checkbox" >
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
  generateElement = () => {
    for(let i =0 ; i<4 ; i++){
      this.answerDiv.innerHTML += this.answerOption
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
  final = questionEl.generateElement()
  el.append(final)
  window.scroll(0, window.scrollY + 50)
}