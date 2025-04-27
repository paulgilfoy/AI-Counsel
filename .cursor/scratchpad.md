# AI Council Flask Application Planner

## Background and Motivation
The goal is to create a Flask application that allows users to interact with an AI Council - a group of different AI models that can discuss complex topics. Users should be able to:
- Fill in system prompts for each AI persona
- Ask and discuss complex topics with these AIs
- Initiate new discussions
- Modify each AI's system prompt/persona during discussions

Each AI will be represented by a retro pixel art character that animates during discussions, similar to 90s arcade games. The user has basic pixel art representations for each AI, but animations need to be created later.

## Key Challenges and Analysis
1. **AI Council Integration**: We need to modify the existing Flask app to use the AICouncil class instead of MasterAI. The AICouncil class is already implemented and supports having multiple AI models discuss topics together.

2. **UI/UX Design Challenges**:
   - Create an interface that allows users to:
     - See all AI participants with their retro pixel avatars
     - Modify system prompts for each AI
     - Start new discussions and track ongoing ones
     - View the discussion in a threaded/conversation format
   - Implement sprite animations for each AI character
   - Make the UI responsive and engaging

3. **Technical Implementation Challenges**:
   - Integrate pixel art animations with discussion state
   - Manage multiple discussions and their states
   - Real-time updates as AIs respond to discussions
   - Efficient handling of potentially long discussions

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

## Project Status Board
- [x] Task 1: Update app.py to use AICouncil
- [x] Task 2: Create new API endpoints for AI council functionality
- [ ] Task 3: Design and implement the AI character display UI
- [ ] Task 4: Implement system prompt editing interface
- [ ] Task 5: Create discussion history and management
- [ ] Task 6: Develop sprite animation system
- [ ] Task 7: Integrate animations with discussion flow
- [ ] Task 8: Test complete system flow
- [ ] Task 9: Optimize performance and fix bugs

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

## Lessons
- When starting a new discussion, users can specify which AI models to include using the `active_models` parameter
- The list of active models is stored with each discussion and remains consistent throughout the discussion
- Models can be selected at discussion creation time, and the selection applies to all rounds of that discussion
- If no models are specified, all available models participate in the discussion by default
- Invalid model names are caught and reported before starting the discussion 