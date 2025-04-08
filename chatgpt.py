import os
from openai import OpenAI
from dotenv import load_dotenv

class ChatGPT:
    def __init__(self, system_prompt=None):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.system_prompt = system_prompt
        
    def get_response(self, prompt):
        """
        Get a response from ChatGPT
        
        Args:
            prompt (str): The user's prompt
            
        Returns:
            str: The model's response
        """
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=messages,
                temperature=1.0,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting response from ChatGPT: {str(e)}" 