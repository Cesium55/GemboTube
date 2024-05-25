
document.getElementById('id_originalVideo').addEventListener('change', function(e) {
    var file = this.files[0];
    if (file) {
        var formData = new FormData();
        formData.append('originalVideo', file);

        var xhr = new XMLHttpRequest();
        var csrftoken = getCookie('csrftoken');
        
        
        // Обработчик для отслеживания прогресса загрузки
        xhr.upload.onprogress = function(event) {
            if (event.lengthComputable) {
                var percentComplete = (event.loaded / event.total) * 100;
                document.getElementById('upload-progress').value = percentComplete;
            }
        };

        xhr.open('POST', '/loadTempVideo/', true);
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        xhr.onload = function () {
            console.log(xhr)
            console.log(xhr.status)
            response = JSON.parse(xhr.response)
            if (response.status === 200) {
                alert('Файл успешно загружен');
                document.getElementById("backID").value = JSON.parse(xhr.responseText).backID
            } else {
                alert('Произошла ошибка при загрузке файла');
            }
        };
        xhr.send(formData);
    }
});




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



document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var csrftoken = getCookie('csrftoken');
    var formData = new FormData(this);


    formData.delete('originalVideo');


    var xhr = new XMLHttpRequest();

    xhr.open('POST', document.getElementById('loginForm').action, true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);

    xhr.onload = function () {
        if (xhr.status === 200) {
            alert('Форма отправлена без видеофайла');
        } else {
            alert('Произошла ошибка при отправке формы');
        }
    };

    xhr.send(formData);
});