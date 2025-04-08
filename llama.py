import os
import replicate
from dotenv import load_dotenv

class Llama:
    def __init__(self, system_prompt=None):
        load_dotenv()
        self.client = replicate.Client(api_token=os.getenv('REPLICATE_API_TOKEN'))
        self.system_prompt = system_prompt
        
    def get_response(self, prompt):
        """
        Get a response from Llama 3
        
        Args:
            prompt (str): The user's prompt
            
        Returns:
            str: The model's response
        """
        try:
            input_params = {
                "prompt": prompt,
                "top_k": 0,
                "top_p": 0.9,
                "max_tokens": 512,
                "min_tokens": 0,
                "temperature": 1.2,
                "length_penalty": 1,
                "stop_sequences": "<|end_of_text|>,<|eot_id|>",
                "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
                "presence_penalty": 1.15,
                "log_performance_metrics": False
            }
            
            # Add system_prompt if it exists
            if self.system_prompt:
                input_params["system_prompt"] = self.system_prompt
            
            output = self.client.run(
                "meta/meta-llama-3-70b-instruct",
                input=input_params
            )
            return "".join(output)
        except Exception as e:
            return f"Error getting response from Llama: {str(e)}" 