const roomName = JSON.parse(
    document.getElementById('room-name').textContent
);
const url = 'ws://' + window.location.host + '/ws/chat/room/' + roomName + '/';
const chatSocket = new WebSocket(url);
chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const chat = document.getElementById("chat");
    chat.innerHTML += '<div class="d-flex flex-row justify-content-start">' + data.message +
        '</div>';
    chat.scrollTop = chat.scrollHeight;
};
chatSocket.onclose = function (event) {
    console.error('Chat socket closed unexpectedly');
};
const input = document.getElementById('chat-message-input');
const submitButton = document.getElementById('chat-message-submit');
submitButton.addEventListener('click', function (event) {
    const message = input.value;
    if (message) {
        chatSocket.send(JSON.stringify({
            'message': message
        }));
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