function nicknameValidator(nickname){
    if(nickname.length < 1){
        setError("Too short nickname! (min 1 symbol)")
        return false;
    }

    if(nickname.length > 50){
        setError("Too long nickname! (max 50 symbols)")
        return false;
    }

    const alph = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890 йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ_-.,@$';

    
    for(i=0;i<nickname.length;i++){
        flag = false;
        for(j=0;j<alph.length;j++){
            if(nickname[i]==alph[j]){
                flag=true;
                break;
            }    
        }
        if(flag == false){
            setError("Nickname contains forbidden symbols!")
            return flag;
        }
    }

    return true;
}

function emailValidator(email){
    if(email.length < 1){
        setError("Invalid email!")
        return false;
    }

    return true
}

function passwordValidator(pass1, pass2){
    if(pass1.length < 6){
        setError("Too short password! (min 6 symbols)")
        return false;
    }

    if(pass1.length > 254){
        setError("Too long password! (max 254 symbols)")
        return false;
    }

    if(pass1 != pass2){
        setError("Passwords are different")
        return false;
    }

    return true
}


function setError(errorText){
    field = document.getElementById("clientErrorMessage")
    field.style.display = "block"
    field.innerHTML = errorText
}

// Получаем токен csrf из куки
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

function regResponse(event){
    var response = JSON.parse(event.target.response);

    if(response['status'] == 0){
        setError(response['message'])
        document.getElementById("password").value = ''
        document.getElementById("passwordConf").value = ''
    }

    if(response['status'] == 1){
        window.location.replace("/login")
    }
}

function json(){

    var csrftoken = getCookie('csrftoken');

    // Создаем объект JSON из данных формы
    var form = document.getElementById("registrationForm");
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


    request.onload = (e) => regResponse(e);


    request.send(JSON.stringify(jsonData));
};

function Validation(event){

    event.preventDefault()

    var pass1 = document.getElementById("password").value;
    var pass2 = document.getElementById("passwordConf").value;
    var email = document.getElementById("email").value;
    var nickname = document.getElementById("nickname").value;

    pRes = passwordValidator(pass1, pass2)
    eRes = emailValidator(email)
    nRes = nicknameValidator(nickname)

    if(nRes && eRes && pRes == true){
        json()
    }
}