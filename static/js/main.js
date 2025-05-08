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
        this.chatForm = document.getElementById('chat-form');
        this.userInput = document.getElementById('user-input');
        this.chatContainer = document.getElementById('chat-container');
        this.councilMembersUI = councilMembersUI; // Store reference
        this.placeholderSprites = placeholderSprites; // Store placeholder sprites
        this.currentDiscussionId = null; // Track the current discussion ID

        if (!this.chatForm || !this.userInput || !this.chatContainer) {
            console.error('Chat interface elements not found!');
            return;
        }
        this.setupEventListeners();
        this.updateInputPlaceholder(); // Initial placeholder setting
    }

    setupEventListeners() {
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSendMessage();
        });
    }

    setStartDiscussionStatus(message, isError = false) {
        console.log(`Discussion Status: ${message}`);
         if (isError) {
             this.addMessage('system', 'Error', message);
         } else {
             this.addMessage('system', 'System', message);
         }
    }

    async startNewDiscussion(topic) {
        console.log(`Starting new discussion with topic: "${topic}"`);
        this.addMessage('user', 'You', topic); // Display user's initial message

        const activeMembers = this.councilMembersUI.members
            .filter(m => m.isActive)
            .map(m => m.id);

        if (activeMembers.length === 0) {
            this.setStartDiscussionStatus("Please activate at least one council member.", true);
            return;
        }

        console.log("Active members for new discussion:", activeMembers);
        this.setStartDiscussionStatus("Starting discussion with council...");

        try {
            const response = await fetch('/api/discussions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    topic: topic,
                    active_models: activeMembers
                }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: 'Unknown error starting discussion.' }));
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log("New discussion started:", result);
            this.currentDiscussionId = result.discussion_id; // Store the ID
            this.setStartDiscussionStatus(`Discussion ${this.currentDiscussionId} started.`);
            this.displayDiscussionResults(result.results || {}); // Display initial AI responses
            this.updateInputPlaceholder(); // Update placeholder after discussion starts

        } catch (error) {
            console.error('Error starting discussion:', error);
            this.setStartDiscussionStatus(`Error: ${error.message}`, true);
            this.currentDiscussionId = null; // Ensure ID is null on error
        }
    }

    displayDiscussionResults(results) {
         const discussionResults = results || {};
        console.log("--- Displaying Discussion Results ---"); // Log start
        console.log("Raw results object received:", JSON.stringify(discussionResults, null, 2)); // Log the whole object structure

         if (Object.keys(discussionResults).length === 0) {
             this.addMessage('system', 'System', 'No initial responses received.');
             return;
         }

        Object.keys(discussionResults).sort().forEach(round => {
            console.log(`Processing round: ${round}`); // Log current round key
            const roundMessages = discussionResults[round];
            console.log(`Value for round ${round} (type: ${typeof roundMessages}):`, JSON.stringify(roundMessages, null, 2)); // Log the value and its type

            // Add a check before calling forEach
            if (Array.isArray(roundMessages)) {
                roundMessages.forEach(msg => {
                     if (msg && msg.sender && msg.message) {
                         this.addMessage('ai', msg.sender, msg.message);
                     } else {
                         console.warn("Skipping invalid message format in round " + round + ":", msg);
                     }
                });
            } else {
                // Log an error if it's not an array
                console.error(`Expected an array for round ${round}, but got type ${typeof roundMessages}. Value:`, roundMessages);
                this.addMessage('system', 'Error', `Failed to process responses for round ${round} due to unexpected data format.`);
            }
        });
        console.log("--- Finished Displaying Discussion Results ---"); // Log end
    }

    async handleSendMessage() {
        const messageText = this.userInput.value.trim();
        if (!messageText) return;

        if (this.currentDiscussionId === null) {
            await this.startNewDiscussion(messageText);
        } else {
            await this.contributeToDiscussion(messageText);
        }

        this.userInput.value = ''; // Clear input after processing
    }

    async contributeToDiscussion(message) {
        if (!this.currentDiscussionId) {
            console.error("Cannot contribute without a currentDiscussionId.");
            this.addMessage('system', 'Error', 'Cannot send message, no active discussion found.');
            return;
        }
        console.log(`Contributing to discussion ${this.currentDiscussionId}: "${message}"`);
        this.addMessage('user', 'You', message); // Display user's message

        this.setStartDiscussionStatus("Sending your message..."); // Use status for feedback

        try {
            const response = await fetch(`/api/discussions/${this.currentDiscussionId}/contribute`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ contribution: message }),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: 'Unknown error contributing to discussion.' }));
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log("Contribution response:", result);
            this.setStartDiscussionStatus("Message sent."); // Update status

            // The current backend /contribute endpoint doesn't return new AI messages.
            // If it did, we would call displayDiscussionResults or a similar function here.
            // We don't need to change the placeholder here as the discussion is still ongoing.

            // Future work (streaming/Task 7) will handle receiving subsequent AI responses.

        } catch (error) {
            console.error('Error contributing to discussion:', error);
            this.setStartDiscussionStatus(`Error sending message: ${error.message}`, true);
        }
    }

    addMessage(type, author, content) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', `message-${type}`); // e.g., message-user, message-ai, message-system
        
        const authorElement = document.createElement('span');
        authorElement.classList.add('font-semibold');
        authorElement.textContent = `${author}: `;

        const contentElement = document.createElement('span');
        contentElement.textContent = content;

        if (type === 'user') {
            messageElement.classList.add('text-right', 'mb-2');
            authorElement.classList.add('text-blue-400'); 
            messageElement.appendChild(contentElement); // Content first for user
            messageElement.appendChild(authorElement); // Author second
        } else if (type === 'ai') {
            messageElement.classList.add('text-left', 'mb-4'); // More margin below AI messages
            // Find member details to get sprite placeholder
            const member = this.councilMembersUI.members.find(m => m.id === author);
            const spriteIndex = this.councilMembersUI.members.findIndex(m => m.id === author);
            const spriteFilename = member ? placeholderSprites[spriteIndex % placeholderSprites.length] : 'grok1.jpeg'; // Default sprite
            
            const avatarElement = document.createElement('div');
            avatarElement.classList.add('w-8', 'h-8', 'rounded-full', 'bg-gray-600', 'mr-2', 'inline-block', 'align-top');
            avatarElement.style.backgroundImage = `url(/static/images/${spriteFilename})`;
            avatarElement.style.backgroundSize = 'cover';
            avatarElement.style.backgroundPosition = 'center';
            avatarElement.title = author; // Show name on hover
            
            const messageContentWrapper = document.createElement('div');
            messageContentWrapper.classList.add('inline-block', 'bg-gray-700', 'rounded-lg', 'px-3', 'py-2', 'max-w-[80%]');
            
            authorElement.classList.add('text-green-400', 'block', 'text-sm'); // Author name on top
            authorElement.textContent = author;
            contentElement.classList.add('text-gray-200');
            
            messageContentWrapper.appendChild(authorElement);
            messageContentWrapper.appendChild(contentElement);
            
            messageElement.appendChild(avatarElement);
            messageElement.appendChild(messageContentWrapper);

        } else { // System messages
            messageElement.classList.add('text-center', 'text-gray-500', 'text-sm', 'my-2');
            authorElement.textContent = `[${author}]`;
            messageElement.appendChild(authorElement);
            messageElement.appendChild(document.createTextNode(' ')); // Add space
            messageElement.appendChild(contentElement);
        }

        this.chatContainer.appendChild(messageElement);
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    // Helper to get member sprite (Placeholder implementation)
    // TODO: Enhance this later if needed
    _getMemberSprite(memberId) {
        const memberIndex = this.councilMembersUI.members.findIndex(m => m.id === memberId);
         if (memberIndex !== -1) {
             return placeholderSprites[memberIndex % placeholderSprites.length];
         }
         return placeholderSprites[0]; // Default
    }

    async sendMessage(message, activeModels) {
        // This function seems deprecated by startNewDiscussion and handleSendMessage logic
        // Keeping it here commented out for reference, might remove later.
        /*
// ... existing code ...

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
        */
    }

    updateInputPlaceholder() {
        if (this.currentDiscussionId === null) {
            this.userInput.placeholder = "Start a new discussion by typing your topic here...";
        } else {
            this.userInput.placeholder = "Type your message to continue the discussion...";
            // Future Enhancement (Task 8c): Modify this when the 'Continue' button is added
            // e.g., "Type your message... or click 'Continue Discussion'"
        }
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    // Removed AICouncilUI initialization as it's not used for chat display anymore
    // const aiCouncil = new AICouncilUI(); 
    const councilMembersUI = new CouncilMembersUI();
    const chat = new ChatInterface(councilMembersUI); // Pass councilMembersUI to ChatInterface
}); 