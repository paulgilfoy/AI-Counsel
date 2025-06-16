// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const modelList = document.getElementById('model-list');

// State
let activeModels = [];

// Initialize
async function initialize() {
    try {
        // Get available models
        const response = await fetch('/api/models');
        const data = await response.json();
        
        if (data.status === 'success') {
            // Initialize all models as active
            activeModels = data.models;
            renderModelList();
        }
    } catch (error) {
        console.error('Error initializing:', error);
        addMessage('System', 'Error initializing the application. Please refresh the page.');
    }
}

// Render model list
function renderModelList() {
    modelList.innerHTML = '';
    activeModels.forEach(model => {
        const checkbox = document.createElement('div');
        checkbox.className = 'form-check';
        checkbox.innerHTML = `
            <input class="form-check-input" type="checkbox" value="${model}" id="model-${model}" checked>
            <label class="form-check-label" for="model-${model}">
                ${model}
            </label>
        `;
        modelList.appendChild(checkbox);
    });
}

// Add message to chat
function addMessage(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.innerHTML = `
        <strong>${sender}:</strong>
        <p>${message}</p>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Get active models from checkboxes
function getActiveModels() {
    return Array.from(document.querySelectorAll('.form-check-input:checked')).map(cb => cb.value);
}

// Send message
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addMessage('You', message);
    userInput.value = '';

    // Get active models
    const models = getActiveModels();
    if (models.length === 0) {
        addMessage('System', 'Please select at least one model to continue.');
        return;
    }

    try {
        // Send message to backend
        const response = await fetch('/api/discuss', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                topic: message,
                active_models: models
            })
        });

        const data = await response.json();
        
        if (data.status === 'success') {
            // Add AI responses to chat
            Object.entries(data.results).forEach(([model, response]) => {
                addMessage(model, response);
            });
        } else {
            addMessage('System', `Error: ${data.message}`);
        }
    } catch (error) {
        console.error('Error sending message:', error);
        addMessage('System', 'Error sending message. Please try again.');
    }
}

// Event Listeners
sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Initialize the application
initialize(); 