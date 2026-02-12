// Navigation
function showSection(sectionId) {
    // 1. Mark all as not active (trigger fade out)
    document.querySelectorAll('.section').forEach(sec => {
        sec.classList.remove('active-section');
        // We do NOT set a timeout to hide here because it causes race conditions
        // Instead, we trust the CSS transition opacity: 0
        // We will only set display: none (hidden) after the transition, IF it's not the active one
    });

    // 2. Hide all (display: none) immediately or after delay? 
    // The previous logic was causing the bug. Let's simplify:
    // Hide everything immediately to ensure clean switch, OR handle transitions properly.
    // Simplifying for stability:

    document.querySelectorAll('.section').forEach(sec => {
        sec.classList.add('hidden');
        sec.classList.remove('active-section');
    });

    // 3. Show target
    const target = document.getElementById(sectionId);
    if (target) {
        target.classList.remove('hidden');
        // Force reflow/repaint
        void target.offsetWidth;
        target.classList.add('active-section');
    }

    // Highlight Nav Button
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('onclick').includes(sectionId)) {
            btn.classList.add('active');
        }
    });

    window.scrollTo(0, 0);
}

// Analyzer Logic (Existing)
let currentType = 'url';
function switchTab(type) {
    currentType = type;
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.closest('.tab-btn').classList.add('active');

    const input = document.getElementById('input-content');
    if (type === 'url') {
        input.placeholder = "Paste the suspicious URL here (e.g., http://secure-login.com)...";
    } else {
        input.placeholder = "Paste the suspicious message or email text here...";
    }
}

async function analyzeContent() {
    const content = document.getElementById('input-content').value.trim();
    if (!content) {
        alert("Please enter some content to analyze.");
        return;
    }

    const resultArea = document.getElementById('result-area');
    const loader = document.getElementById('loader');
    const resultContent = document.getElementById('result-content');

    resultArea.classList.remove('hidden');
    loader.classList.remove('hidden');
    resultContent.classList.add('hidden');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: currentType, content: content })
        });

        const data = await response.json();
        displayResult(data);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during analysis.');
    } finally {
        loader.classList.add('hidden');
        resultContent.classList.remove('hidden');
    }
}

function displayResult(data) {
    const riskColorMap = { 'red': '#da3633', 'orange': '#d29922', 'green': '#238636' };
    const circle = document.querySelector('.circle');
    const color = riskColorMap[data.risk_color] || '#c9d1d9';

    circle.style.stroke = color;
    let percentage = Math.min(data.score * 10, 100);
    circle.style.strokeDasharray = `${percentage}, 100`;

    document.querySelector('.percentage').textContent = data.score;
    const riskLabel = document.getElementById('risk-label');
    riskLabel.textContent = data.risk_level;
    riskLabel.style.color = color;

    document.getElementById('recommendation-text').textContent = data.recommendation;

    const detailsList = document.getElementById('analysis-details');
    detailsList.innerHTML = '';

    if (data.details && data.details.length > 0) {
        data.details.forEach(detail => {
            const li = document.createElement('li');
            li.textContent = detail;
            li.style.borderLeftColor = color;
            detailsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = "No obvious red flags detected.";
        li.style.borderLeftColor = riskColorMap['green'];
        detailsList.appendChild(li);
    }
}

// Chatbot Logic
function toggleChat() {
    const chatWindow = document.getElementById('chat-window');
    chatWindow.classList.toggle('hidden');
}

function handleChatInput(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

async function sendChatMessage() {
    const input = document.getElementById('user-msg');
    const message = input.value.trim();
    if (!message) return;

    // Add User Message
    addMessage(message, 'user-message');
    input.value = '';

    // Typing simulated delay?
    // Call API
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();
        addMessage(data.response, 'bot-message');
    } catch (error) {
        addMessage("Sorry, I'm having trouble connecting to the server.", 'bot-message');
    }
}

function addMessage(text, className) {
    const chatMessages = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.classList.add('message', className);
    div.textContent = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
