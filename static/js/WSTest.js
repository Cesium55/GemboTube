function makeNotification(link, title, text) {
    // Создаем новый элемент a
    var a = document.createElement('a');
    a.setAttribute('href', link);

    // Создаем и настраиваем div.notification
    var notification = document.createElement('div');
    notification.className = 'notification';

    // Создаем и настраиваем div.notificationUpperPanel
    var notificationUpperPanel = document.createElement('div');
    notificationUpperPanel.className = 'notificationUpperPanel';

    // Создаем и добавляем img.notificationIMG
    var imgBell = document.createElement('img');
    imgBell.setAttribute('src', '/static/img/bell.png');
    imgBell.className = 'notificationIMG';
    notificationUpperPanel.appendChild(imgBell);

    // Создаем и добавляем h3.notificationTitle
    var h3 = document.createElement('h3');
    h3.className = 'notificationTitle';
    h3.textContent = title;
    notificationUpperPanel.appendChild(h3);

    // Создаем и добавляем img.notificationCROSS
    var imgCross = document.createElement('img');
    imgCross.setAttribute('src', '/static/img/cross.png');
    imgCross.className = 'notificationCROSS';
    notificationUpperPanel.appendChild(imgCross);
    imgCross.onclick = function(e) {
        e.preventDefault();
        notification.remove();
    };

    // Добавляем верхнюю панель в блок уведомления
    notification.appendChild(notificationUpperPanel);

    // Создаем и настраиваем div.notificationText
    var notificationText = document.createElement('p');
    notificationText.className = 'notificationText';
    notificationText.textContent = text;

    // Добавляем текст уведомления в блок уведомления
    notification.appendChild(notificationText);

    // Добавляем блок уведомления в элемент a
    a.appendChild(notification);

    // Добавляем элемент a в notificationsBlock
    document.getElementById('notificationsBlock').appendChild(a);
}


document.addEventListener('DOMContentLoaded', function() {
    // Подключение к WebSocket
    var socket = new WebSocket(
        'ws://' + window.location.host + "/ws/"
    );

    // Получение сообщения от сервера
    socket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message = data['message'];

        console.log("che to poluchili");
        console.log(data);

        var link = message['link'];
        var title = message['title'];
        var text = message['text'];

        if(link!=undefined & title!=undefined & text!=undefined){makeNotification(link, title, text);}


        // Добавление сообщения в div с id="chat-log"
        // document.querySelector('#chat-log').value += (message + '\n');
    };

    // // Отправка сообщения на сервер
    // document.querySelector('#chat-message-input').onkeyup = function(e) {
    //     if (e.keyCode === 13) {  // enter, return
    //         document.querySelector('#chat-message-submit').click();
    //     }
    // };

    // document.querySelector('#chat-message-submit').onclick = function(e) {
    //     var messageInputDom = document.querySelector('#chat-message-input');
    //     var message = messageInputDom.value;
    //     // Отправка сообщения через WebSocket
    //     socket.send(JSON.stringify({
    //         'message': message
    //     }));
    //     messageInputDom.value = '';
    // };
});


