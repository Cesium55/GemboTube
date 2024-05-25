function emailValidator(email){
    if(email.length < 1){
        setError("Invalid email!")
        return false;
    }

    return true
}

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

function loginResponse(event){
    var response = JSON.parse(event.target.response);

    if(response['status'] == 0){
        setError(response['message'])
        document.getElementById("email").value = ''
    }

    if(response['status'] == 1){
        window.location.replace("/")
    }
}

function json(){

    var csrftoken = getCookie('csrftoken');

    // Создаем объект JSON из данных формы
    var form = document.getElementById("loginForm");

    

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


    request.onload = (e) => loginResponse(e);


    request.send(JSON.stringify(jsonData));
};

function Validation(event){

    event.preventDefault()

    var email = document.getElementById("email").value;
    var token = document.getElementById("loginForm").getElementsByTagName("input")[0].value
    
    eRes = emailValidator(email)

    if(eRes == true){
        json()
    }
}