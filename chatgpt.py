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
            
    def get_streaming_response(self, prompt, callback=None):
        """
        Get a streaming response from ChatGPT
        
        Args:
            prompt (str): The user's prompt
            callback (callable): Function to call with each chunk of the response
            
        Returns:
            str: The full model's response after streaming completes
        """
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            full_response = ""
            stream = self.client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=messages,
                temperature=1.0,
                max_tokens=1000,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    if callback:
                        callback(content)
                    full_response += content
                    
            return full_response
        except Exception as e:
            error_msg = f"Error getting streaming response from ChatGPT: {str(e)}"
            if callback:
                callback(error_msg)
            return error_msg 