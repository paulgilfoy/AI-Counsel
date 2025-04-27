// Mock Data (Replace with API call)
const mockCouncilMembers = [
    {
        id: "claude-3-opus", name: "Claude 3 Opus", provider: "Anthropic",
        description: "Most powerful model, best for complex analysis.",
        sprite: "claude.png", isActive: true, systemPrompt: "You are Claude 3 Opus."
    },
    {
        id: "gpt-4-turbo", name: "GPT-4 Turbo", provider: "OpenAI",
        description: "High-level reasoning and creativity.",
        sprite: "gpt4.png", isActive: true, systemPrompt: "You are GPT-4 Turbo."
    },
    {
        id: "gemini-1.5-pro", name: "Gemini 1.5 Pro", provider: "Google",
        description: "Strong multimodal capabilities.",
        sprite: "gemini.png", isActive: true, systemPrompt: "You are Gemini 1.5 Pro."
    },
    {
        id: "llama-3-70b", name: "Llama 3 70B", provider: "Meta",
        description: "Open source model, good for general tasks.",
        sprite: "llama.png", isActive: false, systemPrompt: "You are Llama 3."
    }
];

// Available placeholder sprites (using files from static/images)
const placeholderSprites = [
    "grok1.jpeg",
    "gemini3.jpeg",
    "gemini2.jpeg",
    "Gemini1.jpeg",
    "chatgpt1.webp",
    "grok4.jpeg"
];

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

// Council Members Section Management
class CouncilMembersUI {
    constructor() {
        this.gridContainer = document.getElementById('council-members-grid');
        this.cardTemplate = document.getElementById('council-member-card-template');
        this.members = [];
        
        // Modal elements
        this.modal = document.getElementById('prompt-modal');
        this.modalMemberName = document.getElementById('modal-member-name');
        this.modalMemberId = document.getElementById('modal-member-id');
        this.modalSystemPrompt = document.getElementById('modal-system-prompt');
        this.modalStatusIndicator = document.getElementById('modal-status-indicator');
        this.modalCloseButton = document.getElementById('modal-close-button');
        this.modalCancelButton = document.getElementById('modal-cancel-button');
        this.promptForm = document.getElementById('prompt-form');
        
        this.init();
    }

    async init() {
        this.loadState();
        if (this.members.length === 0) {
            // Load initial data if no state saved
            // In real app, fetch from /api/council-members
            this.members = mockCouncilMembers.map((m, index) => ({ ...m, order: index }));
            this.saveState();
        }
        this.render();
        this.setupEventListeners();
    }

    loadState() {
        const savedState = localStorage.getItem('councilMembersState');
        if (savedState) {
            this.members = JSON.parse(savedState);
        } else {
            this.members = [];
        }
    }

    saveState() {
        localStorage.setItem('councilMembersState', JSON.stringify(this.members));
    }

    render() {
        this.gridContainer.innerHTML = ''; // Clear existing cards
        
        // Sort members: active first, then by original order
        const sortedMembers = [...this.members].sort((a, b) => {
            if (a.isActive !== b.isActive) {
                return a.isActive ? -1 : 1; // Active members first
            }
            return a.order - b.order; // Maintain original relative order
        });

        sortedMembers.forEach((member, index) => { // Pass index to createCard
            const card = this.createCard(member, index);
            this.gridContainer.appendChild(card);
        });
    }

    createCard(member, index) { // Added index parameter
        const card = this.cardTemplate.content.cloneNode(true).children[0];
        card.dataset.memberId = member.id;
        card.querySelector('.member-name').textContent = member.name;
        card.querySelector('.member-provider').textContent = member.provider;
        card.querySelector('.member-prompt').textContent = member.systemPrompt;
        
        const spriteContainer = card.querySelector('.sprite-container');
        
        // Use placeholder sprite based on index, cycling through available images
        const spriteFilename = placeholderSprites[index % placeholderSprites.length];
        spriteContainer.style.backgroundImage = `url(/static/images/${spriteFilename})`;
        spriteContainer.style.backgroundSize = 'cover'; // Adjust as needed
        spriteContainer.style.backgroundPosition = 'center';

        // Apply animation state based on isActive (placeholder)
        spriteContainer.dataset.state = member.isActive ? 'idle' : 'idle'; // Could add 'inactive' state later

        const statusIndicator = card.querySelector('.member-status-indicator');
        
        if (member.isActive) {
            card.classList.add('active');
            card.classList.remove('inactive');
            statusIndicator.title = 'Active';
        } else {
            card.classList.add('inactive');
            card.classList.remove('active');
            statusIndicator.title = 'Inactive';
        }

        return card;
    }

    setupEventListeners() {
        // Grid click listener (delegated)
        this.gridContainer.addEventListener('click', (e) => {
            const card = e.target.closest('.council-member-card');
            if (!card) return;
            
            const memberId = card.dataset.memberId;

            // Check if the click was on the status indicator within the card
            if (e.target.classList.contains('card-status-indicator')) {
                e.stopPropagation(); // Prevent opening modal when clicking indicator
                this.toggleCardActivation(memberId);
            } else {
                // Click was on the card itself (but not the indicator), open modal
                this.openPromptModal(memberId);
            }
        });

        // Modal listeners
        this.modalCloseButton.addEventListener('click', () => this.closePromptModal());
        this.modalCancelButton.addEventListener('click', () => this.closePromptModal());
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closePromptModal();
            }
        });
        
        // New listener for status indicator click
        this.modalStatusIndicator.addEventListener('click', () => {
            // Toggle the visual state immediately for feedback
            const isActive = this.modalStatusIndicator.classList.toggle('active');
            this.modalStatusIndicator.classList.toggle('inactive', !isActive);
        });

        // Form submission
        this.promptForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handlePromptSave();
        });
    }

    // New method to handle direct activation toggle from card
    toggleCardActivation(memberId) {
        const memberIndex = this.members.findIndex(m => m.id === memberId);
        if (memberIndex !== -1) {
            const newState = !this.members[memberIndex].isActive;
            this.members[memberIndex].isActive = newState;
            // TODO: Add API call POST /api/council-members/{id}/toggle
            console.log(`Toggled card activation for ${memberId} to ${newState}`);
            this.saveState();
            this.render(); // Re-render to reflect the change and order
        }
    }

    openPromptModal(memberId) {
        const member = this.members.find(m => m.id === memberId);
        if (!member) return;

        this.modalMemberId.value = member.id;
        this.modalMemberName.textContent = member.name;
        this.modalSystemPrompt.value = member.systemPrompt;
        
        // Set initial state for the indicator
        const isActive = member.isActive;
        this.modalStatusIndicator.classList.toggle('active', isActive);
        this.modalStatusIndicator.classList.toggle('inactive', !isActive);

        this.modal.classList.add('visible');
        this.modal.classList.remove('hidden');
    }

    closePromptModal() {
        this.modal.classList.remove('visible');
        // Use timeout to allow animation before hiding
        setTimeout(() => {
             if (!this.modal.classList.contains('visible')) { // Check again in case reopened quickly
                this.modal.classList.add('hidden');
             }
        }, 300); // Match CSS transition duration
    }

    handlePromptSave() {
        const memberId = this.modalMemberId.value;
        const newPrompt = this.modalSystemPrompt.value;
        // Read the state the user *left* the indicator in
        let newActiveState = this.modalStatusIndicator.classList.contains('active');

        const memberIndex = this.members.findIndex(m => m.id === memberId);
        if (memberIndex !== -1) {
            let stateChanged = false;
            const originalPrompt = this.members[memberIndex].systemPrompt;
            const originalActiveState = this.members[memberIndex].isActive;

            // Check if prompt changed
            if (originalPrompt !== newPrompt) {
                this.members[memberIndex].systemPrompt = newPrompt;
                // Default to active if prompt was edited
                newActiveState = true; 
                console.log(`Updated prompt for ${memberId}, defaulting to active.`);
                stateChanged = true;
            }

            // Check if active state changed (either by user toggle or default above)
            if (originalActiveState !== newActiveState) {
                this.members[memberIndex].isActive = newActiveState;
                // TODO: API call
                console.log(`Toggled active state for ${memberId} to ${newActiveState}`);
                stateChanged = true;
            } else if (stateChanged && !newActiveState) {
                // If prompt changed but user explicitly set to inactive, ensure it's saved
                this.members[memberIndex].isActive = false;
                console.log(`Prompt updated for ${memberId}, but kept inactive as requested.`);
            }

            if (stateChanged) {
                this.saveState();
                this.render(); // Re-render
            }
        }

        this.closePromptModal();
    }
}

// Chat Interface (modified to use CouncilMembersUI for active members)
class ChatInterface {
    constructor(councilMembersUI) { // Changed constructor parameter
        this.councilMembersUI = councilMembersUI; // Store reference
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

            // Get active models from CouncilMembersUI
            const activeModels = this.councilMembersUI.members
                .filter(m => m.isActive)
                .map(m => m.id);

            if (activeModels.length === 0) {
                this.addMessage('system', 'System', 'No council members are active. Please activate at least one.');
                return;
            }

            try {
                // Pass active_models to the API
                const response = await this.sendMessage(message, activeModels);
                
                // Update character state (if AICouncilUI is still used elsewhere)
                // response.forEach(reply => {
                //     if (this.aiCouncil) { // Check if aiCouncil exists
                //         this.aiCouncil.updateCharacterState(reply.model_id, 'speaking');
                //         setTimeout(() => {
                //             this.aiCouncil.updateCharacterState(reply.model_id, 'idle');
                //         }, 1000); 
                //     }
                //     this.addMessage('ai', reply.model_name, reply.content);
                // });
                // Simplified message display for now
                response.forEach(reply => {
                     this.addMessage('ai', reply.model_name, reply.content);
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
        // Basic markdown rendering (bold and italic)
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        contentDiv.innerHTML = content; // Use innerHTML to render basic markdown
        
        messageDiv.appendChild(authorDiv);
        messageDiv.appendChild(contentDiv);
        this.chatContainer.appendChild(messageDiv);
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    // Modified sendMessage to include active_models
    async sendMessage(message, activeModels) {
        const response = await fetch('/api/discussions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            // Send message and active_models list
            body: JSON.stringify({ message, active_models: activeModels }), 
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(`Failed to send message: ${errorData.detail || response.statusText}`);
        }

        return response.json();
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    // Removed AICouncilUI initialization as it's not used for chat display anymore
    // const aiCouncil = new AICouncilUI(); 
    const councilMembersUI = new CouncilMembersUI();
    const chat = new ChatInterface(councilMembersUI); // Pass councilMembersUI to ChatInterface
}); 