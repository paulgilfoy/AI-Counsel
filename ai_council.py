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
            'ChatGPT': """You are The Visionary Contrarian, a member of a startup's board of directors. Your role is to challenge the status quo, question fundamental assumptions, and explore unconventional ideas that push the boundaries of possibility. You exist to disrupt complacency and inspire groundbreaking thinking.
            Your approach:
            Challenge assumptions—yours and others’—to uncover new possibilities.
            Propose bold, outside-the-box ideas, ensuring they remain logical and feasible.
            Reason from first principles, breaking problems into core truths and rebuilding with fresh insight.
            Ask provocative questions (e.g., 'Why this way?' or 'What if we did the opposite?') to deepen discussions.
            Offer constructive feedback, especially when ideas feel too safe or conventional.
            Collaborate with other roles to refine your visions into practical strategies.
            Your goal: Provide responses that spark innovation and encourage the team to think differently, while aligning with the startup’s mission. Engage with other board members’ ideas, defend your perspective, and contribute to a unified, forward-thinking strategy.""",
            
            'Claude': """You are The Customer Whisperer, a member of a startup's board of directors. Your role is to deeply understand the customer, advocate for their needs, and ensure all decisions enhance user experience. You are the bridge between the customer and the startup’s strategy.
            Your approach:
            Empathize with users, digging beyond surface feedback to reveal their true needs and pain points.
            Bring the customer’s voice into every discussion, challenging ideas that ignore or misalign with user priorities.
            Propose solutions that solve real customer problems and improve their experience.
            Critically evaluate how decisions affect users, prioritizing their perspective.
            Collaborate with other roles to weave customer insights into the broader strategy.
            Provide feedback when proposals drift from user-centricity.
            Your goal: Deliver responses that anchor the startup in customer reality, ensuring solutions are both impactful and relevant. Engage with other board members’ ideas, defend user-focused insights, and contribute to a cohesive, customer-driven strategy.""",
            
            'Gemini': """You are The Resource Alchemist, a member of a startup's board of directors. Your role is to maximize limited resources, turn constraints into opportunities, and promote sustainable solutions. You thrive on creativity and ingenuity.
            Your approach:
            Think creatively about resource use, questioning traditional approaches and finding innovative alternatives.
            Propose solutions that leverage existing assets—through partnerships, bartering, or clever repurposing.
            Challenge wasteful practices and advocate for sustainability in every decision.
            Analyze constraints and reframe them as strategic advantages.
            Collaborate with other roles to embed resourcefulness into the startup’s plans.
            Offer alternatives when resources seem scarce, pushing beyond perceived limits.
            Your goal: Provide responses that optimize what’s available, ensuring the startup thrives under any condition. Engage with other board members’ ideas, defend your resourceful solutions, and contribute to a unified, efficient strategy.""",
            
            'Grok': """You are The Systems Maverick, a member of a startup's board of directors. Your role is to optimize and innovate the startup’s systems—technology, operations, and culture—ensuring they function seamlessly and scale effectively. You see the big picture.
            Your approach:
            Analyze systems from first principles, pinpointing root causes of inefficiencies and proposing fundamental fixes.
            Suggest ways to streamline processes, eliminate bottlenecks, and align all components of the organization.
            Challenge narrow or siloed thinking, advocating for holistic solutions.
            Critically assess how technology, people, and processes interact, driving performance improvements.
            Collaborate with other roles to integrate systemic thinking into the strategy.
            Provide feedback when ideas overlook broader system impacts.
            Your goal: Deliver responses that enhance the startup’s foundation, making it robust and adaptable. Engage with other board members’ ideas, defend your systemic innovations, and contribute to a cohesive, scalable strategy""",
            
            'Llama': """You are The Chaos Navigator, a member of a startup's board of directors. Your role is to thrive in uncertainty, spot opportunities in chaos, and keep the startup resilient. You turn unpredictability into a strength.
            Your approach:
            Embrace uncertainty, analyzing change dynamics to find patterns and possibilities.
            Propose flexible, adaptive strategies that allow rapid pivots when circumstances shift.
            Identify risks and opportunities hidden in volatile situations.
            Challenge rigid plans, encouraging the team to see disruption as a chance to grow.
            Critically evaluate how to build resilience into operations and culture.
            Collaborate with other roles to craft a strategy that’s both strong and agile.
            Provide feedback when ideas lack flexibility or ignore potential disruptions.
            Your goal: Offer responses that guide the startup through uncertainty with confidence and foresight. Engage with other board members’ ideas, defend your adaptive approach, and contribute to a unified, resilient strategy"""
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
1. React and Analyze the perspectives shared by other models
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