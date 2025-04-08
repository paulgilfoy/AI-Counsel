import os
import google.generativeai as genai
from dotenv import load_dotenv

class Gemini:
    def __init__(self, system_prompt=None):
        load_dotenv()
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.system_prompt = system_prompt
        
    def get_response(self, prompt):
        """
        Get a response from Gemini
        
        Args:
            prompt (str): The user's prompt
            
        Returns:
            str: The model's response
        """
        try:
            full_prompt = prompt
            if self.system_prompt:
                full_prompt = f"{self.system_prompt}\n\n{prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=1.0,
                    max_output_tokens=1000,
                )
            )
            return response.text
        except Exception as e:
            return f"Error getting response from Gemini: {str(e)}" 