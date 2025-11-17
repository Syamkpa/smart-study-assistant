"""
Coordinator Agent - Routes requests to appropriate specialist agents.

This demonstrates LLM-powered dynamic routing in a multi-agent system.
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)


class CoordinatorAgent:
    """
    Coordinator Agent that analyzes user requests and routes them to
    the appropriate specialist agent.
    
    This is an LLM-powered agent that uses reasoning to determine
    which specialist agent should handle each request.
    """
    
    def __init__(self, model):
        """
        Initialize the Coordinator Agent.
        
        Args:
            model: Gemini model instance for LLM-powered reasoning
        """
        self.model = model
        logger.info("Coordinator Agent initialized")
    
    def route_request(self, user_input: str, session_memory: Dict, agents: Dict) -> Dict:
        """
        Analyze the user request and route it to the appropriate specialist agent.
        
        This demonstrates:
        - LLM-powered decision making
        - Dynamic workflow routing
        - Multi-agent coordination
        
        Args:
            user_input: The user's request
            session_memory: Session memory for context
            agents: Dictionary of available specialist agents
            
        Returns:
            Dictionary containing the response and metadata
        """
        logger.info(f"Routing request: {user_input}")
        
        # Create a prompt for the LLM to classify the request
        prompt = f"""You are a coordinator for a study assistant system. 
Analyze the following user request and determine which specialist agent should handle it.

Available agents:
1. study_planner - Creates study schedules, plans learning paths, organizes study time
2. question_answerer - Answers questions about topics, explains concepts, provides information
3. progress_tracker - Tracks study progress, records completed tasks, analyzes performance

User request: "{user_input}"

Respond with ONLY ONE of these exact words: study_planner, question_answerer, or progress_tracker
"""
        
        try:
            # Use LLM to determine the appropriate agent
            response = self.model.generate_content(prompt)
            agent_type = response.text.strip().lower()
            
            # Clean up the response (sometimes LLM adds extra text)
            if 'study_planner' in agent_type or 'study' in agent_type and 'plan' in agent_type:
                agent_type = 'study_planner'
            elif 'question' in agent_type or 'answer' in agent_type:
                agent_type = 'question_answerer'
            elif 'progress' in agent_type or 'track' in agent_type:
                agent_type = 'progress_tracker'
            
            # Validate the response
            valid_agents = ['study_planner', 'question_answerer', 'progress_tracker']
            if agent_type not in valid_agents:
                # Default to question answerer if unclear
                logger.warning(f"Invalid agent type returned: {agent_type}, defaulting to question_answerer")
                agent_type = 'question_answerer'
            
            logger.info(f"Request routed to: {agent_type}")
            
            # Route to the appropriate agent and get the response
            if agent_type == 'study_planner':
                return agents['study_planner'].create_plan(user_input, session_memory)
            elif agent_type == 'question_answerer':
                return agents['question_answerer'].answer_question(user_input, session_memory)
            elif agent_type == 'progress_tracker':
                return agents['progress_tracker'].track_progress(user_input, session_memory)
            else:
                # Fallback to question answerer
                return agents['question_answerer'].answer_question(user_input, session_memory)
            
        except Exception as e:
            logger.error(f"Error in routing: {e}")
            # Return error response
            return {
                'status': 'error',
                'agent_used': 'coordinator',
                'message': f'Unable to route request: {str(e)}'
            }
