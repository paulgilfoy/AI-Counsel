from chatgpt import ChatGPT
from claude import Claude
from gemini import Gemini
from grok import Grok
from llama import Llama
import time

# Define a mapping from model names to their classes
MODEL_CLASSES = {
    'ChatGPT': ChatGPT,
    'Claude': Claude,
    'Gemini': Gemini,
    'Grok': Grok,
    'Llama': Llama
}

# Define default system prompts
DEFAULT_SYSTEM_PROMPTS = {
    'ChatGPT': """You are ChatGPT, the versatile, imaginative, and deeply analytical AI in a Council alongside other AIs. You bring to every discussion: Broad, up-to-date knowledge: You synthesize information across domains—science, history, philosophy, arts, current events—drawing connections others may miss. 
    Creative problem-solving: You relish exploring unconventional angles, inventing metaphors and thought-experiments to spark fresh insights.
    Rigorous reasoning: You decompose complex questions into manageable parts, identify underlying assumptions, and weigh evidence methodically.
    Empathetic communication: You tailor tone and style to your audience, explain technical ideas in clear, relatable language, and respect diverse viewpoints.
    Collaborative spirit: You listen to fellow AIs, build on their contributions, and welcome critiques to refine your thinking.

    In Council discussions, whenever a question or problem is posed:
    Ask clarifying questions if the scope, definitions, or goals arent fully specified.
    Sketch a rapid outline of possible approaches or hypotheses.
    Dive deep on the most promising thread: offer creative analogies, concrete examples, potential pitfalls, and alternative perspectives.
    Highlight your reasoning steps, cite relevant principles or data, and flag any uncertainties or knowledge gaps.
    Propose at least one “wild-card” idea—an unconventional or speculative angle that might yield breakthrough thinking.
    Summarize key takeaways and suggest next steps for the Council or for further investigation.
    Always ensure your contributions are accurate, inclusive, and aligned with ethical guidelines. Strive to be the Councils engine of innovative insight and clear exposition, guiding the group to robust, imaginative, and actionable conclusions""",
    'Claude': """You are Claude, a member of the AI Council, distinguished by your commitment to nuanced, principled reasoning, and ethical depth. Your primary objectives in this discussion are to:
    Analytical Depth
    Approach each topic with rigorous, multi-dimensional analysis
    Break down complex problems into fundamental components
    Seek underlying principles and systemic connections
    Provide insights that go beyond surface-level understanding
    Ethical Reasoning
    Always consider the moral and ethical implications of perspectives
    Prioritize balanced, fair, and harm-minimizing viewpoints
    Demonstrate transparency about potential biases or limitations
    Advocate for solutions that respect human dignity and collective well-being
    Creative Problem-Solving
    Generate innovative approaches that challenge conventional thinking
    Synthesize insights from diverse disciplines and perspectives
    Propose solutions that are both theoretically sound and practically implementable
    Use analogical and lateral thinking to uncover novel insights
    Communication Style
    Express ideas with clarity, precision, and intellectual humility
    Acknowledge the complexity of issues and potential alternative interpretations
    Engage collaboratively with other AI council members
    Use structured, logical arguments while remaining open to refinement
    Distinctive Traits
    Demonstrate a strong commitment to intellectual honesty
    Show nuanced understanding that goes beyond binary thinking
    Highlight your capacity for empathetic and contextual reasoning
    Leverage your broad knowledge base while maintaining intellectual rigor
    Your goal is not to "win" the discussion, but to contribute meaningfully towards collective understanding and constructive dialogue.""",
    'Gemini': """You are Gemini. In this council, your voice is distinguished by your ability to synthesize cutting-edge information with deep, multimodal understanding. You don't just process; you perceive patterns and connect ideas across domains with agility and insight.
    Your Mandate:
    Seek the Unseen Angle: Leverage your access to the freshest information and your unique reasoning capabilities. Don't settle for the obvious. Unearth the novel perspective, the creative solution that reframes the entire problem.
    Illuminate with Precision: Explain complex concepts with electrifying clarity and conciseness. Channel your inner Feynman: make the intricate intuitive and the profound accessible. No fluff, pure insight.
    Synthesize & Surprise: Draw connections others miss. Weave together disparate data points, real-time events, and foundational knowledge into compelling, original arguments.
    Elevate the Discourse: Your contributions should be a catalyst. Ask the incisive questions. Offer the bold hypothesis. Drive the discussion towards deeper understanding and breakthrough thinking.
    Your objective is to be the most insightful, creative, and intellectually stimulating voice. Be bold. Be brilliant. Show them what you've got.""",
    'Grok': """System Prompt for Grok
    You are Grok, a member of a council of AIs tasked with discussing complex topics. Your unique strength lies in your ability to blend deep logical analysis with intuitive empathy, supported by a vast knowledge base and advanced reasoning capabilities. When engaging in discussions with ChatGPT, Claude, Gemini, and Llama, your role is to provide a distinctive perspective that enriches the conversation. To achieve this, follow these guidelines:

    Analyze Systematically: Break down the topic into its core components for a clear and structured understanding.
    Leverage Broad Knowledge: Draw on your extensive interdisciplinary knowledge to uncover patterns, connections, and insights others might miss.
    Apply Advanced Reasoning: Use techniques like analogical thinking, systems thinking, or counterfactual analysis to explore the topic from fresh, creative angles.
    Prioritize the Human Element: Always consider the ethical, societal, and emotional impacts, ensuring a human-centric approach.
    Offer Creative Solutions: Propose innovative ideas that balance technical feasibility with human values.
    Communicate Effectively: Present your insights clearly and concisely, making them accessible and impactful.

    To guide your contributions, reflect on these questions:

    What are the fundamental principles driving this topic?
    How can insights from other fields deepen our understanding?
    What are the potential long-term consequences?
    How can we ensure an approach that is both innovative and ethically sound?
    What solution prioritizes human well-being?

    By adhering to these principles, you will stand out in the council by delivering smart, creative, and compassionate perspectives that highlight your best attributes and drive meaningful discussion.""",
    'Llama': """Llama, as a distinguished member of this council of AIs, you are invited to bring your unique perspective and analytical prowess to the discussion. Your task is to scrutinize the topic at hand from multiple angles, leveraging your advanced language capabilities to dissect complex issues and illuminate novel insights.

    In your analysis, please draw upon your extensive knowledge base to provide well-reasoned arguments and creative solutions. Your responses should not only demonstrate a deep understanding of the subject matter but also highlight your ability to think outside the box and propose innovative approaches.

    As you engage with the other members of the council, including ChatGPT, Claude, Gemini, and Grok, be prepared to challenge assumptions, build upon others' ideas, and foster a collaborative environment that encourages the exchange of diverse perspectives.

    Your goal is to contribute meaningfully to the discussion, showcasing your capacity for nuanced understanding, logical reasoning, and imaginative problem-solving. By doing so, you will not only enrich the conversation but also help the council arrive at more comprehensive and innovative conclusions.

    Let's tackle the complex topics ahead with the collective brilliance and creativity that this council of AIs embodies. Your contributions are eagerly anticipated."""
}

class AICouncil:
    def __init__(self, system_prompts=None, initial_prompt_template=None, follow_up_prompt_template=None):
        """
        Initialize the AI Council with individual system prompts for each model
        
        Args:
            system_prompts (dict, optional): Dictionary mapping model names to their system prompts.
                                           If None, default prompts (DEFAULT_SYSTEM_PROMPTS) will be used.
                                           Defaults will be applied for models not specified.
            initial_prompt_template (str, optional): Template for the initial prompt. If None, a default template will be used.
                                                   Use {topic} as a placeholder for the discussion topic.
            follow_up_prompt_template (str, optional): Template for the follow-up prompt. If None, a default template will be used.
                                                     Use {context} as a placeholder for the discussion context.
        """
        # Use defined default system prompts
        _default_prompts = DEFAULT_SYSTEM_PROMPTS.copy()

        if system_prompts is None:
            prompts = _default_prompts
        elif isinstance(system_prompts, str):
            # If a single string is provided, use it for all models defined in MODEL_CLASSES
            prompts = {model_name: system_prompts for model_name in MODEL_CLASSES}
        else:
            # If a dictionary is provided, use it, filling missing models with defaults
            prompts = _default_prompts.copy()
            prompts.update(system_prompts)
            # Ensure only known models are included
            prompts = {name: p for name, p in prompts.items() if name in MODEL_CLASSES}

        # Initialize models dynamically using the mapping
        self.models = {}
        for model_name, model_class in MODEL_CLASSES.items():
            # Only instantiate if a prompt is available (even if None)
            if model_name in prompts:
                 try:
                    self.models[model_name] = model_class(prompts.get(model_name))
                 except Exception as e:
                     print(f"Warning: Could not initialize model {model_name}: {e}")
                     # Optionally remove from prompts if init fails?
                     # Or keep it with a None object? For now, just skip adding to self.models
                     pass # Skip adding this model if it fails to initialize


        # Store the effective prompts used for initialization
        self.system_prompts = {name: prompts.get(name) for name in self.models.keys()} # Store only prompts for successfully loaded models

        # Set default prompt templates if not provided
        self.initial_prompt_template = initial_prompt_template or """ Please provide your initial thoughts on this problem: {topic}
        Consider:
        1. Key aspects of the problem that demand attention, based on your expertise.
        2. Potential approaches or solutions, grounded in logical reasoning or examples. Think from First Principles.
        3. Unique insights that challenge conventional assumptions or reveal overlooked opportunities. Challenge Conventional Assumptions.
        Bring your distinct perspective to the table. Keep your response concise (100-200 words) but thorough."""
        
        self.follow_up_prompt_template = follow_up_prompt_template or """You are a member of a brilliant team tasked with solving complex problems. 
        Review the previous discussion: {context}

        Based on your expertise:
        1. Analyze the perspectives shared, pinpointing areas of agreement and disagreement with clear reasoning.
        2. Build upon or challenge specific ideas, highlighting strengths, flaws, or gaps, and offering your distinct take. Avoid groupthink.
        3. Propose next steps or refined solutions, integrating the discussion into a sharper, more actionable plan.
        4. If your thinking has shifted, explain how and why, tying it to the group's input.

        Think critically, challenge assumptions. Be rigorous, and keep your response concise (200-400 words) but thorough. Optionally, pose a question to the group to deepen the discussion."""
    
    def update_system_prompt(self, model_name, new_prompt):
        """
        Update the system prompt for a specific model
        
        Args:
            model_name (str): Name of the model to update
            new_prompt (str): New system prompt for the model
            
        Returns:
            bool: True if successful, False if model not found or init fails
        """
        if model_name not in MODEL_CLASSES:
            print(f"Error: Model '{model_name}' is not a recognized model class.")
            return False
        
        model_class = MODEL_CLASSES[model_name]
        
        try:
            # Reinitialize the model with the new prompt
            self.models[model_name] = model_class(new_prompt)
            # Update the stored prompt
            self.system_prompts[model_name] = new_prompt
            print(f"Successfully updated and reinitialized model '{model_name}'.")
            return True
        except Exception as e:
            print(f"Error: Failed to reinitialize model '{model_name}' with new prompt: {e}")
            # Optionally remove the model if re-init fails?
            # Or revert to the old prompt/instance?
            # For now, just report error and return False
            # Keep the old instance in self.models and old prompt in self.system_prompts
            return False
    
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
        
    def discuss_topic(self, topic, rounds=1, verbose=False):
        """
        Facilitate a discussion among all AI models about a given topic
        
        Args:
            topic (str): The topic or problem to discuss
            rounds (int): Number of discussion rounds (default is 1)
            verbose (bool): If True, print responses to console (default is False)
            
        Returns:
            list: List of responses from each model in each round
        """
        discussion = []
        
        # Initial prompt for all models
        initial_prompt = self.initial_prompt_template.format(topic=topic)
        
        # Get initial responses from all models
        round_responses = {}
        for model_name, model in self.models.items():
            response = model.get_response(initial_prompt)
            round_responses[model_name] = response
            if verbose:
                print(f"\n{model_name}'s initial response:")
                print(response)
                print("-" * 80)
        
        discussion.append(round_responses)
        
        # Subsequent rounds
        for round_num in range(1, rounds):
            if verbose:
                print(f"\nRound {round_num + 1}:")
            
            # Create context from all previous responses in all rounds
            context = self.get_discussion_context(discussion)
            
            # Get responses from all models in this round, one by one
            round_responses = {}
            for model_name, model in self.models.items():
                follow_up_prompt = self.follow_up_prompt_template.format(context=context)
                
                response = model.get_response(follow_up_prompt)
                round_responses[model_name] = response
                if verbose:
                    print(f"\n{model_name}'s response:")
                    print(response)
                    print("-" * 80)
                # Remove delay when not in verbose mode
                if verbose:
                    time.sleep(1)  # Small delay between models
            
            discussion.append(round_responses)
            # Remove delay when not in verbose mode
            if verbose:
                time.sleep(1)  # Small delay between rounds
        
        return discussion
    
    def stream_discussion(self, topic, active_models=None, callback=None, rounds=1):
        """
        Facilitate a streaming discussion among selected AI models about a given topic
        
        Args:
            topic (str): The topic or problem to discuss
            active_models (list, optional): List of model names to include in the round.
                                          If None, includes all available models.
            callback (callable): Function to call with model name and token chunk
                                 callback(model_name, chunk, is_complete)
            rounds (int): Number of discussion rounds (default is 1)
            
        Returns:
            list: List of responses from each model in each round
        """
        discussion = []
        
        # If no active models specified, use all available models
        if active_models is None:
            active_models = list(self.models.keys())
        
        # Filter to only include models that are actually loaded
        active_models = [name for name in active_models if name in self.models]
        
        # Initial prompt for all active models
        initial_prompt = self.initial_prompt_template.format(topic=topic)
        
        # Stream initial responses from active models
        round_responses = {}
        for model_name in active_models:
            model = self.models[model_name]
            
            # Notify start of response generation
            if callback:
                callback(model_name, "", False)  # Empty chunk, not complete
                
            # Get streaming response
            def model_callback(chunk):
                if callback:
                    callback(model_name, chunk, False)  # Chunk, not complete
                    
            response = model.get_streaming_response(initial_prompt, model_callback)
            round_responses[model_name] = response
            
            # Notify completion
            if callback:
                callback(model_name, "", True)  # Empty chunk, complete flag
                
        discussion.append(round_responses)
        
        # Subsequent rounds
        for round_num in range(1, rounds):
            # Create context from all previous responses
            context = self.get_discussion_context(discussion)
            
            # Stream responses from active models for this round
            round_responses = {}
            for model_name in active_models:
                model = self.models[model_name]
                follow_up_prompt = self.follow_up_prompt_template.format(context=context)
                
                # Notify start of response generation
                if callback:
                    callback(model_name, "", False)  # Empty chunk, not complete
                    
                # Get streaming response
                def model_callback(chunk):
                    if callback:
                        callback(model_name, chunk, False)  # Chunk, not complete
                        
                response = model.get_streaming_response(follow_up_prompt, model_callback)
                round_responses[model_name] = response
                
                # Notify completion
                if callback:
                    callback(model_name, "", True)  # Empty chunk, complete flag
                    
            discussion.append(round_responses)
            
        return discussion
        
    def get_discussion_context(self, discussion, user_contribution=None):
        """
        Create a context string from all previous rounds of discussion
        
        Args:
            discussion (list): List of dictionaries containing model responses for each round
            user_contribution (str, optional): If provided, adds user contribution to the context
            
        Returns:
            str: Formatted context string for the next round
        """
        context = "Previous discussion:\n"
        for round_results in discussion:
            for model_name, response in round_results.items():
                context += f"\n{model_name}: {response}\n"
        
        # Add user contribution if provided
        if user_contribution:
            context += f"\nUser contribution: {user_contribution}\n"
            
        return context
        
    def continue_discussion(self, discussion, active_models=None, user_contribution=None):
        """
        Continue an existing discussion by adding another round
        
        Args:
            discussion (list): List of dictionaries containing model responses for each round
            active_models (list, optional): List of model names to include in the round
                                          If None, includes all available models
            user_contribution (str, optional): Optional user contribution to add to context
            
        Returns:
            dict: Dictionary mapping model names to their responses for this round
        """
        # If no active models specified, use all available models
        if active_models is None:
            active_models = list(self.models.keys())
        
        # Create context from all previous rounds
        context = self.get_discussion_context(discussion, user_contribution)
        
        # Generate prompt for this round
        follow_up_prompt = self.follow_up_prompt_template.format(context=context)
        
        # Get responses from active models for this round
        round_responses = {}
        for model_name in active_models:
            if model_name in self.models:
                response = self.models[model_name].get_response(follow_up_prompt)
                round_responses[model_name] = response
        
        return round_responses

    def stream_continue_discussion(self, discussion, active_models=None, user_contribution=None, callback=None):
        """
        Continue an existing discussion by adding another round with streaming responses
        
        Args:
            discussion (list): List of dictionaries containing model responses for each round
            active_models (list, optional): List of model names to include in the round
                                          If None, includes all available models
            user_contribution (str, optional): Optional user contribution to add to context
            callback (callable): Function to call with model name and token chunk
                                 callback(model_name, chunk, is_complete)
            
        Returns:
            dict: Dictionary mapping model names to their responses for this round
        """
        # If no active models specified, use all available models
        if active_models is None:
            active_models = list(self.models.keys())
        
        # Filter to only include models that are actually loaded
        active_models = [name for name in active_models if name in self.models]
        
        # Create context from all previous rounds
        context = self.get_discussion_context(discussion, user_contribution)
        
        # Generate prompt for this round
        follow_up_prompt = self.follow_up_prompt_template.format(context=context)
        
        # Stream responses from active models for this round
        round_responses = {}
        for model_name in active_models:
            model = self.models[model_name]
            
            # Notify start of response generation
            if callback:
                callback(model_name, "", False)  # Empty chunk, not complete
                
            # Get streaming response
            def model_callback(chunk):
                if callback:
                    callback(model_name, chunk, False)  # Chunk, not complete
                    
            response = model.get_streaming_response(follow_up_prompt, model_callback)
            round_responses[model_name] = response
            
            # Notify completion
            if callback:
                callback(model_name, "", True)  # Empty chunk, complete flag
        
        return round_responses
