# AI Council Flask Application Planner

## Background and Motivation
The goal is to create a Flask application that allows users to interact with an AI Council - a group of different AI models that can discuss complex topics. Users should be able to:
- Fill in system prompts for each AI persona
- Ask and discuss complex topics with these AIs
- Initiate new discussions
- Modify each AI's system prompt/persona during discussions

Each AI will be represented by a static image in the UI. The user has basic images for each AI that will be stored in the static/images directory.

## Application Code Structure Outline

- **`app.py`**: The main Flask application file.
    - Initializes the Flask app.
    - Creates the `AICouncil` instance.
    - Defines all API endpoints.
    - Handles HTTP requests and responses.
    - Serves the main `index.html` template.

- **`ai_council.py`**: Core logic for the AI Council.
    - Defines the `AICouncil` class.
    - Manages multiple AI model instances (e.g., Claude, ChatGPT).
    - Stores and manages default and current system prompts.
    - Orchestrates discussions between AI models.

- **`claude.py`, `chatgpt.py`, `gemini.py`, `grok.py`, `llama.py`**: Individual AI model client implementations.
    - Each file defines a class for a specific AI model.
    - Handle API communication specific to each AI provider.
    - Expose methods for generating responses.

- **`templates/`**: Directory containing HTML templates.
    - **`index.html`**: The main single-page application HTML structure.

- **`static/`**: Directory containing static assets.
    - **`css/style.css`**: Basic CSS for layout and styling.
    - **`js/main.js`**: Frontend JavaScript logic.
    - **`images/`**: AI avatar images.

## Key Challenges and Analysis
1. **AI Council Integration**: We need to modify the existing Flask app to use the AICouncil class. The AICouncil class is already implemented and supports having multiple AI models discuss topics together.

2. **UI/UX Design Challenges**:
   - Create an interface that allows users to:
     - See all AI participants with their static images
     - Modify system prompts for each AI
     - Start new discussions
     - View the discussion in a threaded/conversation format

3. **Technical Implementation Challenges**:
   - Manage discussions and their states
   - Real-time updates as AIs respond to discussions
   - Efficient handling of potentially long discussions

## High-level Task Breakdown
1. **Backend Integration**
   - Update app.py to use AICouncil
   - Create new endpoints for:
     - Getting/updating AI system prompts
     - Starting new discussions
     - Getting discussion status/responses
   - Success criteria: Backend API endpoints function correctly and integrate with AICouncil

2. **Frontend UI Implementation**
   - Update index.html for the council interface
   - Create CSS for member display
   - Implement JS for managing discussions and AI interactions
   - Success criteria: UI displays all required elements and handles user interactions correctly

3. **Testing and Refinement**
   - Test the complete flow from setting prompts to viewing discussions
   - Optimize performance for multiple AI responses
   - Fix any UI/UX issues
   - Success criteria: System works smoothly with all features functioning as expected

## Project Status Board
- [x] Task 1: Update app.py to use AICouncil
- [x] Task 2: Create new API endpoints for AI council functionality
- [x] Task 3: Frontend UI Implementation
- [x] Task 4: Testing and Refinement

## Executor's Feedback or Assistance Requests
Task 1 completed:
- Updated app.py to use AICouncil instead of MasterAI
- Modified the existing API endpoints to work with AICouncil's discussion format
- Added new endpoints for:
  - GET /api/models: Returns a list of available AI models
  - GET /api/prompts: Returns current system prompts for all models
  - POST /api/prompts: Updates system prompts for specified models

The current implementation now returns responses from all AI models in the council rather than a single response. The frontend will need to be updated to handle multiple responses from different AI models.

## Lessons
- Include info useful for debugging in the program output.
- Read the file before you try to edit it.
- If there are vulnerabilities that appear in the terminal, run npm audit before proceeding
- Always ask before using the -force git command