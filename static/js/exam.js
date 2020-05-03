
class questionElement {

  constructor(){
    this.questionDiv = `
    <div class="questionDiv">
    <p><b>Question: </b></p>
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
    return this.questionElement

  }


}

addQuestion = () => {
  var el = document.getElementById('examQuestions')
  questionEl = new questionElement()
  final = questionEl.generateElement()
  el.append(final)
  window.scroll(0, window.scrollY + 50)
}