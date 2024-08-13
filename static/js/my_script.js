const roomId = JSON.parse(
    document.getElementById('room-id').textContent
);
const url = 'ws://' + window.location.host + '/ws/chat/room/' + roomId + '/';
const chatSocket = new WebSocket(url);
chatSocket.onmessage = function (event) {
    const data = JSON.parse(event.data);
    const chat = document.getElementById("chat");
    chat.innerHTML += '<div class="card text-bg-info mb-3 p-2 style="max-width: 18rem;">' + data.message +
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