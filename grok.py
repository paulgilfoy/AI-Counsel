import os
from openai import OpenAI
from dotenv import load_dotenv

class Grok:
    def __init__(self, system_prompt=None):
        load_dotenv()
        self.api_key = os.getenv('XAI_API_KEY')
        self.system_prompt = system_prompt or "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.x.ai/v1",
        )
        
    def get_response(self, prompt, stream=False):
        """
        Get a response from Grok using the X.AI API
        
        Args:
            prompt (str): The user's prompt
            stream (bool): Whether to stream the response
            
        Returns:
            str or generator: The model's response or a generator for streaming responses
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]
        
        response = self.client.chat.completions.create(
            model="grok-2-latest",
            messages=messages,
            stream=stream
        )
        
        if stream:
            return response
        else:
            return response.choices[0].message.content 