from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from ai_council import AICouncil
from dotenv import load_dotenv
from database import db
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
    models = db.get_all_models()
    return jsonify({
        'status': 'success',
        'models': [model['model_id'] for model in models]
    })

@app.route('/api/models/defaults', methods=['GET'])
def get_model_defaults():
    """
    Get the default system prompts for available models
    """
    models = db.get_all_models()
    defaults = {model['model_id']: model['system_prompt'] for model in models}
    return jsonify({
        'status': 'success',
        'defaults': defaults
    })

@app.route('/api/prompts', methods=['GET'])
def get_prompts():
    """
    Get the current system prompts for all models
    """
    models = db.get_all_models()
    prompts = {model['model_id']: model['system_prompt'] for model in models}
    return jsonify({
        'status': 'success',
        'prompts': prompts
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
    
    for model_id, prompt in prompts.items():
        db.update_model(model_id, {'system_prompt': prompt})
    
    return jsonify({
        'status': 'success',
        'message': 'Prompts updated successfully'
    })

@app.route('/api/discussions', methods=['GET'])
def list_discussions():
    """
    Get a list of all discussions
    """
    discussions = db.get_all_discussions()
    discussion_list = []
    for discussion in discussions:
        discussion_list.append({
            'id': discussion['discussion_id'],
            'topic': discussion['topic'],
            'created_at': discussion['created_at'].isoformat(),
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
    
    # Create discussion in database
    discussion_data = {
        'discussion_id': discussion_id,
        'topic': topic,
        'rounds_requested': rounds,
        'active_models': active_models,
        'metadata': {
            'total_rounds': 0,
            'last_activity': datetime.utcnow()
        }
    }
    
    db.create_discussion(discussion_data)
    
    try:
        # Start the first round
        round_results = ai_council.discuss_topic(topic, rounds=1, verbose=True)[0]
        
        # Filter responses to only include active models
        filtered_results = {model: response for model, response in round_results.items() if model in active_models}
        
        # Add round to discussion
        round_data = {
            'round_number': 1,
            'responses': filtered_results,
            'timestamp': datetime.utcnow()
        }
        db.add_discussion_round(discussion_id, round_data)
        
        return jsonify({
            'status': 'success',
            'discussion_id': discussion_id,
            'results': filtered_results
        })
    except Exception as e:
        db.update_discussion_status(discussion_id, 'error')
        return jsonify({
            'status': 'error',
            'message': f'Error starting discussion: {str(e)}'
        }), 500

@app.route('/api/discussions/<discussion_id>', methods=['GET'])
def get_discussion(discussion_id):
    """
    Get the details and results of a specific discussion
    """
    discussion = db.get_discussion(discussion_id)
    if not discussion:
        return jsonify({
            'status': 'error',
            'message': 'Discussion not found'
        }), 404
    
    return jsonify({
        'status': 'success',
        'discussion': {
            'id': discussion['discussion_id'],
            'topic': discussion['topic'],
            'created_at': discussion['created_at'].isoformat(),
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
    discussion = db.get_discussion(discussion_id)
    if not discussion:
        return jsonify({
            'status': 'error',
            'message': 'Discussion not found'
        }), 404
    
    # Get rounds from request
    data = request.get_json() or {}
    rounds = data.get('rounds', 1)  # Default to 1 additional round if not specified
    
    active_models = discussion['active_models']  # Use the models that were active when discussion started
    
    # Update requested rounds if specified
    if 'rounds' in data:
        # Set the total requested rounds to current completed rounds + new rounds requested
        discussion['rounds_requested'] = len(discussion['results']) + rounds
        db.update_model(discussion_id, {'rounds_requested': discussion['rounds_requested']})
    
    # Check if discussion is already complete
    if discussion['status'] == 'complete':
        return jsonify({
            'status': 'error',
            'message': 'Discussion is already complete'
        }), 400
    
    # Check if there are more rounds to be conducted
    completed_rounds = len(discussion['results'])
    if completed_rounds >= discussion['rounds_requested']:
        db.update_discussion_status(discussion_id, 'complete')
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
        
        # Add round to discussion
        round_data = {
            'round_number': len(discussion['results']) + 1,
            'responses': round_responses,
            'timestamp': datetime.utcnow()
        }
        db.add_discussion_round(discussion_id, round_data)
        
        # Check if this was the last requested round
        if len(discussion['results']) + 1 >= discussion['rounds_requested']:
            db.update_discussion_status(discussion_id, 'complete')
        
        return jsonify({
            'status': 'success',
            'discussion_id': discussion_id,
            'round': len(discussion['results']) + 1,
            'results': round_responses,
            'complete': len(discussion['results']) + 1 >= discussion['rounds_requested']
        })
    except Exception as e:
        db.update_discussion_status(discussion_id, 'error')
        return jsonify({
            'status': 'error',
            'message': f'Error continuing discussion: {str(e)}'
        }), 500

@app.route('/api/discussions/<discussion_id>/contribute', methods=['POST'])
def contribute_to_discussion(discussion_id):
    """
    Add a user contribution to an ongoing discussion
    """
    discussion = db.get_discussion(discussion_id)
    if not discussion:
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
    
    active_models = discussion['active_models']  # Use the models that were active when discussion started
    
    # Check if discussion is already complete
    if discussion['status'] == 'complete':
        return jsonify({
            'status': 'error',
            'message': 'Discussion is already complete'
        }), 400
    
    try:
        # Add user contribution to database
        contribution_data = {
            'discussion_id': discussion_id,
            'user_message': contribution,
            'round_number': len(discussion['results']) + 1,
            'active_models': active_models
        }
        db.add_user_contribution(contribution_data)
        
        # Use AICouncil's continue_discussion method to get responses with user contribution
        round_responses = ai_council.continue_discussion(
            discussion=discussion['results'],
            active_models=active_models,
            user_contribution=contribution
        )
        
        # Add round to discussion
        round_data = {
            'round_number': len(discussion['results']) + 1,
            'responses': round_responses,
            'user_contribution': contribution,
            'timestamp': datetime.utcnow()
        }
        db.add_discussion_round(discussion_id, round_data)
        
        return jsonify({
            'status': 'success',
            'discussion_id': discussion_id,
            'round': len(discussion['results']) + 1,
            'results': round_responses
        })
    except Exception as e:
        db.update_discussion_status(discussion_id, 'error')
        return jsonify({
            'status': 'error',
            'message': f'Error adding contribution: {str(e)}'
        }), 500

@app.route('/api/discussions/<discussion_id>/models', methods=['GET'])
def get_discussion_models(discussion_id):
    """
    Get the active models for a specific discussion
    """
    discussion = db.get_discussion(discussion_id)
    if not discussion:
        return jsonify({
            'status': 'error',
            'message': 'Discussion not found'
        }), 404
    
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
            # Get last round number
            current_round = len(discussion['results']) - 1
            
            # Define callback for streaming responses
            def streaming_callback(model_name, chunk, is_complete):
                if is_complete:
                    # Send completion event
                    data = json.dumps({
                        "model": model_name,
                        "response": discussion['results'][current_round].get(model_name, "")
                    })
                    return f'event: model_complete\ndata: {data}\n\n'
                else:
                    # Send chunk update
                    data = json.dumps({
                        "model": model_name,
                        "chunk": chunk
                    })
                    return f'event: model_update\ndata: {data}\n\n'
            
            # Use the user contribution if available from the request
            user_contribution = None
            if request.method == 'POST':
                data = request.get_json() or {}
                user_contribution = data.get('contribution')
            
            # Start streaming the discussion
            if current_round == 0 and not any(discussion['results'][0]):
                # This is a new discussion, start with the initial topic
                topic = discussion['topic']
                
                def callback_wrapper(model_name, chunk, is_complete):
                    # Store chunks in the discussion results as they come in
                    if not is_complete:
                        if model_name not in discussion['results'][current_round]:
                            discussion['results'][current_round][model_name] = ""
                        discussion['results'][current_round][model_name] += chunk
                    
                    # Send the event
                    result = streaming_callback(model_name, chunk, is_complete)
                    if result:
                        yield result
                
                # Send model start events for each active model before streaming
                for model_name in active_models:
                    if model_name in ai_council.models:
                        yield f'event: model_start\n'
                        yield f'data: {{"model": "{model_name}"}}\n\n'
                
                # Stream the initial discussion
                ai_council.stream_discussion(
                    topic=topic,
                    active_models=active_models,
                    callback=callback_wrapper,
                    rounds=1  # Always 1 round for stream_discussion
                )
            else:
                # Continue an existing discussion
                def callback_wrapper(model_name, chunk, is_complete):
                    # Store chunks in the discussion results as they come in
                    if not is_complete:
                        if model_name not in discussion['results'][current_round]:
                            discussion['results'][current_round][model_name] = ""
                        discussion['results'][current_round][model_name] += chunk
                    
                    # Send the event
                    result = streaming_callback(model_name, chunk, is_complete)
                    if result:
                        yield result
                
                # Send model start events for each active model before streaming
                for model_name in active_models:
                    if model_name in ai_council.models:
                        yield f'event: model_start\n'
                        yield f'data: {{"model": "{model_name}"}}\n\n'
                
                # Stream the continuation
                ai_council.stream_continue_discussion(
                    discussion=discussion['results'][:current_round],
                    active_models=active_models,
                    user_contribution=user_contribution,
                    callback=callback_wrapper
                )
            
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