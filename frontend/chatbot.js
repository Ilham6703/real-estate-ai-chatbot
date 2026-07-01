// ==========================================
// Configuration
// ==========================================

const API_URL = "http://127.0.0.1:8000/chat";

// ==========================================
// Elements
// ==========================================

const chatToggle = document.getElementById("chat-toggle");
const chatContainer = document.getElementById("chat-container");
const closeChat = document.getElementById("close-chat");

const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-btn");

const typingIndicator = document.getElementById("typing-indicator");

const suggestions = document.querySelectorAll(".suggestion");

// ==========================================
// Open Chat
// ==========================================

chatToggle.addEventListener("click", () => {

    chatContainer.classList.remove("hidden");

    chatToggle.classList.add("hidden");

});

// ==========================================
// Close Chat
// ==========================================

closeChat.addEventListener("click", () => {

    chatContainer.classList.add("hidden");

    chatToggle.classList.remove("hidden");

});

// ==========================================
// Create Message
// ==========================================

function addMessage(text, sender) {

    const message = document.createElement("div");

    message.classList.add("message");

    message.classList.add(sender);

    message.textContent = text;

    chatBox.appendChild(message);

    scrollToBottom();

}

// ==========================================
// Scroll
// ==========================================

function scrollToBottom() {

    chatBox.scrollTop = chatBox.scrollHeight;

}

// ==========================================
// Typing Indicator
// ==========================================

function showTyping() {

    typingIndicator.classList.remove("hidden");

    scrollToBottom();

}

function hideTyping() {

    typingIndicator.classList.add("hidden");

}

// ==========================================
// Send Request
// ==========================================

async function sendMessage(message) {

    if (!message.trim()) return;

    addMessage(message, "user");

    userInput.value = "";
    // Hide welcome section after first message

    chatContainer.classList.add("hide-home");

    showTyping();

    // ---------------------------------------
    // Session Memory
    // ---------------------------------------

    let sessionId = localStorage.getItem("session_id");

    if (!sessionId) {

        sessionId = crypto.randomUUID();

        localStorage.setItem("session_id", sessionId);

    }

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                session_id: sessionId,

                message: message

            })

        });

        const data = await response.json();

        hideTyping();

        addMessage(data.response, "bot");

    }

    catch (error) {

        hideTyping();

        addMessage(

            "Sorry, something went wrong. Please try again.",

            "bot"

        );

        console.error(error);

    }

}

// ==========================================
// Send Button
// ==========================================

sendButton.addEventListener("click", () => {

    sendMessage(userInput.value);

});

// ==========================================
// Enter Key
// ==========================================

userInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {

        sendMessage(userInput.value);

    }

});

// ==========================================
// Suggestion Chips
// ==========================================

suggestions.forEach(button => {

    button.addEventListener("click", () => {

        sendMessage(button.textContent);

    });

});