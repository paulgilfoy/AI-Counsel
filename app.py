from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from ai_council import AICouncil
from dotenv import load_dotenv
import os
import uuid
import time
import json
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')

# Initialize the AICouncil
ai_council = AICouncil()

# In-memory storage for discussions
# In a production app, this would be a database
discussions = {}

# Get list of available models
def get_available_models():
    # Use the keys from the dynamic model loading
    return list(ai_council.models.keys()) # Returns keys of successfully initialized models

# Get default prompts
def get_default_prompts():
    # Import or access the defaults defined in ai_council.py
    from ai_council import DEFAULT_SYSTEM_PROMPTS
    # Filter defaults to only include models that are currently recognized/available
    available_models = get_available_models()
    return {name: prompt for name, prompt in DEFAULT_SYSTEM_PROMPTS.items() if name in available_models}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    active_models = data.get('active_models', get_available_models())  # Default to all models if not specified
    
    if not user_message:
        return jsonify({
            'status': 'error',
            'message': 'No message provided'
        }), 400
    
    # Validate active_models
    available_models = get_available_models()
    invalid_models = [model for model in active_models if model not in available_models]
    if invalid_models:
        return jsonify({
            'status': 'error',
            'message': f'Invalid models specified: {", ".join(invalid_models)}'
        }), 400
    
    # Start a discussion with only the active models
    discussion_results = ai_council.discuss_topic(user_message, rounds=1, verbose=False)[0]
    
    # Filter responses to only include active models
    responses = {model: response for model, response in discussion_results.items() if model in active_models}
    
    return jsonify({
        'status': 'success',
        'responses': responses
    })

@app.route('/api/process', methods=['POST'])
def process_text():
    data = request.get_json()
    text = data.get('text', '')
    
    # Start a discussion with the AI Council (1 round)
    discussion_results = ai_council.discuss_topic(text, rounds=1, verbose=False)
    
    # Format the response
    responses = {}
    for model_name, response in discussion_results[0].items():
        responses[model_name] = response
    
    return jsonify({
        'status': 'success',
        'responses': responses
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    """
    Get the list of available AI models in the council
    """
    model_names = list(ai_council.models.keys())
    return jsonify({
        'status': 'success',
        'models': model_names
    })

@app.route('/api/models/defaults', methods=['GET'])
def get_model_defaults():
    """
    Get the default system prompts for available models
    """
    default_prompts = get_default_prompts()
    return jsonify({
        'status': 'success',
        'defaults': default_prompts
    })

@app.route('/api/prompts', methods=['GET'])
def get_prompts():
    """
    Get the current system prompts for all models
    """
    return jsonify({
        'status': 'success',
        'prompts': ai_council.system_prompts
    })

@app.route('/api/prompts', methods=['POST'])
def update_prompts():
    """
    Update system prompts for one or more models
    """
    data = request.get_json()
    prompts = data.get('prompts', {})
    
    if not prompts:
        return jsonify({
            'status': 'error',
            'message': 'No prompts provided'
        }), 400
    
    ai_council.update_all_system_prompts(prompts)
    
    return jsonify({
        'status': 'success',
        'message': 'Prompts updated successfully'
    })

@app.route('/api/discussions', methods=['GET'])
def list_discussions():
    """
    Get a list of all discussions
    """
    discussion_list = []
    for id, discussion in discussions.items():
        discussion_list.append({
            'id': id,
            'topic': discussion['topic'],
            'created_at': discussion['created_at'],
            'rounds': len(discussion['results']),
            'status': discussion['status']
        })
    
    return jsonify({
        'status': 'success',
        'discussions': discussion_list
    })

@app.route('/api/discussions', methods=['POST'])
def start_discussion():
    """
    Start a new discussion with the AI Council
    """
    data = request.get_json()
    topic = data.get('topic', '')
    rounds = data.get('rounds', 1)  # Default to 1 round
    active_models = data.get('active_models', get_available_models())  # Default to all models if not specified
    
    if not topic:
        return jsonify({
            'status': 'error',
            'message': 'No topic provided'
        }), 400
    
    # Validate active_models
    available_models = get_available_models()
    invalid_models = [model for model in active_models if model not in available_models]
    if invalid_models:
        return jsonify({
            'status': 'error',
            'message': f'Invalid models specified: {", ".join(invalid_models)}'
        }), 400
    
    # Generate a unique ID for this discussion
    discussion_id = str(uuid.uuid4())
    
    # Store initial discussion details
    discussions[discussion_id] = {
        'topic': topic,
        'created_at': datetime.now().isoformat(),
        'status': 'in_progress',
        'rounds_requested': rounds,
        'active_models': active_models,  # Store which models are active for this discussion
        'results': []
    }
    
    try:
        # Start the first round
        round_results = ai_council.discuss_topic(topic, rounds=1, verbose=True)[0]
        
        # Filter responses to only include active models
        filtered_results = {model: response for model, response in round_results.items() if model in active_models}
        discussions[discussion_id]['results'].append(filtered_results)
        
        return jsonify({
            'status': 'success',
            'discussion_id': discussion_id,
            'results': filtered_results
        })
    except Exception as e:
        discussions[discussion_id]['status'] = 'error'
        return jsonify({
            'status': 'error',
            'message': f'Error starting discussion: {str(e)}'
        }), 500

@app.route('/api/discussions/<discussion_id>', methods=['GET'])
def get_discussion(discussion_id):
    """
    Get the details and results of a specific discussion
    """
    if discussion_id not in discussions:
        return jsonify({
            'status': 'error',
            'message': 'Discussion not found'
        }), 404
    
    discussion = discussions[discussion_id]
    
    return jsonify({
        'status': 'success',
        'discussion': {
            'id': discussion_id,
            'topic': discussion['topic'],
            'created_at': discussion['created_at'],
            'status': discussion['status'],
            'rounds': len(discussion['results']),
            'results': discussion['results']
        }
    })

@app.route('/api/discussions/<discussion_id>/continue', methods=['POST'])
def continue_discussion(discussion_id):
    """
    Continue an existing discussion by adding more rounds
    """
    if discussion_id not in discussions:
        return jsonify({
            'status': 'error',
            'message': 'Discussion not found'
        }), 404
    
    # Get rounds from request
    data = request.get_json() or {}
    rounds = data.get('rounds', 1)  # Default to 1 additional round if not specified
    
    discussion = discussions[discussion_id]
    active_models = discussion['active_models']  # Use the models that were active when discussion started
    
    # Update requested rounds if specified
    if 'rounds' in data:
        # Set the total requested rounds to current completed rounds + new rounds requested
        discussion['rounds_requested'] = len(discussion['results']) + rounds
    
    # Check if discussion is already complete
    if discussion['status'] == 'complete':
        return jsonify({
            'status': 'error',
            'message': 'Discussion is already complete'
        }), 400
    
    # Check if there are more rounds to be conducted
    completed_rounds = len(discussion['results'])
    if completed_rounds >= discussion['rounds_requested']:
        discussion['status'] = 'complete'
        return jsonify({
            'status': 'success',
            'message': 'Discussion is already complete',
            'discussion': {
                'id': discussion_id,
                'rounds': completed_rounds,
                'status': 'complete'
            }
        })
    
    try:
        # Use AICouncil's continue_discussion method to get responses
        round_responses = ai_council.continue_discussion(
            discussion=discussion['results'],
            active_models=active_models
        )
        
        # Store this round's results
        discussion['results'].append(round_responses)
        
        # Check if this was the last requested round
        if len(discussion['results']) >= discussion['rounds_requested']:
            discussion['status'] = 'complete'
        
        return jsonify({
            'status': 'success',
            'discussion_id': discussion_id,
            'round': len(discussion['results']),
            'results': round_responses,
            'complete': discussion['status'] == 'complete'
        })
    except Exception as e:
        discussion['status'] = 'error'
        return jsonify({
            'status': 'error',
            'message': f'Error continuing discussion: {str(e)}'
        }), 500

@app.route('/api/discussions/<discussion_id>/contribute', methods=['POST'])
def contribute_to_discussion(discussion_id):
    """
    Add a user contribution to an ongoing discussion
    """
    if discussion_id not in discussions:
        return jsonify({
            'status': 'error',
            'message': 'Discussion not found'
        }), 404
    
    data = request.get_json()
    contribution = data.get('contribution', '')
    
    if not contribution:
        return jsonify({
            'status': 'error',
            'message': 'No contribution provided'
        }), 400
    
    discussion = discussions[discussion_id]
    active_models = discussion['active_models']  # Use the models that were active when discussion started
    
    # Check if discussion is already complete
    if discussion['status'] == 'complete':
        return jsonify({
            'status': 'error',
            'message': 'Discussion is already complete'
        }), 400
    
    try:
        # Use AICouncil's continue_discussion method to get responses with user contribution
        round_responses = ai_council.continue_discussion(
            discussion=discussion['results'],
            active_models=active_models,
            user_contribution=contribution
        )
        
        # Store this round's results
        discussion['results'].append(round_responses)
        
        return jsonify({
            'status': 'success',
            'discussion_id': discussion_id,
            'round': len(discussion['results']),
            'results': round_responses
        })
    except Exception as e:
        discussion['status'] = 'error'
        return jsonify({
            'status': 'error',
            'message': f'Error adding contribution: {str(e)}'
        }), 500

@app.route('/api/discussions/<discussion_id>/models', methods=['GET'])
def get_discussion_models(discussion_id):
    """
    Get the active models for a specific discussion
    """
    if discussion_id not in discussions:
        return jsonify({
            'status': 'error',
            'message': 'Discussion not found'
        }), 404
    
    discussion = discussions[discussion_id]
    
    return jsonify({
        'status': 'success',
        'active_models': discussion['active_models'],
        'available_models': get_available_models()
    })

@app.route('/api/discussions/<discussion_id>/stream', methods=['GET', 'POST'])
def stream_discussion(discussion_id):
    """
    Stream the AI responses for a discussion using Server-Sent Events (SSE)
    """
    if discussion_id not in discussions:
        return jsonify({
            'status': 'error',
            'message': 'Discussion not found'
        }), 404
        
    discussion = discussions[discussion_id]
    
    # Only allow streaming for in-progress discussions
    if discussion['status'] != 'in_progress':
        return jsonify({
            'status': 'error',
            'message': f'Discussion is {discussion["status"]}, not in_progress'
        }), 400
    
    # For POST requests, first continue the discussion in the background
    if request.method == 'POST':
        # Get rounds from request or use default
        data = request.get_json() or {}
        rounds = data.get('rounds', 1)  # Default to 1 round
        
        # Update requested rounds if specified
        if 'rounds' in data:
            discussion['rounds_requested'] = rounds
        
        # Create a new round in the discussion results
        discussion['results'].append({})
    
    @stream_with_context
    def generate():
        # Send the event format and data
        yield 'event: stream_start\n'
        yield f'data: {{"discussion_id": "{discussion_id}", "rounds_requested": {discussion["rounds_requested"]}}}\n\n'
        
        # Get reference to the active models for this discussion
        active_models = discussion.get('active_models', list(ai_council.models.keys()))
        
        try:
            # Get context string from AICouncil
            context_str = ai_council.get_discussion_context(discussion['results'])
            
            # Start generating responses for each active model
            for model_name in active_models:
                if model_name not in ai_council.models:
                    continue  # Skip models that aren't loaded
                
                # Send event indicating model is starting
                yield f'event: model_start\n'
                yield f'data: {{"model": "{model_name}"}}\n\n'
                
                # Get the model's response (in a real implementation, this would use streaming)
                # For now, we'll simulate streaming by sending chunks of the response
                model = ai_council.models[model_name]
                
                # Instead of getting the full response at once, we'd ideally get it in chunks
                # This is a simplified example
                follow_up_prompt = ai_council.follow_up_prompt_template.format(context=context_str)
                full_response = model.get_response(follow_up_prompt)
                
                # Split the response into words to simulate streaming
                words = full_response.split()
                chunks = [' '.join(words[i:i+5]) for i in range(0, len(words), 5)]
                
                # Send each chunk as an update
                for chunk in chunks:
                    yield f'event: model_update\n'
                    yield f'data: {{"model": "{model_name}", "chunk": {json.dumps(chunk)}}}\n\n'
                    time.sleep(0.1)  # Simulate delay between chunks
                
                # Send event indicating model is complete
                yield f'event: model_complete\n'
                yield f'data: {{"model": "{model_name}", "response": {json.dumps(full_response)}}}\n\n'
                
                # Store the response in the discussion results
                # For now, let's append to the current round if it exists, otherwise create a new round
                if not discussion['results']:
                    discussion['results'].append({})
                
                # Add or update this model's response in the latest round
                discussion['results'][-1][model_name] = full_response
            
            # Send event indicating all models are complete
            yield 'event: stream_complete\n'
            yield f'data: {{"rounds": {len(discussion["results"])}, "rounds_requested": {discussion["rounds_requested"]}}}\n\n'
            
            # Check if this was the last requested round and update status
            if len(discussion['results']) >= discussion['rounds_requested']:
                discussion['status'] = 'complete'
            
        except Exception as e:
            # Send error event
            error_msg = str(e)
            yield f'event: stream_error\n'
            yield f'data: {{"error": {json.dumps(error_msg)}}}\n\n'
            
            # Update discussion status
            discussion['status'] = 'error'
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)