// AI Council Management
class AICouncilUI {
    constructor() {
        this.councilContainer = document.getElementById('ai-council');
        this.characterTemplate = document.getElementById('ai-character-template');
        this.characters = new Map();
        this.init();
    }

    async init() {
        try {
            const response = await fetch('/api/models');
            const models = await response.json();
            this.setupCharacters(models);
        } catch (error) {
            console.error('Failed to fetch AI models:', error);
        }
    }

    setupCharacters(models) {
        models.forEach(model => {
            const character = this.createCharacter(model);
            this.characters.set(model.id, character);
            this.councilContainer.appendChild(character);
        });
    }

    createCharacter(model) {
        const element = this.characterTemplate.content.cloneNode(true).children[0];
        const sprite = element.querySelector('.sprite-container');
        const name = element.querySelector('h3');
        const status = element.querySelector('.status');

        sprite.style.backgroundImage = `url(/static/images/${model.sprite})`;
        sprite.dataset.state = 'idle';
        name.textContent = model.name;
        status.textContent = 'Idle';

        return element;
    }

    updateCharacterState(modelId, state) {
        const character = this.characters.get(modelId);
        if (!character) return;

        const sprite = character.querySelector('.sprite-container');
        const status = character.querySelector('.status');
        
        sprite.dataset.state = state;
        status.textContent = state.charAt(0).toUpperCase() + state.slice(1);
    }
}

// Chat Interface
class ChatInterface {
    constructor(aiCouncil) {
        this.aiCouncil = aiCouncil;
        this.chatContainer = document.getElementById('chat-container');
        this.chatForm = document.getElementById('chat-form');
        this.userInput = document.getElementById('user-input');
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = this.userInput.value.trim();
            if (!message) return;

            this.addMessage('user', 'You', message);
            this.userInput.value = '';

            try {
                const response = await this.sendMessage(message);
                response.forEach(reply => {
                    this.aiCouncil.updateCharacterState(reply.model_id, 'speaking');
                    this.addMessage('ai', reply.model_name, reply.content);
                    setTimeout(() => {
                        this.aiCouncil.updateCharacterState(reply.model_id, 'idle');
                    }, 1000);
                });
            } catch (error) {
                console.error('Failed to send message:', error);
                this.addMessage('system', 'System', 'Failed to send message. Please try again.');
            }
        });
    }

    addMessage(type, author, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const authorDiv = document.createElement('div');
        authorDiv.className = 'author';
        authorDiv.textContent = author;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'content';
        contentDiv.textContent = content;
        
        messageDiv.appendChild(authorDiv);
        messageDiv.appendChild(contentDiv);
        this.chatContainer.appendChild(messageDiv);
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    async sendMessage(message) {
        const response = await fetch('/api/discussions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) {
            throw new Error('Failed to send message');
        }

        return response.json();
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    const aiCouncil = new AICouncilUI();
    const chat = new ChatInterface(aiCouncil);
}); 