from chatgpt import ChatGPT
from claude import Claude
from gemini import Gemini
from grok import Grok
from llama import Llama
import time

class AICouncil:
    def __init__(self, system_prompts=None):
        """
        Initialize the AI Council with individual system prompts for each model
        
        Args:
            system_prompts (dict, optional): Dictionary mapping model names to their system prompts.
                                           If None, no system prompts will be used.
                                           If a string is provided instead of a dict, it will be used for all models.
        """
        # Default system prompts (empty)
        default_prompts = {
            'ChatGPT': None,
            'Claude': None,
            'Gemini': None,
            'Grok': None,
            'Llama': None
        }
        
        # Handle different input types
        if system_prompts is None:
            prompts = default_prompts
        elif isinstance(system_prompts, str):
            # If a single string is provided, use it for all models
            prompts = {model: system_prompts for model in default_prompts}
        else:
            # If a dictionary is provided, update the default prompts
            prompts = default_prompts.copy()
            prompts.update(system_prompts)
        
        # Initialize models with their respective prompts
        self.models = {
            'ChatGPT': ChatGPT(prompts['ChatGPT']),
            'Claude': Claude(prompts['Claude']),
            'Gemini': Gemini(prompts['Gemini']),
            'Grok': Grok(prompts['Grok']),
            'Llama': Llama(prompts['Llama'])
        }
        
        # Store the prompts for potential updates
        self.system_prompts = prompts
    
    def update_system_prompt(self, model_name, new_prompt):
        """
        Update the system prompt for a specific model
        
        Args:
            model_name (str): Name of the model to update
            new_prompt (str): New system prompt for the model
            
        Returns:
            bool: True if successful, False if model not found
        """
        if model_name not in self.models:
            return False
        
        # Update the stored prompt
        self.system_prompts[model_name] = new_prompt
        
        # Reinitialize the model with the new prompt
        if model_name == 'ChatGPT':
            self.models[model_name] = ChatGPT(new_prompt)
        elif model_name == 'Claude':
            self.models[model_name] = Claude(new_prompt)
        elif model_name == 'Gemini':
            self.models[model_name] = Gemini(new_prompt)
        elif model_name == 'Grok':
            self.models[model_name] = Grok(new_prompt)
        elif model_name == 'Llama':
            self.models[model_name] = Llama(new_prompt)
        
        return True
    
    def update_all_system_prompts(self, new_prompts):
        """
        Update system prompts for multiple models at once
        
        Args:
            new_prompts (dict): Dictionary mapping model names to their new system prompts
        """
        for model_name, prompt in new_prompts.items():
            self.update_system_prompt(model_name, prompt)
        
    def discuss_topic(self, topic, rounds=3):
        """
        Facilitate a discussion among all AI models about a given topic
        
        Args:
            topic (str): The topic or problem to discuss
            rounds (int): Number of discussion rounds
            
        Returns:
            list: List of responses from each model in each round
        """
        discussion = []
        
        # Initial prompt for all models
        initial_prompt = f"""Please provide your initial thoughts on the following topic or problem:
{topic}

Consider:
1. Key aspects of the problem
2. Potential approaches or solutions
3. Any unique insights you can bring to the discussion

Please be concise but thorough in your response."""
        
        # Get initial responses
        round_responses = {}
        for model_name, model in self.models.items():
            response = model.get_response(initial_prompt)
            round_responses[model_name] = response
            print(f"\n{model_name}'s initial response:")
            print(response)
            print("-" * 80)
        
        discussion.append(round_responses)
        
        # Subsequent rounds
        for round_num in range(1, rounds):
            print(f"\nRound {round_num + 1}:")
            
            # Create context from previous responses
            context = "Previous responses:\n"
            for model_name, response in round_responses.items():
                context += f"\n{model_name}: {response}\n"
            
            follow_up_prompt = f"""Based on the previous discussion:

{context}

Please:
1. Analyze the perspectives shared by other models
2. Identify areas of agreement and disagreement
3. Build upon or challenge previous points
4. Propose next steps or refined solutions

Your response:"""
            
            round_responses = {}
            for model_name, model in self.models.items():
                response = model.get_response(follow_up_prompt)
                round_responses[model_name] = response
                print(f"\n{model_name}'s response:")
                print(response)
                print("-" * 80)
            
            discussion.append(round_responses)
            time.sleep(1)  # Small delay between rounds
        
        return discussion

def main():
    # Example usage with individual system prompts
    topic = """How can we improve the efficiency of renewable energy storage systems?
Consider both technological and economic aspects."""
    
    # Define individual system prompts for each model
    system_prompts = {
        'ChatGPT': """You are participating in a collaborative discussion with other AI models.
Your goal is to contribute unique insights while building upon others' ideas.
Be constructive, specific, and focus on practical solutions.""",
        
        'Claude': """You are participating in a collaborative discussion with other AI models.
Your goal is to contribute unique insights while building upon others' ideas.
Be constructive, specific, and focus on practical solutions.
As Claude, you have particular expertise in ethical considerations.""",
        
        'Gemini': """You are participating in a collaborative discussion with other AI models.
Your goal is to contribute unique insights while building upon others' ideas.
Be constructive, specific, and focus on practical solutions.
As Gemini, you have particular expertise in multimodal analysis.""",
        
        'Grok': """You are participating in a collaborative discussion with other AI models.
Your goal is to contribute unique insights while building upon others' ideas.
Be constructive, specific, and focus on practical solutions.
As Grok, you have particular expertise in humor and unconventional approaches.""",
        
        'Llama': """You are participating in a collaborative discussion with other AI models.
Your goal is to contribute unique insights while building upon others' ideas.
Be constructive, specific, and focus on practical solutions.
As Llama, you have particular expertise in open-source approaches."""
    }
    
    # Initialize with individual prompts
    council = AICouncil(system_prompts)
    
    # Example of updating a single model's prompt
    council.update_system_prompt('ChatGPT', "You are now a more focused expert on renewable energy.")
    
    # Run the discussion
    discussion = council.discuss_topic(topic, rounds=3)
    
if __name__ == "__main__":
    main() 