document.addEventListener("DOMContentLoaded", () => {
  const chatbotHTML = `
    <div class="chatbot">
      <div class="chatbot-header">Relief Assistant</div>
      <div class="chatbot-body" id="chat-body">
        <div class="bot-msg">👋 Hi! I’m your rescue assistant. How can I help?</div>
      </div>
      <div class="chatbot-input">
        <input type="text" id="chat-input" placeholder="Type your message..." />
        <button id="send-btn">Send</button>
      </div>
    </div>
    <button class="chatbot-toggle">💬</button>
  `;

  document.getElementById("chatbot-container").innerHTML = chatbotHTML;

  const toggleBtn = document.querySelector(".chatbot-toggle");
  const chatbot = document.querySelector(".chatbot");
  const input = document.getElementById("chat-input");
  const chatBody = document.getElementById("chat-body");

  toggleBtn.addEventListener("click", () => chatbot.classList.toggle("open"));
  document.getElementById("send-btn").addEventListener("click", sendMessage);

  function sendMessage() {
    const msg = input.value.trim();
    if (!msg) return;
    appendMsg("user", msg);
    input.value = "";
    setTimeout(() => {
      appendMsg("bot", getBotReply(msg));
    }, 500);
  }

  function appendMsg(sender, text) {
    const div = document.createElement("div");
    div.className = sender === "user" ? "user-msg" : "bot-msg";
    div.textContent = text;
    chatBody.appendChild(div);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function getBotReply(msg) {
    msg = msg.toLowerCase();
    if (msg.includes("help")) return "🚨 Please stay calm. Emergency teams are being notified.";
    if (msg.includes("fire")) return "🔥 Fire alert reported. Stay away from danger zones.";
    if (msg.includes("flood")) return "🌊 Flood alert detected. Move to higher ground immediately.";
    if (msg.includes("contact")) return "📞 Call our emergency line: +91 999-888-7777.";
    return "🤖 I'm here to help! Try asking about fire, flood, or emergency support.";
  }
});
