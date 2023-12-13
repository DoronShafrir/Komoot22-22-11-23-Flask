// javascript file for Komoot Stat program

// function checkName - cehck and warn once the letters in the name and password not in English
function checkName(e, msgBack) {
    const reg = /^[a-zA-Z0-9\@.]+$/;
    const msgName = document.getElementById(msgBack);
    if (!e.value.match(reg)) {
        msgName.style = "color:red"
        msgName.innerHTML = "Name should contain english letters only"}
    else { msgName.innerHTML = "";  }}

//next section show the date box only if the start date radion buttons checked
//    document.addEventListener("DOMContentLoaded", () =>{
//    let from_when = document.querySelector('.from_when');
//    from_when.addEventListener('change', () =>{
//    let start_date = document.getElementById("start_date");
//    let from_date = document.getElementById("from_date");
//
//    if (from_date.checked){ start_date.style.display = "block" }
//    else{ start_date.style.display = "none" };
//})})

// function checkName - cehck and warn once the letters in the name and password not in English
function check_warning(){
 let result = true;
    let messages = document.querySelectorAll(".warning");
    let letter_error = document.getElementById("letter_error")
    messages.forEach((message) => {
        if (message.innerHTML != "") { result = false }
    });
    if (result == false) {letter_error.style.display = 'block'}
    else {letter_error.style.display = 'none'}

        return result;
}