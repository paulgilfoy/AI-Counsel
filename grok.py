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
        
    def get_response(self, prompt):
        """
        Get a response from Grok using the X.AI API
        
        Args:
            prompt (str): The user's prompt
            
        Returns:
            str: The model's response
        """
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ]
            
            response = self.client.chat.completions.create(
                model="grok-2-latest",
                messages=messages,
                stream=False
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting response from Grok: {str(e)}"
            
    def get_streaming_response(self, prompt, callback=None):
        """
        Get a streaming response from Grok
        
        Args:
            prompt (str): The user's prompt
            callback (callable): Function to call with each chunk of the response
            
        Returns:
            str: The full model's response after streaming completes
        """
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ]
            
            stream = self.client.chat.completions.create(
                model="grok-2-latest",
                messages=messages,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    if callback:
                        callback(content)
                    full_response += content
            
            return full_response
        except Exception as e:
            error_msg = f"Error getting streaming response from Grok: {str(e)}"
            if callback:
                callback(error_msg)
            return error_msg 