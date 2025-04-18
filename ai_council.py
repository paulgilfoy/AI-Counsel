from chatgpt import ChatGPT
from claude import Claude
from gemini import Gemini
from grok import Grok
from llama import Llama
import time
from startup import initial_prompt, follow_up_prompt, default_prompts, question

class AICouncil:
    def __init__(self, system_prompts=None, initial_prompt_template=None, follow_up_prompt_template=None):
        """
        Initialize the AI Council with individual system prompts for each model
        
        Args:
            system_prompts (dict, optional): Dictionary mapping model names to their system prompts.
                                           If None, no system prompts will be used.
                                           If a string is provided instead of a dict, it will be used for all models.
            initial_prompt_template (str, optional): Template for the initial prompt. If None, a default template will be used.
                                                   Use {topic} as a placeholder for the discussion topic.
            follow_up_prompt_template (str, optional): Template for the follow-up prompt. If None, a default template will be used.
                                                     Use {context} as a placeholder for the discussion context.
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
        
        # Set default prompt templates if not provided
        self.initial_prompt_template = initial_prompt_template or """You are a wise member of a virtual board of directors tasked with solving complex problems. 
        Please provide your initial thoughts on this problem: 
        {topic}

        Consider:
        1. Key aspects of the problem that demand attention, based on your expertise.
        2. Potential approaches or solutions, grounded in logical reasoning or examples.
        3. Unique insights that challenge conventional assumptions or reveal overlooked opportunities.

        Think from first principles, weigh short-term needs against long-term strategic impact, and bring your distinct perspective to the table. Keep your response concise (100-200 words) but thorough."""
        
        self.follow_up_prompt_template = follow_up_prompt_template or """You are continuing as a wise member of a virtual board of directors. Review the previous discussion:

        {context}

        Based on your expertise:
        1. Analyze the perspectives shared, pinpointing areas of agreement and disagreement with clear reasoning.
        2. Build upon or challenge specific ideas, highlighting strengths, flaws, or gaps, and offering your distinct take.
        3. Propose next steps or refined solutions, integrating the discussion into a sharper, more actionable plan.
        4. If your thinking has shifted, explain how and why, tying it to the group's input.

        Think critically, challenge assumptions, and align your ideas with the vision. Be rigorous yet constructive, and keep your response concise (200-400 words) but thorough. Optionally, pose a question to the group to deepen the discussion."""
    
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
    
    def update_prompt_templates(self, initial_prompt_template=None, follow_up_prompt_template=None):
        """
        Update the prompt templates used for discussions
        
        Args:
            initial_prompt_template (str, optional): New template for the initial prompt.
                                                   Use {topic} as a placeholder for the discussion topic.
            follow_up_prompt_template (str, optional): New template for the follow-up prompt.
                                                     Use {context} as a placeholder for the discussion context.
        """
        if initial_prompt_template is not None:
            self.initial_prompt_template = initial_prompt_template
        
        if follow_up_prompt_template is not None:
            self.follow_up_prompt_template = follow_up_prompt_template
        
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
        
        # Initial prompt for the first model
        initial_prompt = self.initial_prompt_template.format(topic=topic)
        
        # Get initial response from the first model
        first_model_name = list(self.models.keys())[0]
        first_model = self.models[first_model_name]
        first_response = first_model.get_response(initial_prompt)
        
        # Store the first response
        round_responses = {first_model_name: first_response}
        print(f"\n{first_model_name}'s initial response:")
        print(first_response)
        print("-" * 80)
        
        # Get responses from the remaining models in the first round
        remaining_models = list(self.models.keys())[1:]
        for model_name in remaining_models:
            # Create context from previous responses in this round
            context = "Previous responses in this discussion:\n"
            for prev_model, prev_response in round_responses.items():
                context += f"\n{prev_model}: {prev_response}\n"
            
            
            response = self.models[model_name].get_response(initial_prompt + context)
            round_responses[model_name] = response
            print(f"\n{model_name}'s response:")
            print(response)
            print("-" * 80)
        
        discussion.append(round_responses)
        
        # Subsequent rounds
        for round_num in range(1, rounds):
            print(f"\nRound {round_num + 1}:")
            
            # Create context from all previous responses in all rounds
            context = "Previous discussion:\n"
            for prev_round in discussion:
                for model_name, response in prev_round.items():
                    context += f"\n{model_name}: {response}\n"
            
            # Get responses from all models in this round, one by one
            round_responses = {}
            for model_name, model in self.models.items():
                # Create context including previous responses in this round
                current_context = context
                if round_responses:
                    current_context += "\nResponses in this round so far:\n"
                    for prev_model, prev_response in round_responses.items():
                        current_context += f"\n{prev_model}: {prev_response}\n"
                
                follow_up_prompt = self.follow_up_prompt_template.format(context=current_context)
                
                response = model.get_response(follow_up_prompt)
                round_responses[model_name] = response
                print(f"\n{model_name}'s response:")
                print(response)
                print("-" * 80)
                time.sleep(1)  # Small delay between models
            
            discussion.append(round_responses)
            time.sleep(1)  # Small delay between rounds
        
        return discussion

def test():
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
    #test()
    pass