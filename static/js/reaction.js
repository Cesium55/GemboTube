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

function like(){

    var csrftoken = getCookie('csrftoken');
    var id = document.getElementById("videoid");


    var jsonData = {
        "video_id" : id.innerText
    };

    
    // Отправляем JSON на сервер с помощью AJAX
    var request = new XMLHttpRequest();
    request.open("POST", "/like/", true);
    request.setRequestHeader("X-CSRFToken", csrftoken);
    request.setRequestHeader("Content-Type", "application/json");

    console.log(jsonData)
    console.log(JSON.stringify(jsonData))

    request.send(JSON.stringify(jsonData));

    document.getElementById('likeIMG').setAttribute("src", like_img_url);


    like_status = 1;
    swap_like(like_status);
};

function unlike(){

  var csrftoken = getCookie('csrftoken');
  var id = document.getElementById("videoid");


  var jsonData = {
      "video_id" : id.innerText
  };

  
  // Отправляем JSON на сервер с помощью AJAX
  var request = new XMLHttpRequest();
  request.open("POST", "/unlike/", true);
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.setRequestHeader("Content-Type", "application/json");

  console.log(jsonData)
  console.log(JSON.stringify(jsonData))

  request.send(JSON.stringify(jsonData));

  document.getElementById('likeIMG').setAttribute("src", unlike_img_url);
  
  like_status = 0;
  swap_like(like_status);
  

};


function swap_like(new_status){
  lb = document.getElementById("likeButton")
  lc = document.getElementById("likeCounter")
  limg = document.getElementById("likeIMG")
  if (new_status == true){
    lc.innerText = 1 + Number(lc.innerText)
    limg.setAttribute("src", like_img_url)
    lb.removeEventListener("click", like)
    lb.addEventListener("click", unlike)
  }
  else{
    lc.innerText = Number(lc.innerText) - 1
    limg.setAttribute("src", unlike_img_url)
    lb.removeEventListener("click", unlike)
    lb.addEventListener("click", like)
  }
}


function dislike(){

  var csrftoken = getCookie('csrftoken');
  var id = document.getElementById("videoid");


  var jsonData = {
      "video_id" : id.innerText
  };

  
  // Отправляем JSON на сервер с помощью AJAX
  var request = new XMLHttpRequest();
  request.open("POST", "/dislike/", true);
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.setRequestHeader("Content-Type", "application/json");

  console.log(jsonData)
  console.log(JSON.stringify(jsonData))

  request.send(JSON.stringify(jsonData));

  document.getElementById('dislikeIMG').setAttribute("src", dislike_img_url);


  dislike_status = 1;
  swap_dislike(dislike_status);
};

function undislike(){

var csrftoken = getCookie('csrftoken');
var id = document.getElementById("videoid");

// Создаем объект JSON из данных формы

var jsonData = {
    "video_id" : id.innerText
};


// Отправляем JSON на сервер с помощью AJAX
var request = new XMLHttpRequest();
request.open("POST", "/undislike/", true);
request.setRequestHeader("X-CSRFToken", csrftoken);
request.setRequestHeader("Content-Type", "application/json");

console.log(jsonData)
console.log(JSON.stringify(jsonData))

request.send(JSON.stringify(jsonData));

document.getElementById('dislikeIMG').setAttribute("src", undislike_img_url);

dislike_status = 0;
swap_dislike(dislike_status);


};


function swap_dislike(new_status){
lb = document.getElementById("dislikeButton")
lc = document.getElementById("dislikeCounter")
limg = document.getElementById("dislikeIMG")
if (new_status == true){
  lc.innerText = 1 + Number(lc.innerText)
  limg.setAttribute("src", dislike_img_url)
  lb.removeEventListener("click", dislike)
  lb.addEventListener("click", undislike)
}
else{
  lc.innerText = Number(lc.innerText) - 1
  limg.setAttribute("src", undislike_img_url)
  lb.removeEventListener("click", undislike)
  lb.addEventListener("click", dislike)
}
}


