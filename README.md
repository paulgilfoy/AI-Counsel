# AI Council

A system that facilitates discussions between multiple AI models (ChatGPT, Claude, Gemini, Grok, and Llama 2) to collaboratively solve problems and discuss topics.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key
GROK_API_KEY=your_grok_api_key
REPLICATE_API_TOKEN=your_replicate_api_token
```

Note: The Grok API is not yet publicly available, so that component will return placeholder responses.

## Usage

You can use the AI Council in two ways:

1. Run the example discussion:
```bash
python ai_council.py
```

2. Import and use the AICouncil class in your own code:
```python
from ai_council import AICouncil

council = AICouncil()

# Start a discussion
topic = "Your topic or problem here"
system_prompt = "Optional system prompt to guide the discussion"
discussion = council.discuss_topic(topic, rounds=3, system_prompt=system_prompt)
```

## Features

- Facilitates multi-round discussions between AI models
- Each model can build upon others' responses
- Configurable number of discussion rounds
- Customizable system prompts to guide the discussion
- Error handling for API failures
- Rate limiting to prevent API throttling

## Models

- ChatGPT (OpenAI GPT-4)
- Claude (Anthropic Claude 3 Opus)
- Gemini (Google Gemini Pro)
- Grok (X/Tesla - placeholder until API is available)
- Llama 2 (Meta - via Replicate)

## Contributing

Feel free to submit issues and enhancement requests! 