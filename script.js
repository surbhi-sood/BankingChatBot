// Web socket initialization
var ws = new WebSocket("ws://localhost:8000");

// Close socket when window closes
$(window).on('beforeunload', function() {
    ws.close();
});

// This code reloads the page (location.reload()) to restart the connection and recover from the error
ws.onerror = function(event) {
    location.reload();
}

/* It extracts the received message from event.data and calls the chat_add_message()
function to display the message in the chat history */
ws.onmessage = function(event) {
    var message_received = event.data;
    chat_add_message(message_received, false);
};

// Add a message to the chat history
function chat_add_message(message, isUser) {
    var class_suffix = isUser ? '_user' : '';
    var html = '';

    if (isSuggestedQuestion(message)) {
        var questions = message.split("\n");
        html += '<div class="chat_line">';
        html += '<div class="chat_bubble' + class_suffix + '">';
        html += '<div class="chat_triangle' + class_suffix + '"></div>';

        for (var i = 0; i < questions.length; i++) {
            var question = questions[i];
            html += '<button class="suggested_question" onclick="sendSuggestedQuestion(\'' + question + '\')">' + question + '</button>';
        }

        html += '</div>';
        html += '</div>';
    } else {
        html += '<div class="chat_line">';
        html += '<div class="chat_bubble' + class_suffix + '">';
        html += '<div class="chat_triangle' + class_suffix + '"></div>';
        html += message;
        html += '</div>';
        html += '</div>';
    }

    chat_add_html(html);
}

// Add HTML to the chat history
function chat_add_html(html) {
    $("#chat_log").append(html);
    chat_scrolldown();
}

// Scrolls the chat history to the bottom
function chat_scrolldown() {
    $("#chat_log").animate({
        scrollTop: $("#chat_log")[0].scrollHeight
    }, 500);
}

// If press ENTER, talk to chat and send message to server
$(function() {
    $('#chat_input').on('keypress', function(event) {
        if (event.which === 13 && $(this).val() != "") {
            var message = $(this).val();
            $(this).val("");
            chat_add_message(message, true);
            ws.send(message);
        }
    });
});

// Check if the message is a suggested question
function isSuggestedQuestion(message) {
    return message.includes("Suggested Questions\n");
}

// Send the selected suggested question as the next question
function sendSuggestedQuestion(question) {
    chat_add_message(question, true);
    ws.send(question);
}
