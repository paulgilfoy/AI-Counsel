from flask import Flask, render_template, request, jsonify
from ai_council import AICouncil
from dotenv import load_dotenv
import os
import uuid
import time
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
    discussion_results = ai_council.discuss_topic(user_message, rounds=1)[0]
    
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
    discussion_results = ai_council.discuss_topic(text, rounds=1)
    
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
    rounds = data.get('rounds', 3)  # Default to 3 rounds
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
        round_results = ai_council.discuss_topic(topic, rounds=1)[0]
        
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
    
    discussion = discussions[discussion_id]
    active_models = discussion['active_models']  # Use the models that were active when discussion started
    
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
        # Create context from all previous rounds
        context = "Previous discussion:\n"
        for round_results in discussion['results']:
            for model_name, response in round_results.items():
                context += f"\n{model_name}: {response}\n"
        
        follow_up_prompt = ai_council.follow_up_prompt_template.format(context=context)
        
        # Get responses from active models for this round
        round_responses = {}
        for model_name, model in ai_council.models.items():
            if model_name in active_models:  # Only get responses from active models
                response = model.get_response(follow_up_prompt)
                round_responses[model_name] = response
        
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
        # Create context from all previous rounds including the user contribution
        context = "Previous discussion:\n"
        for round_results in discussion['results']:
            for model_name, response in round_results.items():
                context += f"\n{model_name}: {response}\n"
        
        context += f"\nUser contribution: {contribution}\n"
        
        # Get responses from active models for this round
        follow_up_prompt = ai_council.follow_up_prompt_template.format(context=context)
        
        round_responses = {}
        for model_name, model in ai_council.models.items():
            if model_name in active_models:  # Only get responses from active models
                response = model.get_response(follow_up_prompt)
                round_responses[model_name] = response
        
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

if __name__ == '__main__':
    app.run(debug=True)