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
        await this.loadCouncilData(); // Fetch data from API instead of mock/localStorage
        this.render();
        this.setupEventListeners();
    }

    async loadCouncilData() {
        try {
            console.log("Fetching council data...");
            const [modelsRes, currentPromptsRes, defaultPromptsRes] = await Promise.all([
                fetch('/api/models'),
                fetch('/api/prompts'),
                fetch('/api/models/defaults')
            ]);

            if (!modelsRes.ok || !currentPromptsRes.ok || !defaultPromptsRes.ok) {
                throw new Error('Failed to fetch council data from API');
            }

            const modelsData = await modelsRes.json();
            const currentPromptsData = await currentPromptsRes.json();
            const defaultPromptsData = await defaultPromptsRes.json();

            const models = modelsData.models || []; // ['ChatGPT', 'Claude', ...]
            const currentPrompts = currentPromptsData.prompts || {}; // { 'ChatGPT': 'current prompt', ... }
            this.defaultPrompts = defaultPromptsData.defaults || {}; // Store defaults { 'ChatGPT': 'default prompt', ... }

            // Try loading saved state (isActive, order) from localStorage
            const savedState = localStorage.getItem('councilMembersState');
            let persistedState = {};
            if (savedState) {
                try {
                    persistedState = JSON.parse(savedState).reduce((acc, member) => {
                        acc[member.id] = { isActive: member.isActive, order: member.order };
                        return acc;
                    }, {});
                } catch (e) {
                    console.error("Failed to parse saved state:", e);
                    localStorage.removeItem('councilMembersState'); // Clear corrupted state
                }
            }

            this.members = models.map((modelId, index) => {
                const state = persistedState[modelId] || {}; // Get saved state or empty object
                return {
                    id: modelId,
                    name: modelId, // Use ID as name for now, could enhance API later
                    provider: "Unknown", // Add provider info to API later if needed
                    // Use current prompt from API, fallback to default if missing
                    systemPrompt: currentPrompts[modelId] !== undefined ? currentPrompts[modelId] : this.defaultPrompts[modelId],
                    isActive: state.isActive !== undefined ? state.isActive : true, // Default to active if no saved state
                    order: state.order !== undefined ? state.order : index, // Use saved order or default index
                    // sprite: TBD - assign based on name or get from API
                };
            });

            console.log("Council data loaded:", this.members);
            this.saveState(); // Save the potentially merged/updated state

        } catch (error) {
            console.error('Failed to initialize council members UI:', error);
            this.gridContainer.innerHTML = '<p class="error">Failed to load council members. Please try refreshing.</p>';
            // Fallback to empty or mock data if needed?
            this.members = []; // Set to empty on error
        }
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

    async handlePromptSave() {
        const memberId = this.modalMemberId.value;
        const newPromptText = this.modalSystemPrompt.value;
        const memberIndex = this.members.findIndex(m => m.id === memberId);
        const modalIsActive = this.modalStatusIndicator.classList.contains('active');

        if (memberIndex === -1) {
            console.error("Member not found:", memberId);
            this.closePromptModal();
            return;
        }

        const originalMember = this.members[memberIndex];
        const promptChanged = originalMember.systemPrompt !== newPromptText;
        const statusChanged = originalMember.isActive !== modalIsActive;

        // 1. Save Prompt via API if it changed
        if (promptChanged) {
            try {
                console.log(`Updating prompt for ${memberId}...`);
                const response = await fetch('/api/prompts', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ prompts: { [memberId]: newPromptText } }),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
                }

                console.log(`Prompt for ${memberId} updated successfully.`);
                // Update local state only after successful API call
                this.members[memberIndex].systemPrompt = newPromptText;

            } catch (error) {
                console.error('Failed to save prompt:', error);
                alert(`Error saving prompt: ${error.message}`);
                // Optionally, don't close the modal or revert changes on error
                return; // Stop processing if prompt save fails
            }
        }

        // 2. Handle Activation State Change if it changed
        if (statusChanged) {
            // This logic already exists in toggleCardActivation, reuse or call it
            // For now, update local state directly and add TODO for API call
            this.members[memberIndex].isActive = modalIsActive;
            // TODO: Implement API call in toggleCardActivation (e.g., POST /api/council-members/{id}/toggle)
            // For now, just log it
            console.log(`Status for ${memberId} changed to ${modalIsActive} in modal. API call needed.`);
        }
        
        // If the prompt was edited, default member to active if it wasn't already
        if (promptChanged && !originalMember.isActive && !modalIsActive) {
             console.log(`Prompt edited for inactive member ${memberId}. Setting to active.`);
             this.members[memberIndex].isActive = true;
             // TODO: This state change also needs an API call
             console.log(`Status for ${memberId} implicitly changed to active. API call needed.`);
        }

        // 3. Save state locally and re-render
        this.saveState(); // Save combined changes (prompt + potential status)
        this.render();
        this.closePromptModal();
    }
}

// Chat Interface (modified to use CouncilMembersUI for active members)
class ChatInterface {
    constructor(councilMembersUI) { // Changed constructor parameter
        this.chatMessages = document.getElementById('chat-messages');
        this.startDiscussionForm = document.getElementById('start-discussion-form');
        this.discussionTopicInput = document.getElementById('discussion-topic-input');
        this.startDiscussionButton = document.getElementById('start-discussion-button');
        this.startDiscussionStatus = document.getElementById('start-discussion-status');
        this.chatForm = document.getElementById('chat-form'); // Follow-up form
        this.userInput = document.getElementById('user-input');
        this.sendButton = this.chatForm.querySelector('button[type="submit"]'); // Adjust if needed
        this.councilMembersUI = councilMembersUI; // Store reference
        this.currentDiscussionId = null;

        this.placeholderSprites = ["grok1.jpeg", "gemini3.jpeg", "gemini2.jpeg", "Gemini1.jpeg", "chatgpt1.webp", "grok4.jpeg"]; // Keep placeholder list

        this.setupEventListeners();
        this.showInitialState(); // Show start form initially
    }

    setupEventListeners() {
        // Listener for the initial discussion form
        this.startDiscussionForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const topic = this.discussionTopicInput.value.trim();
            if (topic) {
                this.startNewDiscussion(topic);
            }
        });

        // Listener for the follow-up message form
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSendMessage();
        });
    }

    showInitialState() {
        this.chatMessages.innerHTML = '<p class="text-center text-gray-500">Start a new discussion below.</p>'; // Placeholder message
        this.startDiscussionForm.style.display = 'flex'; // Show start form
        this.startDiscussionStatus.style.display = 'block'; // Show status for start form
        this.chatForm.style.display = 'none'; // Hide follow-up form
        this.currentDiscussionId = null;
    }

    showChattingState() {
        this.startDiscussionForm.style.display = 'none'; // Hide start form
        this.startDiscussionStatus.style.display = 'none'; // Hide status for start form
        this.chatForm.style.display = 'flex'; // Show follow-up form
    }

    setStartDiscussionStatus(message, isError = false) {
        this.startDiscussionStatus.textContent = message;
        this.startDiscussionStatus.className = `mt-3 text-sm ${isError ? 'text-red-400' : 'text-gray-400'}`;
    }

    async startNewDiscussion(topic) {
        console.log(`Starting new discussion with topic: ${topic}`);
        this.setStartDiscussionStatus('Starting discussion...', false);
        this.startDiscussionButton.disabled = true;
        this.discussionTopicInput.disabled = true;

        // 1. Get active models from CouncilMembersUI
        const activeModels = this.councilMembersUI.getActiveMemberIds();
        if (activeModels.length === 0) {
            this.setStartDiscussionStatus('Error: Please activate at least one council member.', true);
            this.startDiscussionButton.disabled = false;
            this.discussionTopicInput.disabled = false;
            return;
        }
        console.log('Active models:', activeModels);

        try {
            // 2. Call API to start discussion
            const response = await fetch('/api/discussions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    topic: topic,
                    active_models: activeModels
                }),
            });

            const data = await response.json();
            console.log('API Response:', data);

            if (!response.ok) {
                throw new Error(data.error || 'Failed to start discussion');
            }

            // 3. Clear initial message and add user's topic
            this.chatMessages.innerHTML = ''; // Clear the 'Start a new discussion' placeholder
            this.addMessage('user', 'You', topic); 

            // 4. Display results
            this.currentDiscussionId = data.discussion_id;
            this.displayDiscussionResults(data.results);

            // 5. Update UI state
            this.setStartDiscussionStatus('Discussion started successfully.', false);
            this.discussionTopicInput.value = ''; // Clear the input
            this.showChattingState(); // Switch to follow-up input

        } catch (error) {
            console.error('Error starting discussion:', error);
            this.setStartDiscussionStatus(`Error: ${error.message}`, true);
        } finally {
            // Re-enable the form elements in case of error, but keep disabled if successful
            if (this.startDiscussionForm.style.display !== 'none') {
                 this.startDiscussionButton.disabled = false;
                 this.discussionTopicInput.disabled = false;
            }
        }
    }

    displayDiscussionResults(results) {
        console.log('Displaying discussion results:', results);
        if (!results || results.length === 0) {
            // Handle cases where the API might return empty results initially
            // Maybe add a system message? 
            this.addMessage('system', 'System', 'Waiting for responses...');
            return;
        }
        // Assuming results is an array of message objects like: 
        // [{ role: 'assistant', name: 'ModelName', content: '...' }, ...]
        // Or potentially nested rounds
        results.forEach(message => {
            if (message.role === 'assistant' && message.name && message.content) {
                 this.addMessage('ai', message.name, message.content);
            } else if (message.role === 'user' && message.content) {
                // Might not receive user messages back in initial results, but handle if we do
                this.addMessage('user', 'You', message.content);
            } else {
                 console.warn("Received unknown message format: ", message);
                 this.addMessage('system', 'System', `Received message from ${message.name || 'Unknown'}`);
            }
        });
    }

    async handleSendMessage() {
        const messageContent = this.userInput.value.trim();
        if (!messageContent || !this.currentDiscussionId) {
            console.log("Cannot send message: Empty content or no active discussion.");
            return; // Don't send empty messages or if no discussion is active
        }

        console.log(`Sending message: ${messageContent} to discussion ${this.currentDiscussionId}`);

        // 1. Add user message immediately to UI
        this.addMessage('user', 'You', messageContent);
        this.userInput.value = ''; // Clear input field
        this.sendButton.disabled = true;
        this.userInput.disabled = true;

        try {
            // 2. Call API to contribute to the discussion
             const response = await fetch(`/api/discussions/${this.currentDiscussionId}/contribute`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ contribution: messageContent }),
            });

            const data = await response.json();
            console.log('API Response for contribution:', data);

            if (!response.ok) {
                throw new Error(data.error || 'Failed to send message');
            }

            // 3. Display new AI responses
            if (data.results) {
                 this.displayDiscussionResults(data.results); // Display the new round of AI responses
            } else {
                 this.addMessage('system', 'System', 'Received confirmation, waiting for next round...');
            }

        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('system', 'System', `Error sending message: ${error.message}`);
            // Optional: Re-enable input on error or add the failed message back?
        } finally {
            this.sendButton.disabled = false;
            this.userInput.disabled = false;
             this.userInput.focus(); // Set focus back to input
        }
    }

    addMessage(type, author, content) {
        console.log(`Adding message - Type: ${type}, Author: ${author}, Content: ${content.substring(0, 50)}...`);
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', `message-${type}`); // type: 'user', 'ai', 'system'

        let authorHtml = '';
        let contentHtml = `<div class="message-content">${content.replace(/\n/g, '<br>')}</div>`; // Basic formatting

        if (type === 'ai') {
            const spriteFilename = this._getMemberSprite(author);
            const spriteUrl = spriteFilename ? `/static/images/${spriteFilename}` : '/static/images/ai_placeholder.png'; // Fallback placeholder
            authorHtml = `
                <div class="message-author flex items-center mb-1">
                    <img src="${spriteUrl}" alt="${author} avatar" class="w-6 h-6 rounded-full mr-2">
                    <span class="font-medium">${author}</span>
                </div>`;
        } else if (type === 'user') {
            authorHtml = `
                <div class="message-author flex items-center justify-end mb-1">
                    <span class="font-medium mr-2">${author}</span>
                    <img src="/static/images/user_placeholder.png" alt="User avatar" class="w-6 h-6 rounded-full">
                </div>`;
        } else { // system
             authorHtml = `
                <div class="message-author flex items-center mb-1">
                     <span class="font-medium text-gray-500 italic">${author}</span>
                 </div>`;
        }
        
        messageElement.innerHTML = authorHtml + contentHtml;

        this.chatMessages.appendChild(messageElement);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight; // Scroll to bottom
    }

    // Helper to get sprite (assuming councilMembersUI has the mapping)
    _getMemberSprite(memberId) {
        const member = this.councilMembersUI.getMemberById(memberId);
        // Use placeholder sprite based on index, cycling through available images
        const index = this.councilMembersUI.members.findIndex(m => m.id === memberId);
        return this.placeholderSprites[index % this.placeholderSprites.length] || null;
        // return member ? member.sprite : null; // Replace with actual sprite logic when available
    }

    // TODO: Implement /api/discussions/<id>/continue endpoint handling if needed
    // async continueDiscussion() { ... }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    // Removed AICouncilUI initialization as it's not used for chat display anymore
    // const aiCouncil = new AICouncilUI(); 
    const councilMembersUI = new CouncilMembersUI();
    const chat = new ChatInterface(councilMembersUI); // Pass councilMembersUI to ChatInterface
}); 