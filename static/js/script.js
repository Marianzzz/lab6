document.getElementById('chat-form').addEventListener('submit', function (event) {
    event.preventDefault();
    let message = document.getElementById('user-message').value;
    sendMessage(message);
});

function sendMessage(message) {
    fetch('/message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({message: message})
    })
        .then(response => response.json())
        .then(data => {
            displayResponse(data.response, data.message_type);
        });
}

function displayResponse(response, message_type) {
    var chatResponse = document.getElementById('chat-response');
    var responseElement = document.createElement('p');
    responseElement.textContent = response;
    if (message_type === 'user') {
        responseElement.classList.add('user-message');
    } else if (message_type === 'bot') {
        responseElement.classList.add('bot-message');
    }

    chatResponse.appendChild(responseElement);
}