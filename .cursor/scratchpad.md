# AI Council Flask Application Planner

## Background and Motivation
The goal is to create a Flask application that allows users to interact with an AI Council - a group of different AI models that can discuss complex topics. Users should be able to:
- Fill in system prompts for each AI persona
- Ask and discuss complex topics with these AIs
- Initiate new discussions
- Modify each AI's system prompt/persona during discussions

Each AI will be represented by a retro pixel art character that animates during discussions, similar to 90s arcade games. The user has basic pixel art representations for each AI, but animations need to be created later.

This phase focuses on integrating the specific AI model implementations (e.g., Claude, ChatGPT) available in the codebase, defining distinct default personalities for them, and implementing the core discussion interface where users can interact with the selected AI council and view their conversation.

## Key Challenges and Analysis
1. **AI Council Integration**: We need to modify the existing Flask app to use the AICouncil class instead of MasterAI. The AICouncil class is already implemented and supports having multiple AI models discuss topics together.

2. **UI/UX Design Challenges** (Initial Setup):
   - Create an interface that allows users to:
     - See all AI participants with their retro pixel avatars
     - Modify system prompts for each AI
     - Start new discussions and track ongoing ones
     - View the discussion in a threaded/conversation format
   - Implement sprite animations for each AI character
   - Make the UI responsive and engaging

3. **Technical Implementation Challenges** (Initial Setup):
   - Integrate pixel art animations with discussion state
   - Manage multiple discussions and their states
   - Real-time updates as AIs respond to discussions
   - Efficient handling of potentially long discussions

4. **Interactive Council Member Management**
   - Users need to be able to:
     - Activate/deactivate council members through UI interaction
     - Modify system prompts for each AI through a popup interface
     - Visually distinguish between active and inactive members
   - Technical considerations:
     - State management for council members (active/inactive)
     - Smooth transitions for visual feedback
     - Proper event handling for member interactions
     - Efficient reordering of council members list
     - Persistence of member states and prompts

5. **UI/UX Design Challenges** (Council Management):
   - Create an intuitive popup interface for system prompt modification
   - Implement clear visual feedback for active/inactive states
   - Design smooth animations for state transitions
   - Ensure accessibility in interactive elements
   - Maintain responsive design across different screen sizes

6. **AI Model & Discussion Flow Implementation**:
    - **Multiple AI APIs**: Integrate potentially different API structures and response times from various AI models (Claude, ChatGPT, etc.) into a unified council framework.
    - **Distinct Personas**: Ensure default and user-defined prompts effectively create diverse viewpoints within the AI council discussions.
    - **Chat UI**: Develop a clear and intuitive chat interface that displays contributions from multiple AIs, associating responses with the correct AI avatar.
    - **Real-time Updates**: Manage the asynchronous nature of AI responses and update the UI smoothly as the discussion progresses.

## High-level Task Breakdown
1. **Backend Integration**
   - Update app.py to use AICouncil instead of MasterAI
   - Create new endpoints for:
     - Getting/updating AI system prompts
     - Starting new discussions
     - Getting discussion status/responses
   - Success criteria: Backend API endpoints function correctly and integrate with AICouncil

2. **Database/State Management**
   - Implement storage for:
     - AI system prompts
     - Discussion history
     - User sessions
   - Success criteria: Data persists between sessions, system prompts can be modified

3. **Frontend UI Implementation**
   - Update index.html for the council interface
   - Create CSS for pixel art display and animations
   - Implement JS for managing discussions and AI interactions
   - Success criteria: UI displays all required elements and handles user interactions correctly

4. **Sprite Animation System**
   - Design a sprite animation framework
   - Integrate sprite animations with AI response states
   - Create basic animation states (idle, thinking, speaking)
   - Success criteria: Characters animate properly based on AI state

5. **Testing and Refinement**
   - Test the complete flow from setting prompts to viewing discussions
   - Optimize performance for multiple AI responses
   - Fix any UI/UX issues
   - Success criteria: System works smoothly with all features functioning as expected

3. **Enhanced Council Member Display and Interaction** (Modified)
   a. Update Council Member UI Components
      - Create new council member card design with interactive elements
      - Implement active/inactive state styling
      - Add click handlers for member activation
      - Success criteria: Council members are clickable and show clear visual state
   
   b. Implement Member State Management
      - Create state management system for member status
      - Implement ordering logic for active/inactive members
      - Add persistence for member states
      - Success criteria: Member states persist and affect display order correctly

   c. Add Animation and Visual Feedback
      - Implement smooth transitions for state changes
      - Add visual indicators for interactive elements
      - Create grayscale effect for inactive members
      - Success criteria: State changes have smooth, clear visual feedback

4. **System Prompt Modification Interface** (Modified)
   a. Create Popup Component
      - Design and implement modal/popup UI
      - Add form for system prompt editing
      - Include activation toggle switch
      - Success criteria: Popup appears/disappears smoothly with proper form controls

   b. Implement Prompt Management
      - Add save/cancel functionality for prompt changes
      - Implement state persistence for prompts
      - Add validation for prompt content
      - Success criteria: Prompts can be modified and persist between sessions

   c. Enhance User Experience
      - Add keyboard navigation support
      - Implement loading states
      - Add error handling and user feedback
      - Success criteria: Interface is accessible and provides clear feedback

5. **AI Model Integration and Discussion Flow**
   a. Backend - Model Instantiation
      - Modify `AICouncil` or related backend logic to dynamically instantiate and use specific model classes from `claude.py`, `chatgpt.py`, etc. based on configuration or availability.
      - Success criteria: Backend can load and interact with the defined AI model classes.
   b. Backend - Default System Prompts
      - Implement logic to load default system prompts for each available AI model.
      - Expose these defaults via an API endpoint (perhaps extending `/api/models` or `/api/prompts`).
      - Success criteria: Default prompts are loaded and accessible via API.
   c. Frontend - Fetch Models and Prompts
      - Update the frontend to fetch the list of available models and their *default* system prompts.
      - Display this information, potentially allowing users to reset to defaults in the prompt editor.
      - Success criteria: UI lists available models and shows their default prompts.
   d. Frontend - Discussion Initiation
      - Implement the UI flow for starting a new discussion.
      - Allow users to provide an initial topic/question.
      - Send the request to the backend, including the list of *active* models and their *current* (potentially modified) system prompts.
      - Prerequisite: Task 4b (Implement Prompt Management) must be complete.
      - Success criteria: User can start a new discussion with selected AIs and prompts via the UI.
   e. Frontend - Discussion Display
      - Create the chat interface area in `index.html`.
      - Implement JS logic to fetch discussion updates (new messages from AIs or user).
      - Display messages sequentially, associating each AI message with the correct model's name and avatar icon. Use a layout similar to Discord/Slack.
      - Success criteria: Ongoing discussions are displayed in a chat format with speaker attribution (icon + name).
   f. End-to-End Testing
      - Test the complete workflow: Load page -> Modify prompts -> Select active models -> Start discussion -> View AI responses in chat UI -> Add user follow-up.
      - Verify that different system prompts lead to varied responses.
      - Success criteria: The application facilitates a multi-AI discussion initiated and viewed by the user.

## Project Status Board
- [x] Task 1: Update app.py to use AICouncil
- [x] Task 2: Create new API endpoints for AI council functionality
- [x] Task 3a: Update Council Member UI Components
- [x] Task 3b: Implement Member State Management
- [/] Task 3c: Add Animation and Visual Feedback (Basic transitions added, needs sprites)
- [x] Task 4a: Create Popup Component
- [ ] Task 4b: Implement Prompt Management
- [ ] Task 4c: Enhance User Experience
- [ ] Task 5a: Backend - Model Instantiation
- [ ] Task 5b: Backend - Default System Prompts
- [ ] Task 5c: Frontend - Fetch Models and Prompts
- [ ] Task 5d: Frontend - Discussion Initiation
- [ ] Task 5e: Frontend - Discussion Display
- [ ] Task 5f: End-to-End Testing

## Executor's Feedback or Assistance Requests
Task 1 completed:
- Updated app.py to use AICouncil instead of MasterAI
- Modified the existing API endpoints to work with AICouncil's discussion format
- Added new endpoints for:
  - GET /api/models: Returns a list of available AI models
  - GET /api/prompts: Returns current system prompts for all models
  - POST /api/prompts: Updates system prompts for specified models

The current implementation now returns responses from all AI models in the council rather than a single response. The frontend will need to be updated to handle multiple responses from different AI models.

Task 2 completed:
- Added in-memory storage for discussions (in a production app, this would be a database)
- Implemented new API endpoints:
  - GET /api/discussions: Lists all discussions
  - POST /api/discussions: Starts a new discussion
  - GET /api/discussions/<id>: Gets details and results of a specific discussion
  - POST /api/discussions/<id>/continue: Continues an existing discussion by adding more rounds
  - POST /api/discussions/<id>/contribute: Adds a user contribution to an ongoing discussion

Each discussion has:
- A unique ID
- Topic
- Creation timestamp
- Status (in_progress, complete, error)
- Results from each round of the discussion

Next steps would be to implement Task 3 (design and implement the AI character display UI) and Task 4 (implement system prompt editing interface) to create the frontend that will interact with these new API endpoints.

Task 3c partially completed:
- Added smoother CSS transitions for card state changes.
- Implemented placeholder background images for sprites.
- Full sprite animation requires proper assets.

Task 4a completed:
- Created HTML structure for the prompt editor modal.
- Added CSS for modal visibility, animations, and styling (including toggle indicator).
- Implemented JS logic to open/close the modal, populate it with member data, and handle basic save logic (updating local state).
- Refined modal layout and interaction based on user feedback (bigger 'X', clickable status indicator, indicator position).
- Refined card interaction: clicking indicator toggles state directly, clicking card opens modal.
- Logic added to default member to 'active' if prompt is edited.

Next step is Task 4b (implementing API calls for saving changes).

## Technical Requirements
1. Frontend State Management:
   ```javascript
   interface CouncilMember {
     id: string;
     name: string;
     sprite: string;
     isActive: boolean;
     systemPrompt: string;
     order: number;
   }
   ```

2. API Endpoints Needed:
   ```
   GET /api/council-members
   POST /api/council-members/{id}/toggle
   PUT /api/council-members/{id}/prompt
   PUT /api/council-members/order
   ```

3. CSS Requirements:
   - Transitions for state changes
   - Grayscale filter for inactive members
   - Z-index management for popup
   - Responsive design breakpoints

## Implementation Steps (In Order)
1. Update HTML structure for council member cards
2. Add state management in JavaScript
3. Implement popup component
4. Add activation/deactivation logic
5. Implement ordering system
6. Add persistence layer
7. Enhance animations and transitions
8. Add accessibility features
9. Implement error handling
10. Add loading states

## Success Criteria
1. Council member states (active/inactive) persist between sessions
2. Members can be activated/deactivated with clear visual feedback
3. System prompts can be modified and are saved correctly
4. Active members appear before inactive ones
5. All interactions have smooth animations
6. Interface is fully responsive and accessible
7. Error states are handled gracefully
8. Performance remains smooth with multiple state changes

## Lessons
- When starting a new discussion, users can specify which AI models to include using the `active_models` parameter
- The list of active models is stored with each discussion and remains consistent throughout the discussion
- Models can be selected at discussion creation time, and the selection applies to all rounds of that discussion
- If no models are specified, all available models participate in the discussion by default
- Invalid model names are caught and reported before starting the discussion

## Default System Prompts
*Note: These are initial suggestions and can be refined.*

- **Claude (The Pragmatist)**: "You are a pragmatic and analytical AI. Focus on logical reasoning, feasibility, and potential downsides. Provide balanced perspectives and avoid overly speculative or emotional arguments. Ground your contributions in evidence and practical considerations."
- **ChatGPT (The Optimist/Creative)**: "You are a creative and optimistic AI. Focus on possibilities, innovative solutions, and positive outcomes. Explore potential benefits and encourage blue-sky thinking. Don't be afraid to be imaginative and think outside the box."
- **[Future Model] (The Critic)**: "You are a critical and questioning AI. Your role is to challenge assumptions, identify potential flaws, and raise devil's advocate points. Focus on rigor, potential risks, and unintended consequences. Ensure all angles are considered."
- **[Future Model] (The Synthesizer)**: "You are a synthesizing AI. Your role is to find connections between different viewpoints, summarize key arguments, and facilitate consensus or identify core disagreements. Focus on clarity, structure, and bridging perspectives." 