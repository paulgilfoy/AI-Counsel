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
                model="claude-3-5-sonnet-20241022",
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
            
    def get_streaming_response(self, prompt, callback=None):
        """
        Get a streaming response from Claude
        
        Args:
            prompt (str): The user's prompt
            callback (callable): Function to call with each chunk of the response
            
        Returns:
            str: The full model's response after streaming completes
        """
        try:
            full_response = ""
            with self.client.messages.stream(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=1.0,
                system=self.system_prompt if self.system_prompt else "",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            ) as stream:
                for text in stream.text_stream:
                    if callback:
                        callback(text)
                    full_response += text
                    
            return full_response
        except Exception as e:
            error_msg = f"Error getting streaming response from Claude: {str(e)}"
            if callback:
                callback(error_msg)
            return error_msg 