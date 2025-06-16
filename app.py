from flask import Flask, render_template, request, jsonify
from ai_council import AICouncil
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')

# Initialize the AICouncil
ai_council = AICouncil()

# Get list of available models
def get_available_models():
    return list(ai_council.models.keys())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get list of available AI models"""
    return jsonify({
        'status': 'success',
        'models': get_available_models()
    })

@app.route('/api/prompts', methods=['GET'])
def get_prompts():
    """Get current system prompts for all models"""
    return jsonify({
        'status': 'success',
        'prompts': ai_council.system_prompts
    })

@app.route('/api/prompts', methods=['POST'])
def update_prompts():
    """Update system prompts for specified models"""
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

@app.route('/api/discuss', methods=['POST'])
def discuss():
    """Start a new discussion with the AI Council"""
    data = request.get_json()
    topic = data.get('topic', '')
    active_models = data.get('active_models', get_available_models())
    
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
    
    try:
        # Get responses from all active models
        responses = ai_council.discuss_topic(topic, rounds=1, verbose=False)[0]
        
        # Filter responses to only include active models
        filtered_responses = {model: response for model, response in responses.items() if model in active_models}
        
        return jsonify({
            'status': 'success',
            'results': filtered_responses
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error in discussion: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)