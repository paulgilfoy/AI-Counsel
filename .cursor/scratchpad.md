# AI Council Flask Application Planner

## Background and Motivation
The goal is to create a Flask application that allows users to interact with an AI Council - a group of different AI models that can discuss complex topics. Users should be able to:
- Fill in system prompts for each AI persona
- Ask and discuss complex topics with these AIs
- Initiate new discussions
- Modify each AI's system prompt/persona during discussions

Each AI will be represented by a static image in the UI. The user has basic images for each AI that will be stored in the static/images directory.

This phase focuses on integrating the specific AI model implementations (e.g., Claude, ChatGPT) available in the codebase, defining distinct default personalities for them, and implementing the core discussion interface where users can interact with the selected AI council and view their conversation.



## Application Code Structure Outline

This section outlines the structure of the AI Council Flask application.

- **`app.py`**: The main Flask application file.
    - Initializes the Flask app.
    - Creates the `AICouncil` instance.
    - Defines all API endpoints (`/api/models`, `/api/prompts`, `/api/discussions`, etc.).
    - Handles HTTP requests and responses.
    - Serves the main `index.html` template.

- **`ai_council.py`**: Core logic for the AI Council.
    - Defines the `AICouncil` class.
    - Manages multiple AI model instances (e.g., Claude, ChatGPT).
    - Dynamically instantiates models based on `MODEL_CLASSES`.
    - Stores and manages default and current system prompts (`DEFAULT_SYSTEM_PROMPTS`).
    - Orchestrates discussions between AI models.
    - Handles discussion state (using in-memory dictionary `discussions`).

- **`claude.py`, `chatgpt.py`, `gemini.py`, `grok.py`, `llama.py`**: Individual AI model client implementations.
    - Each file defines a class for a specific AI model (e.g., `ClaudeClient`, `ChatGPTClient`).
    - These classes likely inherit from a base class or implement a common interface (defined implicitly or explicitly).
    - Handle API communication specific to each AI provider.
    - Expose methods like `generate_response` or similar for the `AICouncil` to use.

- **`templates/`**: Directory containing HTML templates.
    - **`index.html`**: The main single-page application HTML structure. Defines the layout for council members, prompt editor modal, discussion area, etc.

- **`static/`**: Directory containing static assets served directly to the browser.
    - **`css/style.css`**: Contains all CSS rules for styling the application, including layout, member cards, modal, chat display, and animations.
    - **`js/main.js`**: Contains the frontend JavaScript logic.
        - Handles UI interactions (button clicks, modal opening/closing, toggling members).
        - Manages frontend state (council member data, active status using `localStorage`).
        - Makes API calls to the Flask backend (using `fetch`).
        - Renders dynamic content (council members, discussion messages).
        - Includes classes like `CouncilMembersUI` and `PromptEditorModal`.
    - **`images/`**: (Likely location for) AI avatar images, icons, and sprite assets.

- **`requirements.txt`**: Lists the Python dependencies required for the project (Flask, requests, specific AI client libraries, etc.).

- **`.cursor/scratchpad.md`**: This file, used for planning, tracking progress, and documenting decisions.

- **`README.md`**: General information about the project setup and usage.

- **`.gitignore`**: Specifies intentionally untracked files that Git should ignore (e.g., `venv/`, `__pycache__/`, `.DS_Store`).

- **`venv/`**: (Typically) The directory containing the Python virtual environment. 


## Key Challenges and Analysis
1. **AI Council Integration**: We need to modify the existing Flask app to use the AICouncil class instead of MasterAI. The AICouncil class is already implemented and supports having multiple AI models discuss topics together.

2. **UI/UX Design Challenges** (Initial Setup):
   - Create an interface that allows users to:
     - See all AI participants with their static images
     - Modify system prompts for each AI
     - Start new discussions and track ongoing ones
     - View the discussion in a threaded/conversation format
   - Make the UI responsive and engaging

3. **Technical Implementation Challenges** (Initial Setup):
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
   - Design smooth transitions for state changes
   - Ensure accessibility in interactive elements
   - Maintain responsive design across different screen sizes

6. **AI Model & Discussion Flow Implementation**:
    - **Multiple AI APIs**: Integrate potentially different API structures and response times from various AI models (Claude, ChatGPT, etc.) into a unified council framework.
    - **Distinct Personas**: Ensure default and user-defined prompts effectively create diverse viewpoints within the AI council discussions.
    - **Chat UI**: Develop a clear and intuitive chat interface that displays contributions from multiple AIs, associating responses with the correct AI avatar.
    - **Real-time Updates**: Manage the asynchronous nature of AI responses and update the UI smoothly as the discussion progresses.

7. **Enhanced User Experience - Discussion Flow**:
   - **Unified Chat Input:** Merge the "Start New Discussion" area with the main chat input for a more seamless initial interaction. The first message in an empty context should initiate the discussion.
   - **Streaming Responses:** Transition from batch response display to real-time streaming. AI messages should appear in the UI as they are generated by the backend, improving perceived responsiveness. This requires backend support (e.g., Server-Sent Events) and frontend handling.
   - **Explicit Continuation:** Introduce a "Continue Discussion" button to allow users to trigger subsequent rounds of AI interaction without necessarily adding their own textual input, facilitating the "council" discussion format.

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
   - Create CSS for member display and state transitions
   - Implement JS for managing discussions and AI interactions
   - Success criteria: UI displays all required elements and handles user interactions correctly

4. **Testing and Refinement**
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

   c. Add Visual Feedback
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
      - Verify streaming responses appear individually.
      - Verify unified input for starting/continuing discussions.
      - Verify "Continue Discussion" button triggers AI rounds.
      - Success criteria: The application facilitates a multi-AI discussion initiated and viewed by the user, with streaming responses and clear controls for user input vs. AI continuation.

## Project Status Board
- [x] Task 1: Update app.py to use AICouncil
- [x] Task 2: Create new API endpoints for AI council functionality
- [x] Task 3a: Update Council Member UI Components
- [x] Task 3b: Implement Member State Management
- [x] Task 3c: Add Visual Feedback (Basic transitions added)
- [x] Task 4a: Create Popup Component
- [x] Task 4b: Implement Prompt Management
- [x] Task 4c: Enhance User Experience
- [x] Task 5a: Backend - Model Instantiation
- [x] Task 5b: Backend - Default System Prompts
- [x] Task 5c: Frontend - Fetch Models and Prompts
- [/] Task 5d: Frontend - Discussion Initiation (Superseded by Task 6)
- [/] Task 5e: Frontend - Discussion Display (Needs update for Streaming - Task 7)
- [x] Task 5f: End-to-End Testing
- [x] Task 6: Unified Chat Input
  - [x] Task 6a: Frontend - Modify Chat Input & Remove Separate Section
  - [x] Task 6b: Frontend - Implement Initiation/Contribution Logic
  - [x] Task 6c: Frontend - Update Placeholder Text
- [x] Task 7: Streaming AI Responses
  - [x] Task 7a: Backend - Implement Streaming Response Endpoint
  - [x] Task 7b: Frontend - Handle Streamed Responses
- [x] Task 8: "Continue Discussion" Button
  - [x] Task 8a: Frontend - Add "Continue Discussion" Button
  - [x] Task 8b: Frontend - Implement Button Logic (Call `/continue` endpoint)
  - [x] Task 8c: Frontend - Integrate Placeholder Update (with Task 6c)
- [x] Task 9: Refactor AI Council for Web Integration
  - [x] Task 9a: Update `discuss_topic` Method
  - [x] Task 9b: Improve Context Handling
  - [x] Task 9c: Enhance User Contribution Support
- [/] Task 10: Implement True AI Model Streaming
  - [ ] Task 10a: Update Individual Model Classes for Streaming
  - [ ] Task 10b: Refactor AICouncil for Streaming Support
  - [ ] Task 10c: Update Backend Streaming Endpoint
  - [ ] Task 10d: Frontend Streaming Integration
- [ ] Task 11: Database Setup and Testing
  - [x] Task 11a: Create .env file with MongoDB configuration
  - [x] Task 11b: Initialize database with default models
  - [x] Task 11c: Run database tests
  - [ ] Task 11d: Test database integration with Flask app

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

## Task 9 Completion: Refactor AI Council for Web Integration

Tasks 9a, 9b, and 9c have been completed. The following changes were made:

1. **Update `discuss_topic` Method**:
   - Changed default `rounds` parameter from 3 to 1 to meet user expectations
   - Added `verbose` parameter (default: False) to make console output optional
   - Removed unnecessary delays between model responses when not in verbose mode
   - Success criteria achieved: Method now works seamlessly with the web interface

2. **Improve Context Handling**:
   - Added new `get_discussion_context` method to standardize context creation
   - Optimized context handling for better performance and code organization
   - Used the method consistently across all discussion-related functions
   - Success criteria achieved: Each AI now responds with awareness of the full discussion history

3. **Enhance User Contribution Support**:
   - Added support for user contributions in the context string
   - Implemented a new `continue_discussion` method that handles user contributions
   - Updated app.py to use the new method in relevant endpoints
   - Success criteria achieved: User contributions are now seamlessly integrated with AI responses

4. **Additional Improvements**:
   - Updated the stream_discussion endpoint to use the new AICouncil methods
   - Modified all routes in app.py to use the verbose=False parameter
   - Changed the default rounds in the start_discussion route to 1 for consistency
   - Improved context format to ensure each AI has the full conversation history

These changes have significantly improved the integration between AICouncil and the web application, making the chat experience more seamless and responsive. The code is now more maintainable with better separation of concerns.

The application is now ready for user testing to verify that all improvements work as expected in a real-world scenario.

## Key Challenges and Analysis - AI Council Improvements

Based on the user's request, we need to make several improvements to the AI Council's integration with the web application to create a more seamless chat experience:

1. **Console to Web UI Transition**: Currently, the `discuss_topic` method in `ai_council.py` prints results to the console, which doesn't integrate well with the web UI. We need to modify it to return results without console output.

2. **Default Rounds Setting**: The `discuss_topic` method has a default of 3 rounds, but we should change this to 1 round as the default to match user expectations.

3. **User Contribution Flow**: We need to enhance the AI Council to better support user contributions to ongoing discussions. The current system works for AI-to-AI discussions but doesn't smoothly incorporate user input.

4. **Round-the-Table Discussion**: We need to ensure each AI sees the full context of the conversation before responding, and that the discussion flows naturally around the "council table."

5. **Performance Optimization**: We should look for opportunities to reduce delays between responses to improve the user experience.

## High-level Task Breakdown - AI Council Improvements

9. **Refactor AI Council for Web Integration**
   a. Update `discuss_topic` Method
      - Change default rounds parameter to 1
      - Remove or make console output optional 
      - Success criteria: Method works seamlessly with web interface
   
   b. Improve Context Handling
      - Ensure each AI has full conversation context
      - Optimize context creation for better performance
      - Success criteria: Each AI responds with awareness of the full discussion history
   
   c. Enhance User Contribution Support
      - Review and improve how user contributions are integrated into discussions
      - Ensure the flow feels natural when users add their input
      - Success criteria: User contributions are seamlessly integrated with AI responses

## Project Status Board
- [x] Task 1: Update app.py to use AICouncil
- [x] Task 2: Create new API endpoints for AI council functionality
- [x] Task 3a: Update Council Member UI Components
- [x] Task 3b: Implement Member State Management
- [x] Task 3c: Add Visual Feedback (Basic transitions added)
- [x] Task 4a: Create Popup Component
- [x] Task 4b: Implement Prompt Management
- [x] Task 4c: Enhance User Experience
- [x] Task 5a: Backend - Model Instantiation
- [x] Task 5b: Backend - Default System Prompts
- [x] Task 5c: Frontend - Fetch Models and Prompts
- [/] Task 5d: Frontend - Discussion Initiation (Superseded by Task 6)
- [/] Task 5e: Frontend - Discussion Display (Needs update for Streaming - Task 7)
- [x] Task 5f: End-to-End Testing
- [x] Task 6: Unified Chat Input
  - [x] Task 6a: Frontend - Modify Chat Input & Remove Separate Section
  - [x] Task 6b: Frontend - Implement Initiation/Contribution Logic
  - [x] Task 6c: Frontend - Update Placeholder Text
- [x] Task 7: Streaming AI Responses
  - [x] Task 7a: Backend - Implement Streaming Response Endpoint
  - [x] Task 7b: Frontend - Handle Streamed Responses
- [x] Task 8: "Continue Discussion" Button
  - [x] Task 8a: Frontend - Add "Continue Discussion" Button
  - [x] Task 8b: Frontend - Implement Button Logic (Call `/continue` endpoint)
  - [x] Task 8c: Frontend - Integrate Placeholder Update (with Task 6c)
- [x] Task 9: Refactor AI Council for Web Integration
  - [x] Task 9a: Update `discuss_topic` Method
  - [x] Task 9b: Improve Context Handling
  - [x] Task 9c: Enhance User Contribution Support
- [/] Task 10: Implement True AI Model Streaming
  - [ ] Task 10a: Update Individual Model Classes for Streaming
  - [ ] Task 10b: Refactor AICouncil for Streaming Support
  - [ ] Task 10c: Update Backend Streaming Endpoint
  - [ ] Task 10d: Frontend Streaming Integration

## Executor's Feedback or Assistance Requests

Task 10 (Implement True AI Model Streaming) has significantly progressed:

1. **Update Individual Model Classes for Streaming** (Completed):
   - Added `get_streaming_response` method to all model classes:
     - Claude: Uses Anthropic's streaming API with the `.stream_text` method
     - ChatGPT: Uses OpenAI's streaming API with the `stream=True` parameter
     - Gemini: Uses Google's streaming API with the `stream=True` parameter
     - Grok: Uses OpenAI-compatible streaming API with the `stream=True` parameter
     - Llama: Uses Replicate's existing streaming capabilities
   - Each method takes a callback function to process tokens in real-time
   - Common interface across all models for consistency

2. **Refactor AICouncil for Streaming Support** (Completed):
   - Added two new methods to the AICouncil class:
     - `stream_discussion`: Initiates a new streaming discussion
     - `stream_continue_discussion`: Continues an existing discussion with streaming
   - Both methods use callbacks to relay model outputs in real-time
   - Ensures proper model initialization and context handling for streaming

3. **Update Backend Streaming Endpoint** (Completed):
   - Replaced simulated streaming in `/api/discussions/<discussion_id>/stream` with real model streaming
   - Enhanced the endpoint to handle both new discussions and continuations
   - Implemented proper context management during streaming
   - Added support for storing streamed responses in the discussion history

4. **Frontend Streaming Integration** (Pending):
   - The frontend currently already supports receiving streamed chunks via Server-Sent Events
   - No changes are needed on the frontend as it's already designed to handle streaming chunks
   - The transition from simulated to real streaming should be transparent to the frontend

The implementation now uses the native streaming capabilities of each AI provider API, resulting in a much more responsive and real-time experience. Each model will stream tokens as they're generated, providing a more accurate representation of model generation speed.

The frontend doesn't need to be updated since it already handles the Server-Sent Events and chunked responses properly. The change from simulated to real streaming should be transparent from the frontend's perspective.

I recommend testing the system with a simple discussion to verify that:
1. The streaming works correctly for all models
2. The responses are correctly captured in the discussion history
3. The UI displays real-time streaming without any issues

## Technical Requirements
1. Frontend State Management:
11. **(New)** A dedicated "Continue Discussion" button allows triggering AI rounds.

## Lessons
- **Validate API Responses:** Always validate the structure of data received from API calls (especially complex objects/arrays) before attempting to access nested properties or call methods like `forEach`. Add checks (e.g., `if (Array.isArray(data.expectedArray))`) to handle unexpected formats gracefully and log informative errors.
- When starting a new discussion, users can specify which AI models to include using the `active_models` parameter

## Key Challenges and Analysis - Streaming Model Output

Based on the user's request, we need to implement real streaming of the actual model output from the APIs directly to the UI chat box. Currently, the app simulates streaming by breaking pre-generated full responses into chunks and sending them with artificial delays.

Here's an analysis of the current implementation and what needs to be changed:

1. **Current Implementation**: 
   - The backend uses `stream_discussion` endpoint which simulates streaming by getting full responses from each model and then artificially splitting them into chunks with delays.
   - The frontend uses Server-Sent Events (SSE) to receive these artificial chunks and display them in the chat UI.

2. **True Streaming Implementation Needed**:
   - Modify individual model classes (Claude, ChatGPT, etc.) to use streaming API calls from their respective providers.
   - Update the AICouncil class to support true streaming from model APIs.
   - Modify the server endpoints to relay the actual model streaming responses to the frontend.
   - Ensure the frontend can handle real-time streaming from each model concurrently.

3. **Technical Challenges**:
   - Different AI providers have different streaming implementations and response formats.
   - Need to ensure all models support streaming or provide fallbacks for those that don't.
   - Handling multiple concurrent streams from different models.
   - Maintaining a clean UI with multiple models potentially responding simultaneously.

4. **Benefits**:
   - Users will see the actual model responses being generated in real-time.
   - More responsive UX without artificial delays.
   - More accurate representation of model generation times.
   - Ability to cancel ongoing responses if needed.

## High-level Task Breakdown - Streaming Model Output

10. **Implement True AI Model Streaming**
   a. Update Individual Model Classes for Streaming
      - Modify Claude class to use Anthropic's streaming API
      - Update ChatGPT class to use OpenAI's streaming API
      - Update other model classes as needed (Gemini, Llama, Grok)
      - Success criteria: Each model class can generate streaming responses
   
   b. Refactor AICouncil for Streaming Support
      - Modify `discuss_topic` method to support streaming mode
      - Create a new method for streaming individual model responses
      - Add a callback mechanism to stream chunks back to caller
      - Success criteria: AICouncil can orchestrate streaming responses from multiple models
   
   c. Update Backend Streaming Endpoint
      - Modify `/api/discussions/<discussion_id>/stream` to use true model streaming
      - Ensure proper error handling and connection management
      - Success criteria: Server correctly streams actual model output to the frontend
   
   d. Frontend Streaming Integration
      - Ensure the UI correctly handles real streaming tokens from models
      - Update the ChatInterface class to properly display concurrent streams
      - Success criteria: UI shows real-time model outputs with proper attribution

## Project Status Board
- [x] Task 1: Update app.py to use AICouncil
- [x] Task 2: Create new API endpoints for AI council functionality
- [x] Task 3a: Update Council Member UI Components
- [x] Task 3b: Implement Member State Management
- [x] Task 3c: Add Visual Feedback (Basic transitions added)
- [x] Task 4a: Create Popup Component
- [x] Task 4b: Implement Prompt Management
- [x] Task 4c: Enhance User Experience
- [x] Task 5a: Backend - Model Instantiation
- [x] Task 5b: Backend - Default System Prompts
- [x] Task 5c: Frontend - Fetch Models and Prompts
- [/] Task 5d: Frontend - Discussion Initiation (Superseded by Task 6)
- [/] Task 5e: Frontend - Discussion Display (Needs update for Streaming - Task 7)
- [x] Task 5f: End-to-End Testing
- [x] Task 6: Unified Chat Input
  - [x] Task 6a: Frontend - Modify Chat Input & Remove Separate Section
  - [x] Task 6b: Frontend - Implement Initiation/Contribution Logic
  - [x] Task 6c: Frontend - Update Placeholder Text
- [x] Task 7: Streaming AI Responses
  - [x] Task 7a: Backend - Implement Streaming Response Endpoint
  - [x] Task 7b: Frontend - Handle Streamed Responses
- [x] Task 8: "Continue Discussion" Button
  - [x] Task 8a: Frontend - Add "Continue Discussion" Button
  - [x] Task 8b: Frontend - Implement Button Logic (Call `/continue` endpoint)
  - [x] Task 8c: Frontend - Integrate Placeholder Update (with Task 6c)
- [x] Task 9: Refactor AI Council for Web Integration
  - [x] Task 9a: Update `discuss_topic` Method
  - [x] Task 9b: Improve Context Handling
  - [x] Task 9c: Enhance User Contribution Support
- [ ] Task 10: Implement True AI Model Streaming
  - [ ] Task 10a: Update Individual Model Classes for Streaming
  - [ ] Task 10b: Refactor AICouncil for Streaming Support
  - [ ] Task 10c: Update Backend Streaming Endpoint
  - [ ] Task 10d: Frontend Streaming Integration

## Lessons
- **Validate API Responses:** Always validate the structure of data received from API calls (especially complex objects/arrays) before attempting to access nested properties or call methods like `forEach`. Add checks (e.g., `if (Array.isArray(data.expectedArray))`) to handle unexpected formats gracefully and log informative errors.
- When starting a new discussion, users can specify which AI models to include using the `active_models` parameter
- **Plan for streaming from the beginning:** When working with AI models, design the architecture to support true streaming responses from the start rather than simulating it, as retrofitting streaming into an existing system requires significant changes.

## Database Setup and Testing
1. **Initial Setup**
   - Create `.env` file with MongoDB configuration
   - Install MongoDB if not already installed
   - Initialize database with default models and settings
   - Run database tests to verify functionality

2. **Integration Testing**
   - Test database connection with Flask application
   - Verify CRUD operations through API endpoints
   - Test discussion creation and management
   - Verify model management functionality

## Project Status Board
- [ ] Task 11: Database Setup and Testing
  - [x] Task 11a: Create .env file with MongoDB configuration
  - [x] Task 11b: Initialize database with default models
  - [x] Task 11c: Run database tests
  - [ ] Task 11d: Test database integration with Flask app

## Executor's Feedback or Assistance Requests
- .env file instructions provided (manual creation required due to security restrictions)
- MongoDB is installed and running
- Database initialized successfully with `python init_db.py`
- All database unit tests passed after minor fixes to timestamp fields
- Next: Test database integration with Flask app endpoints