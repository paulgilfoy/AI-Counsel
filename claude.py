import os
from anthropic import Anthropic
from dotenv import load_dotenv

class Claude:
    def __init__(self, system_prompt=None):
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.system_prompt = system_prompt
        
    def get_response(self, prompt):
        """
        Get a response from Claude
        
        Args:
            prompt (str): The user's prompt
            
        Returns:
            str: The model's response
        """
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=1.0,
                system=self.system_prompt if self.system_prompt else "",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error getting response from Claude: {str(e)}" 