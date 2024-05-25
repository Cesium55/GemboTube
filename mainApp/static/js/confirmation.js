function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    let timerId = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = 'You can send another code in ' + minutes + ":" + seconds + '!';

        document.getElementById("time").style.display="block";

        if (--timer < 0) {
            display.textContent = "";
            document.getElementById("time").parentElement.style.display="none";
            document.getElementById("SendCode").style.display="block";
            
            clearInterval(timerId);

        }
    }, 1000);
}

window.onload = function () {
    var time = document.getElementById("time").innerText,
        display = document.querySelector('#time');
    startTimer(time, display);
};

function setError(errorText){
    field = document.getElementById("clientErrorMessage")
    field.style.display = "block"
    field.innerHTML = errorText
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}

function codeResponse(event){
    var response = JSON.parse(event.target.response);

    console.log(response)

    if(response['status'] == 0){
        setError(response['message'])
        document.getElementById("confirmCode").value = ''
    }

    if(response['status'] == 1){
        window.location.replace("/")
    }
}

function resendCodeResponse(event){
    var response = JSON.parse(event.target.response);

    console.log(response)

    if(response['status'] == 0){
        
    }

    if(response['status'] == 1){
        
    }
}


function validateCode(event){
    event.preventDefault()

    json()

    return false;
}


function json(){

    var csrftoken = getCookie('csrftoken');

    // Создаем объект JSON из данных формы
    var form = document.getElementById("ConfirmForm");

    

    var formData = new FormData(form);
    var jsonData = {};
    for (var pair of formData.entries()) {
        jsonData[pair[0]] = pair[1];
    }
    
    // Отправляем JSON на сервер с помощью AJAX
    var request = new XMLHttpRequest();
    request.open("POST", form.action, true);
    request.setRequestHeader("X-CSRFToken", csrftoken);
    request.setRequestHeader("Content-Type", "application/json");


    request.onload = (e) => codeResponse(e);


    request.send(JSON.stringify(jsonData));
};


function resendCode(event){
    var csrftoken = getCookie('csrftoken');

    var jsonData = {"hello": "world"};
    
    // Отправляем JSON на сервер с помощью AJAX
    var request = new XMLHttpRequest();
    request.open("POST", "/resendregcode/", true);
    request.setRequestHeader("X-CSRFToken", csrftoken);
    request.setRequestHeader("Content-Type", "application/json");


    request.onload = (e) => resendCodeResponse(e);


    request.send(JSON.stringify(jsonData));
}