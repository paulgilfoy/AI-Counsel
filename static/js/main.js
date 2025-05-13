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

// Available AI images
const aiImages = {
    'Claude': 'claude1.jpeg',
    'ChatGPT': 'chatgpt1.webp',
    'Gemini': 'gemini1.jpeg',
    'Llama': 'llma1.jpeg',
    'Grok': 'grok1.jpeg',
    // Add more specific mappings to match exact model IDs
    'claude-3-5-sonnet-20241022': 'claude1.jpeg',
    'gpt-4o-mini-2024-07-18': 'chatgpt1.webp',
    'gemini-2.0-flash': 'gemini1.jpeg',
    'meta/meta-llama-3-70b-instruct': 'llma1.jpeg',
    'grok-2-latest': 'grok1.jpeg'
};

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

        // Use the static image for this model
        const imageFile = aiImages[model.id] || 'grok1.jpeg'; // Default to grok if not found
        sprite.style.backgroundImage = `url(/static/images/${imageFile})`;
        name.textContent = model.name;
        status.textContent = 'Ready';

        return element;
    }

    updateCharacterState(modelId, state) {
        const character = this.characters.get(modelId);
        if (!character) return;

        const status = character.querySelector('.status');
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

    createCard(member, index) {
        const card = this.cardTemplate.content.cloneNode(true).children[0];
        card.dataset.memberId = member.id;
        card.querySelector('.member-name').textContent = member.name;
        card.querySelector('.member-provider').textContent = member.provider;
        card.querySelector('.member-prompt').textContent = member.systemPrompt;
        
        const spriteContainer = card.querySelector('.sprite-container');
        
        // Use the static image for this model
        const imageFile = aiImages[member.id] || 'grok1.jpeg'; // Default to grok if not found
        spriteContainer.style.backgroundImage = `url(/static/images/${imageFile})`;

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

    getActiveMembers() {
        // Return an array of active member objects
        return this.members.filter(member => member.isActive);
    }
}

// Chat Interface (modified to use CouncilMembersUI for active members)
class ChatInterface {
    constructor(councilMembersUI) { // Changed constructor parameter
        this.form = document.getElementById('chat-form');
        this.inputField = document.getElementById('user-input');
        this.chatContainer = document.getElementById('chat-container');
        this.councilMembersUI = councilMembersUI;
        this.currentDiscussionId = null;
        this.isContinuingDiscussion = false;
        this.eventSource = null;
        this.modelMessages = {};
        this.roundsSelector = document.getElementById('rounds-selector'); // Add round selector reference
        
        // Check if browser supports EventSource (Server-Sent Events)
        this.supportsEventSource = typeof EventSource !== 'undefined';
        if (!this.supportsEventSource) {
            console.warn('This browser does not support Server-Sent Events. Falling back to traditional requests.');
        }
        
        this.setupEventListeners();
        this.updateInputPlaceholder();
    }

    setupEventListeners() {
        this.form.addEventListener('submit', (e) => {
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
        this.setStartDiscussionStatus('Starting discussion...', false);
        
        try {
            // Get active council members
            const activeMembers = this.councilMembersUI.getActiveMembers();
            
            if (activeMembers.length === 0) {
                this.addMessage('system', 'System', 'Please activate at least one council member to start a discussion.');
                return;
            }

            // Get selected number of rounds
            const rounds = parseInt(this.roundsSelector.value, 10) || 1;
            
            // Show a typing indicator for each active member
            activeMembers.forEach(member => {
                this.addTypingIndicator(member.id);
            });
            
            // Start the discussion with streaming responses
            if (this.supportsEventSource) {
                // Use streaming API if EventSource is available
                this.streamDiscussionStart(topic, activeMembers.map(m => m.id), rounds);
            } else {
                // Fallback to non-streaming API
                const response = await fetch('/api/discussions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        topic: topic,
                        active_models: activeMembers.map(m => m.id),
                        rounds: rounds
                    })
                });
                
                if (!response.ok) {
                    throw new Error(`Failed to start discussion: ${response.statusText}`);
                }
                
                const data = await response.json();
                
                if (data.status === 'success') {
                    this.currentDiscussionId = data.discussion_id;
                    this.updateInputPlaceholder();
                    
                    // Remove typing indicators
                    this.removeAllTypingIndicators();
                    
                    // Display initial AI responses
                    this.displayDiscussionResults(data.results);
                } else {
                    throw new Error(data.message || 'Failed to start discussion');
                }
            }
        } catch (error) {
            console.error('Error starting discussion:', error);
            this.setStartDiscussionStatus('Error: ' + error.message, true);
            this.removeAllTypingIndicators();
        }
    }

    streamDiscussionStart(topic, activeModels, rounds = 1) {
        // Create a new POST request to start a discussion
        fetch('/api/discussions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                topic: topic,
                active_models: activeModels,
                rounds: rounds
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to start discussion: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                this.currentDiscussionId = data.discussion_id;
                this.updateInputPlaceholder();
                
                // Now that we have a discussion ID, connect to the streaming endpoint
                this.connectToStream(this.currentDiscussionId);
            } else {
                throw new Error(data.message || 'Failed to start discussion');
            }
        })
        .catch(error => {
            console.error('Error starting discussion:', error);
            this.setStartDiscussionStatus('Error: ' + error.message, true);
            this.removeAllTypingIndicators();
        });
    }

    connectToStream(discussionId) {
        // Close any existing event source
        if (this.eventSource) {
            this.eventSource.close();
        }
        
        // For continue discussion, first make a POST request
        if (this.isContinuingDiscussion) {
            // Get selected number of rounds
            const rounds = parseInt(this.roundsSelector.value, 10) || 1;
            
            fetch(`/api/discussions/${discussionId}/stream`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    rounds: rounds
                })
            }).then(response => {
                if (!response.ok) {
                    throw new Error('Failed to initiate streaming');
                }
                // Now create the EventSource after successful POST
                this.createEventSource(discussionId);
            }).catch(error => {
                console.error('Error initiating streaming:', error);
                this.addMessage('system', 'System', `Error: ${error.message}`);
                this.removeAllTypingIndicators();
            });
        } else {
            // For initial discussion, just create the EventSource
            this.createEventSource(discussionId);
        }
    }

    createEventSource(discussionId) {
        // Create a new event source for the streaming endpoint
        this.eventSource = new EventSource(`/api/discussions/${discussionId}/stream`);
        
        // Initialize message containers for each model
        this.modelMessages = {};
        
        // Setup event handlers
        this.eventSource.addEventListener('stream_start', (event) => {
            const data = JSON.parse(event.data);
            console.log('Stream started:', data);
            
            // Show round progress info if available
            if (data.rounds_requested) {
                this.addMessage('system', 'System', `Discussion started with ${data.rounds_requested} round(s) requested.`);
            }
        });
        
        this.eventSource.addEventListener('model_start', (event) => {
            const data = JSON.parse(event.data);
            console.log('Model starting:', data.model);
            
            // Remove typing indicator for this model
            this.removeTypingIndicator(data.model);
            
            // Create a message element for this model
            this.modelMessages[data.model] = this.createStreamingMessage(data.model);
        });
        
        this.eventSource.addEventListener('model_update', (event) => {
            const data = JSON.parse(event.data);
            console.log('Model update:', data.model, data.chunk);
            
            // Append the chunk to the model's message
            this.appendToStreamingMessage(data.model, data.chunk);
        });
        
        this.eventSource.addEventListener('model_complete', (event) => {
            const data = JSON.parse(event.data);
            console.log('Model complete:', data.model);
            
            // Mark the model's message as complete
            this.completeStreamingMessage(data.model, data.response);
        });
        
        this.eventSource.addEventListener('stream_complete', (event) => {
            console.log('Stream complete');
            
            // Show round progress if available
            try {
                const data = JSON.parse(event.data);
                if (data.rounds && data.rounds_requested) {
                    const isComplete = data.rounds >= data.rounds_requested;
                    if (isComplete) {
                        this.addMessage('system', 'System', `Discussion complete. All ${data.rounds} round(s) finished.`);
                    } else {
                        this.addMessage('system', 'System', `Round ${data.rounds} of ${data.rounds_requested} complete.`);
                    }
                }
            } catch (error) {
                console.error('Error parsing stream_complete data:', error);
            }
            
            // Close the event source
            if (this.eventSource) {
                this.eventSource.close();
                this.eventSource = null;
            }
            
            // Add a continue button now that the streaming is complete
            this.addContinueButton();
        });
        
        this.eventSource.addEventListener('stream_error', (event) => {
            const data = JSON.parse(event.data);
            console.error('Stream error:', data.error);
            
            // Display error message
            this.addMessage('system', 'Error', data.error);
            
            // Close the event source
            if (this.eventSource) {
                this.eventSource.close();
                this.eventSource = null;
            }
        });
        
        this.eventSource.onerror = (error) => {
            console.error('EventSource error:', error);
            this.addMessage('system', 'System', 'Connection error. Please try again.');
            
            // Close the event source
            if (this.eventSource) {
                this.eventSource.close();
                this.eventSource = null;
            }
        };
    }

    createStreamingMessage(modelName) {
        // Create a message element for this model
        const messageContainer = document.createElement('div');
        messageContainer.className = 'message ai';
        messageContainer.dataset.model = modelName;
        
        // Get the static image for this AI
        const imageFile = aiImages[modelName] || aiImages['Grok'] || 'grok1.jpeg';
        
        const avatarElement = document.createElement('div');
        avatarElement.className = 'w-8 h-8 rounded-full bg-gray-600 mr-2 inline-block align-top ai-avatar';
        avatarElement.style.backgroundImage = `url(/static/images/${imageFile})`;
        avatarElement.style.backgroundSize = 'cover';
        avatarElement.style.backgroundPosition = 'center';
        avatarElement.title = modelName;
        
        const authorWrapper = document.createElement('div');
        authorWrapper.className = 'inline-block';
        
        const author = document.createElement('div');
        author.className = 'author text-green-400 block text-sm';
        author.textContent = modelName;
        
        const content = document.createElement('div');
        content.className = 'content streaming bg-gray-700 rounded-lg px-3 py-2 max-w-[80%]';
        content.textContent = ''; // Start empty
        
        // Add a blinking cursor
        const cursor = document.createElement('span');
        cursor.className = 'cursor';
        cursor.textContent = '|';
        content.appendChild(cursor);
        
        authorWrapper.appendChild(author);
        authorWrapper.appendChild(content);
        
        messageContainer.appendChild(avatarElement);
        messageContainer.appendChild(authorWrapper);
        
        // Add to chat container
        this.chatContainer.appendChild(messageContainer);
        
        // Scroll to the bottom
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
        
        return messageContainer;
    }

    appendToStreamingMessage(modelName, chunk) {
        const messageElement = this.modelMessages[modelName];
        if (!messageElement) return;
        
        const content = messageElement.querySelector('.content');
        if (!content) return;
        
        // Remove the cursor if present
        const cursor = content.querySelector('.cursor');
        if (cursor) {
            content.removeChild(cursor);
        }
        
        // Append the chunk
        const text = document.createTextNode(chunk);
        content.appendChild(text);
        
        // Re-add the cursor
        const newCursor = document.createElement('span');
        newCursor.className = 'cursor';
        newCursor.textContent = '|';
        content.appendChild(newCursor);
        
        // Scroll to the bottom
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    completeStreamingMessage(modelName, fullResponse) {
        const messageElement = this.modelMessages[modelName];
        if (!messageElement) return;
        
        const content = messageElement.querySelector('.content');
        if (!content) return;
        
        // Remove the streaming class and cursor
        content.classList.remove('streaming');
        const cursor = content.querySelector('.cursor');
        if (cursor) {
            content.removeChild(cursor);
        }
        
        // Set the full response text
        content.textContent = fullResponse;
        
        // Scroll to the bottom
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    addTypingIndicator(modelName) {
        // Create typing indicator
        const indicatorContainer = document.createElement('div');
        indicatorContainer.className = 'message typing-container';
        indicatorContainer.dataset.model = modelName;
        
        const author = document.createElement('div');
        author.className = 'author';
        author.textContent = modelName;
        
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = '<span></span><span></span><span></span>';
        
        indicatorContainer.appendChild(author);
        indicatorContainer.appendChild(indicator);
        
        // Add to chat container
        this.chatContainer.appendChild(indicatorContainer);
        
        // Scroll to the bottom
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    removeTypingIndicator(modelName) {
        const indicators = this.chatContainer.querySelectorAll(`.typing-container[data-model="${modelName}"]`);
        indicators.forEach(indicator => {
            indicator.remove();
        });
    }

    removeAllTypingIndicators() {
        const indicators = this.chatContainer.querySelectorAll('.typing-container');
        indicators.forEach(indicator => {
            indicator.remove();
        });
    }

    continueDiscussion() {
        if (!this.currentDiscussionId) {
            console.error('No active discussion to continue');
            return;
        }
        
        // Show loading state
        const continueButton = document.getElementById('continue-discussion-btn');
        if (continueButton) {
            continueButton.disabled = true;
            continueButton.textContent = 'Continuing...';
            continueButton.className = 'bg-gray-500 text-white py-2 px-4 rounded-lg';
        }
        
        // Get active council members for showing typing indicators
        const activeMembers = this.councilMembersUI.getActiveMembers();
        
        // Show a typing indicator for each active member
        activeMembers.forEach(member => {
            this.addTypingIndicator(member.id);
        });
        
        // Get selected number of rounds
        const rounds = parseInt(this.roundsSelector.value, 10) || 1;
        
        // Use streaming if available, otherwise fall back to regular endpoint
        if (this.supportsEventSource) {
            // Remove the button now that we're streaming
            if (continueButton) {
                continueButton.remove();
            }
            
            // Set the flag to indicate we're continuing a discussion
            this.isContinuingDiscussion = true;
            
            // Connect to the streaming endpoint
            this.connectToStream(this.currentDiscussionId);
            
            // Reset the flag after connecting
            setTimeout(() => {
                this.isContinuingDiscussion = false;
            }, 1000);
        } else {
            // Fallback to non-streaming API
            fetch(`/api/discussions/${this.currentDiscussionId}/continue`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    rounds: rounds
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to continue discussion');
                }
                return response.json();
            })
            .then(data => {
                // Remove typing indicators
                this.removeAllTypingIndicators();
                
                if (data.status === 'success') {
                    // Display the new results
                    this.displayDiscussionResults({ [data.results.length - 1]: data.results[data.results.length - 1] });
                } else {
                    throw new Error(data.message || 'Failed to continue discussion');
                }
            })
            .catch(error => {
                console.error('Error continuing discussion:', error);
                this.addMessage('system', 'System', `Error continuing discussion: ${error.message}`);
            })
            .finally(() => {
                // Remove the button regardless of outcome
                if (continueButton) {
                    continueButton.remove();
                }
            });
        }
    }

    async handleSendMessage() {
        const messageText = this.inputField.value.trim();
        if (!messageText) return;

        // Display the user's message
        this.addMessage('user', 'You', messageText);

        if (this.currentDiscussionId === null) {
            // Start a new discussion if we don't have one
            await this.startNewDiscussion(messageText);
        } else {
            // Continue the existing discussion
            await this.contributeToDiscussion(messageText);
        }

        this.inputField.value = ''; // Clear input after processing
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

    displayDiscussionResults(results) {
        console.log("Displaying discussion results:", results);
        
        // Check for empty results
        if (!results) {
            console.warn("No results to display");
            return;
        }
        
        // Add all AI messages from the last round
        const rounds = Object.keys(results);
        if (rounds.length === 0) {
            console.warn("No rounds in results");
            return;
        }
        
        // Get the last round
        const lastRound = rounds[rounds.length - 1];
        const roundMessages = results[lastRound];
        
        // Check if roundMessages is actually an array or object
        console.log("Round messages type:", typeof roundMessages);
        console.log("Round messages is array?", Array.isArray(roundMessages));
        console.log("Round messages value:", roundMessages);
        
        // Safely iterate - handle both array and object formats
        if (Array.isArray(roundMessages)) {
            // If it's an array, iterate normally
            roundMessages.forEach(message => {
                const author = message.model;
                const content = message.response;
                this.addMessage('ai', author, content);
            });
        } else if (typeof roundMessages === 'object' && roundMessages !== null) {
            // If it's an object (old format), iterate over key-value pairs
            Object.entries(roundMessages).forEach(([author, content]) => {
                this.addMessage('ai', author, content);
            });
        } else {
            console.warn("Unexpected format for roundMessages:", roundMessages);
        }
        
        // Add a continue button if this is an active discussion
        if (this.currentDiscussionId) {
            this.addContinueButton();
        }
    }

    addMessage(type, author, content) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', `message-${type}`);
        
        const authorElement = document.createElement('span');
        authorElement.classList.add('font-semibold');
        authorElement.textContent = `${author}: `;

        const contentElement = document.createElement('span');
        contentElement.textContent = content;

        if (type === 'user') {
            messageElement.classList.add('text-right', 'mb-2');
            authorElement.classList.add('text-blue-400'); 
            messageElement.appendChild(contentElement);
            messageElement.appendChild(authorElement);
        } else if (type === 'ai') {
            messageElement.classList.add('text-left', 'mb-4');
            
            // Get the static image for this AI - ensure correct key lookup
            const imageFile = aiImages[author] || aiImages['Grok'] || 'grok1.jpeg';
            
            const avatarElement = document.createElement('div');
            avatarElement.classList.add('w-8', 'h-8', 'rounded-full', 'bg-gray-600', 'mr-2', 'inline-block', 'align-top', 'ai-avatar');
            avatarElement.style.backgroundImage = `url(/static/images/${imageFile})`;
            avatarElement.style.backgroundSize = 'cover';
            avatarElement.style.backgroundPosition = 'center';
            avatarElement.title = author;
            
            const messageContentWrapper = document.createElement('div');
            messageContentWrapper.classList.add('inline-block', 'bg-gray-700', 'rounded-lg', 'px-3', 'py-2', 'max-w-[80%]');
            
            authorElement.classList.add('text-green-400', 'block', 'text-sm');
            authorElement.textContent = author;
            contentElement.classList.add('text-gray-200');
            
            messageContentWrapper.appendChild(authorElement);
            messageContentWrapper.appendChild(contentElement);
            
            messageElement.appendChild(avatarElement);
            messageElement.appendChild(messageContentWrapper);
        } else {
            messageElement.classList.add('text-center', 'text-gray-500', 'text-sm', 'my-2');
            authorElement.textContent = `[${author}]`;
            messageElement.appendChild(authorElement);
            messageElement.appendChild(document.createTextNode(' '));
            messageElement.appendChild(contentElement);
        }

        this.chatContainer.appendChild(messageElement);
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }

    updateInputPlaceholder() {
        if (this.currentDiscussionId === null) {
            this.inputField.placeholder = "Start a new discussion by typing your topic here...";
        } else {
            this.inputField.placeholder = "Type your message to continue the discussion...";
            // Future Enhancement (Task 8c): Modify this when the 'Continue' button is added
            // e.g., "Type your message... or click 'Continue Discussion'"
        }
    }

    addContinueButton() {
        // Check if a continue button already exists
        if (document.getElementById('continue-discussion-btn')) {
            return; // Don't add another one
        }
        
        const buttonContainer = document.createElement('div');
        buttonContainer.className = 'flex flex-col items-center my-4';
        
        const roundsInfo = document.createElement('div');
        roundsInfo.className = 'text-sm text-gray-400 mb-2 text-center';
        const selectedRounds = parseInt(this.roundsSelector.value, 10) || 1;
        roundsInfo.textContent = `${selectedRounds} round(s) will be generated next`;
        
        const continueButton = document.createElement('button');
        continueButton.id = 'continue-discussion-btn';
        continueButton.className = 'bg-indigo-600 hover:bg-indigo-700 text-white py-2 px-4 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500';
        continueButton.textContent = 'Continue Discussion';
        continueButton.setAttribute('aria-label', 'Continue the AI discussion without adding your own message');
        continueButton.setAttribute('role', 'button');
        continueButton.setAttribute('tabindex', '0');
        
        // Add event listeners for both click and keyboard events
        continueButton.addEventListener('click', () => this.continueDiscussion());
        continueButton.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.continueDiscussion();
            }
        });
        
        buttonContainer.appendChild(roundsInfo);
        buttonContainer.appendChild(continueButton);
        this.chatContainer.appendChild(buttonContainer);
        
        // Focus the button to make it immediately accessible via keyboard
        continueButton.focus();
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    // Removed AICouncilUI initialization as it's not used for chat display anymore
    // const aiCouncil = new AICouncilUI(); 
    const councilMembersUI = new CouncilMembersUI();
    const chat = new ChatInterface(councilMembersUI); // Pass councilMembersUI to ChatInterface
}); 