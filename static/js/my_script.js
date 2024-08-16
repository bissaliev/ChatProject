document.getElementById("chat").scrollTop = document.getElementById("chat").scrollHeight
const roomName = JSON.parse(
    document.getElementById('room-name').textContent
);
const userName = JSON.parse(
    document.getElementById('username').textContent
);
const url = 'ws://' + window.location.host + '/ws/chat/room/' + roomName + '/';
const chatSocket = new WebSocket(url);

function timeAgo(date) {
    const now = new Date();
    const secondsPast = Math.floor((now - date) / 1000);

    if (secondsPast < 60) {
        return `${secondsPast} секунд назад`;
    }
    if (secondsPast < 3600) {
        const minutes = Math.floor(secondsPast / 60);
        return `${minutes} минут назад`;
    }
    if (secondsPast < 86400) {
        const hours = Math.floor(secondsPast / 3600);
        return `${hours} часов назад`;
    }
    if (secondsPast < 2592000) {
        const days = Math.floor(secondsPast / 86400);
        return `${days} дней назад`;
    }
    if (secondsPast < 31536000) {
        const months = Math.floor(secondsPast / 2592000);
        return `${months} месяцев назад`;
    }
    const years = Math.floor(secondsPast / 31536000);
    return `${years} лет назад`;
};

// Получение шаблона для сообщения
function getTemplate(userName, sender) {
    if (userName == sender) {
        return document.getElementById('message-template-me');
    } else {
        return document.getElementById('message-template');
    }
}

function buildingMessageTemplate(data) {
    const template = getTemplate(userName, data.username);
    const messageElement = template.content.cloneNode(true);
    messageElement.getElementById("message-content").textContent = data.message;
    messageElement.getElementById("message-username").textContent = data.username;
    const timestamp = new Date(data.created_at);
    messageElement.getElementById("message-time").textContent = timeAgo(timestamp);
    messageElement.getElementById('message-sender-avatar').src = data.avatar;
    return messageElement
};

// Добавление шаблона сообщения в чат
function addMessageToChat(data) {
    const chat = document.getElementById("chat");
    messageElement = buildingMessageTemplate(data);
    chat.appendChild(messageElement);
    chat.scrollTop = chat.scrollHeight;
};

function buildUserTemplate(user) {
    const userItem = document.getElementById('user-template').content.cloneNode(true);
    userItem.getElementById("field-username").textContent = user['username']
    userItem.getElementById("field-avatar").src = user['avatar']
    userItem.id = "participant-" + user['avatar'];
    return userItem;
}

function buildUserListTemplate(data) {
    const userList = document.getElementById('user-list');
    userList.innerHTML = "";
    for (let user of data.users) {
        template = buildUserTemplate(user);
        userList.appendChild(template);
    };
}

// получение данных через веб-сокет
chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    if (data.type == "user_list") {
        buildUserListTemplate(data);
    } else {
        addMessageToChat(data);
    }
};

// Закрытие вебсокета
chatSocket.onclose = function (event) {
    console.error('Chat socket closed unexpectedly');
};

// Отправка данных на сервер
function sendMessage(message, userName) {
    chatSocket.send(JSON.stringify({
        'type': 'chat_message',
        'message': message,
        'username': userName
    }));
};

const input = document.getElementById('chat-message-input');
const submitButton = document.getElementById('chat-message-submit');
submitButton.addEventListener('click', function (event) {
    const message = input.value;
    if (message) {
        sendMessage(message, userName)
        input.value = '';
        input.focus();
    }
});
input.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        submitButton.click();
    }
});
input.focus();