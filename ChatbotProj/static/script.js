const chatContainer = document.getElementById("chat-container");
const msgInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const typingIndicator = document.getElementById("typing-indicator");

function addMessage(text, sender, latencyMs = null) {
    const container = document.createElement("div");
    container.classList.add("msg", sender);

    // Create avatar image
    const avatar = document.createElement("img");
    avatar.classList.add("avatar");
    avatar.src = sender === "bot" ? "/static/BotIcon.png" : "/static/UserIcon.png";
    container.appendChild(avatar);

    // Create message div
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message-text");
    messageDiv.innerHTML = text;
    container.appendChild(messageDiv);

    // Latency Footnote
    if (latencyMs !== null && sender === "bot") {
        const footnote = document.createElement("div");
        footnote.classList.add("bot-footnote");
        footnote.textContent = `Responded in ${latencyMs.toFixed(0)} ms`;
        messageDiv.appendChild(footnote);
    }

    chatContainer.appendChild(container);
    chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
}

async function sendMessage() {
    const text = msgInput.value.trim();
    if (!text) return;

    addMessage(text, "user");
    msgInput.value = "";

    // Show typing indicator
    typingIndicator.style.display = "block";
    const startTime = performance.now();

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ message: text, session_id: "user123" })
        });
        // parse response
        const data = await response.json();
        const latency = performance.now() - startTime;

        // Hide typing indicator
        typingIndicator.style.display = "none";

        // pass latency to addMessage
        addMessage(data.reply, "bot", latency);
    } catch (err) {
        typingIndicator.style.display = "none";
        addMessage("Error: Unable to get response.", "bot");
        console.error(err);
    }
}

msgInput.focus();
sendBtn.onclick = sendMessage;
msgInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});


// Theme Stuff
window.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("chatTheme");
    if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
        themeBtn.textContent = "Light Mode";
    } else {
        document.body.classList.remove("dark-theme");
        themeBtn.textContent = "Dark Mode";
    }
});

const themeBtn = document.getElementById("theme-btn");
    themeBtn.onclick = () => {
        document.body.classList.toggle("dark-theme");
        if(document.body.classList.contains("dark-theme"))
        {
            themeBtn.textContent = "Light Mode";
            localStorage.setItem("chatTheme", "dark");
        }
        else
        {
            themeBtn.textContent = "Dark Mode";
            localStorage.setItem("chatTheme", "light");
        }
    };