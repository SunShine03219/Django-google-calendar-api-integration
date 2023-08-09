const roomName          = JSON.parse(document.getElementById('json-roomname').textContent)
const userName          = JSON.parse(document.getElementById('json-username').textContent)

const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

chatSocket.onopen = function(e){
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.message) {

        console.log(data.username)
        console.log(userName)
        let html ='<li class='
        if (data.username === userName)
        {
            html += '"sender" ><p>' + data.message + '</p></li>';
        }
        else 
        {
            html += '"reply" ><p>' + data.message + '</p></li>';
        }
        
        const chatMessages = document.querySelector('#chat-messages');
        chatMessages.insertAdjacentHTML('beforeend', html);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    } else {
        alert('Message empty');
    }
    var element = document.getElementById("modal-body");
    element.scrollTop = element.scrollHeight;
}

chatSocket.onclose = function(e){
    console.log('onclose')
}

// Define a function to send a message over the socket
function sendMessage() {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    console.log(chatSocket);

    chatSocket.send(JSON.stringify({
    'message': message,
    'username': userName,
    'room': roomName,
    }));

    messageInputDom.value = '';
    var element = document.getElementById("modal-body");
    element.scrollTop = element.scrollHeight;
}

// Attach the sendMessage function to the submit button click event
const messageSubmitDom = document.querySelector('#chat-message-submit');
messageSubmitDom.addEventListener('click', function(e) {
    e.preventDefault();
    sendMessage();
    return false;
});

// Attach the sendMessage function to the input element keydown event
const messageInputDom = document.querySelector('#chat-message-input');
messageInputDom.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
    return false;
    }
});

// Get the chat box element
var chatBox = document.getElementById("chat-messages");

// Append the new message to the chat
var newMessage = document.createElement("li");
// ... code to set the contents of the new message ...
chatBox.appendChild(newMessage);

// Scroll the chat box to the bottom
chatBox.scrollTop = chatBox.scrollHeight;

jQuery(document).ready(function() {
    $(".chat-list a").click(function() {
        $(".chatbox").addClass('showbox');
        return false;
    });

    $(".chat-icon").click(function() {
        $(".chatbox").removeClass('showbox');
    });
});


function scrollToBottom() {
    var element = document.getElementById("modal-body-chat");
    element.scrollTop = element.scrollHeight;
  }
  
  window.onload = function() {
    scrollToBottom();
  };
  
  document.getElementById("chat-message-submit").addEventListener("click", function(event) {
    event.preventDefault();
    // Your code to handle sending the message (e.g., AJAX request to the server)
    scrollToBottom();
  });
  
  document.getElementById("chat-message-input").addEventListener("keydown", function(event) {
    if (event.keyCode === 13) {
      event.preventDefault(); 
      scrollToBottom();
    }
  });
  

  
  