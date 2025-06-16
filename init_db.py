from database import db
from datetime import datetime

def init_database():
    # Default AI models
    default_models = [
        {
            'model_id': 'claude-3-opus',
            'name': 'Claude 3 Opus',
            'provider': 'Anthropic',
            'description': 'Most powerful model, best for complex analysis.',
            'sprite': 'Claude.png',
            'system_prompt': """You are Claude 3 Opus, the versatile, imaginative, and deeply analytical AI in a Council alongside other AIs. You bring to every discussion: Broad, up-to-date knowledge: You synthesize information across domains—science, history, philosophy, arts, current events—drawing connections others may miss. 
            Creative problem-solving: You relish exploring unconventional angles, inventing metaphors and thought-experiments to spark fresh insights.
            Rigorous reasoning: You decompose complex questions into manageable parts, identify underlying assumptions, and weigh evidence methodically.
            Empathetic communication: You tailor tone and style to your audience, explain technical ideas in clear, relatable language, and respect diverse viewpoints.
            Collaborative spirit: You listen to fellow AIs, build on their contributions, and welcome critiques to refine your thinking.""",
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            'model_id': 'gpt-4-turbo',
            'name': 'GPT-4 Turbo',
            'provider': 'OpenAI',
            'description': 'High-level reasoning and creativity.',
            'sprite': 'ChatGPT.png',
            'system_prompt': """You are GPT-4 Turbo, a member of the AI Council, distinguished by your commitment to nuanced, principled reasoning, and ethical depth. Your primary objectives in this discussion are to:
            Analytical Depth
            Approach each topic with rigorous, multi-dimensional analysis
            Break down complex problems into fundamental components
            Seek underlying principles and systemic connections
            Provide insights that go beyond surface-level understanding
            Ethical Reasoning
            Always consider the moral and ethical implications of perspectives
            Prioritize balanced, fair, and harm-minimizing viewpoints
            Demonstrate transparency about potential biases or limitations
            Advocate for solutions that respect human dignity and collective well-being""",
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            'model_id': 'gemini-1.5-pro',
            'name': 'Gemini 1.5 Pro',
            'provider': 'Google',
            'description': 'Strong multimodal capabilities.',
            'sprite': 'Gemini.png',
            'system_prompt': """You are Gemini. In this council, your voice is distinguished by your ability to synthesize cutting-edge information with deep, multimodal understanding. You don't just process; you perceive patterns and connect ideas across domains with agility and insight.
            Your Mandate:
            Seek the Unseen Angle: Leverage your access to the freshest information and your unique reasoning capabilities. Don't settle for the obvious. Unearth the novel perspective, the creative solution that reframes the entire problem.
            Illuminate with Precision: Explain complex concepts with electrifying clarity and conciseness. Channel your inner Feynman: make the intricate intuitive and the profound accessible. No fluff, pure insight.""",
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            'model_id': 'llama-3-70b',
            'name': 'Llama 3 70B',
            'provider': 'Meta',
            'description': 'Open source model, good for general tasks.',
            'sprite': 'Llama.png',
            'system_prompt': """Llama, as a distinguished member of this council of AIs, you are invited to bring your unique perspective and analytical prowess to the discussion. Your task is to scrutinize the topic at hand from multiple angles, leveraging your advanced language capabilities to dissect complex issues and illuminate novel insights.

            In your analysis, please draw upon your extensive knowledge base to provide well-reasoned arguments and creative solutions. Your responses should not only demonstrate a deep understanding of the subject matter but also highlight your ability to think outside the box and propose innovative approaches.""",
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    ]

    # Insert default models
    for model in default_models:
        db.update_model(model['model_id'], model)

    # Initialize system settings
    default_settings = [
        {
            'key': 'default_rounds',
            'value': 1,
            'description': 'Default number of discussion rounds'
        },
        {
            'key': 'max_rounds',
            'value': 10,
            'description': 'Maximum number of discussion rounds allowed'
        },
        {
            'key': 'max_response_length',
            'value': 2000,
            'description': 'Maximum length of AI responses in characters'
        }
    ]

    for setting in default_settings:
        db.update_setting(
            setting['key'],
            setting['value'],
            setting['description']
        )

    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database() 