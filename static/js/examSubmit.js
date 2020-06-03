submitExam = () => {
    document.getElementById("submitExam").click()
}


timeLeftString = (timeLeft) => {
    minutes = parseInt(timeLeft/60)
    seconds = timeLeft%60
    return `${minutes} : ${seconds}`
}

const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
  }

startTime = async (timeLeft) => {
    for(let i = 0; i<=timeLeft; i++){
        await sleep(1000)
        let t = timeLeft-i
        document.getElementById('timeLeft').innerText = timeLeftString(t)
        if(timeLeft-i<60){
            document.getElementById('timeLeftDiv').style.color = "red"
        }
        if(i===timeLeft){
            submitExam()
            break
        }
    }
    return;
  }

