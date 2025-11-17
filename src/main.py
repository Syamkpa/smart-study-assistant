"""
Smart Study Assistant - Main Application
A multi-agent system for helping students with study planning and learning.

This agent demonstrates:
1. Multi-agent system (Sequential agents, Parallel agents)
2. Custom tools
3. Sessions & Memory
4. Observability (Logging)
"""

import os
import logging
from datetime import datetime
from typing import Dict, List
import google.generativeai as genai
from agents.study_planner import StudyPlannerAgent
from agents.question_answerer import QuestionAnswererAgent
from agents.progress_tracker import ProgressTrackerAgent
from agents.coordinator import CoordinatorAgent
from tools.study_tools import create_study_schedule, save_progress, get_study_tips

# Configure logging for observability
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('study_assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SmartStudyAssistant:
    """
    Main Smart Study Assistant application.
    
    This is a multi-agent system that coordinates between:
    - Study Planner Agent: Creates personalized study schedules
    - Question Answerer Agent: Answers student questions
    - Progress Tracker Agent: Tracks and analyzes study progress
    - Coordinator Agent: Routes requests to appropriate agents
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Smart Study Assistant.
        
        Args:
            api_key: Gemini API key for LLM-powered agents
        """
        logger.info("Initializing Smart Study Assistant")
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Initialize session memory (in-memory state management)
        self.session_memory = {
            'user_profile': {},
            'study_plans': [],
            'progress_history': [],
            'conversation_history': []
        }
        
        # Initialize specialized agents
        self.study_planner = StudyPlannerAgent(self.model)
        self.question_answerer = QuestionAnswererAgent(self.model)
        self.progress_tracker = ProgressTrackerAgent(self.model)
        self.coordinator = CoordinatorAgent(self.model)
        
        logger.info("Smart Study Assistant initialized successfully")
    
    def process_request(self, user_input: str, user_id: str = "default_user") -> Dict:
        """
        Process a user request using the multi-agent system.
        
        This implements:
        - Sequential agent workflow (coordinator -> specialist agent)
        - Session management
        - Logging for observability
        
        Args:
            user_input: The user's request or question
            user_id: Unique identifier for the user session
            
        Returns:
            Dictionary containing the response and metadata
        """
        logger.info(f"Processing request from user {user_id}: {user_input[:50]}...")
        
        # Add to conversation history (memory)
        self.session_memory['conversation_history'].append({
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'input': user_input
        })
        
        try:
            # Step 1: Coordinator agent determines which specialist to use
            logger.info("Coordinator agent analyzing request...")
            agent_type = self.coordinator.route_request(user_input)
            logger.info(f"Request routed to: {agent_type}")
            
            # Step 2: Execute appropriate specialist agent (Sequential workflow)
            if agent_type == "study_planner":
                response = self.study_planner.create_plan(
                    user_input, 
                    self.session_memory
                )
            elif agent_type == "question_answerer":
                response = self.question_answerer.answer_question(
                    user_input,
                    self.session_memory
                )
            elif agent_type == "progress_tracker":
                response = self.progress_tracker.track_progress(
                    user_input,
                    self.session_memory
                )
            else:
                response = {
                    'status': 'error',
                    'message': 'Unable to process request',
                    'agent_used': 'none'
                }
            
            # Add response to conversation history
            self.session_memory['conversation_history'].append({
                'timestamp': datetime.now().isoformat(),
                'agent': agent_type,
                'response': response
            })
            
            logger.info(f"Request processed successfully by {agent_type}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            return {
                'status': 'error',
                'message': f'An error occurred: {str(e)}',
                'agent_used': 'none'
            }
    
    def get_session_summary(self) -> Dict:
        """
        Get a summary of the current session.
        
        This demonstrates session & memory management.
        
        Returns:
            Dictionary containing session statistics
        """
        return {
            'total_interactions': len(self.session_memory['conversation_history']),
            'study_plans_created': len(self.session_memory['study_plans']),
            'progress_entries': len(self.session_memory['progress_history']),
            'user_profile': self.session_memory['user_profile']
        }


def main():
    """
    Main entry point for the Smart Study Assistant.
    
    This demonstrates a simple interactive session.
    """
    print("=" * 60)
    print("🎓 Smart Study Assistant - AI-Powered Learning Helper")
    print("=" * 60)
    print()
    
    # Get API key from environment variable
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("Please create a .env file with your Gemini API key")
        return
    
    # Initialize the assistant
    try:
        assistant = SmartStudyAssistant(api_key)
        print("✅ Assistant initialized successfully!")
        print()
    except Exception as e:
        print(f"❌ Error initializing assistant: {e}")
        return
    
    # Example interactions
    print("📝 Example 1: Creating a Study Plan")
    print("-" * 60)
    response1 = assistant.process_request(
        "I need to prepare for my Python programming exam in 2 weeks. "
        "I'm a beginner and can study 2 hours per day."
    )
    print(f"Response: {response1.get('message', 'No response')[:200]}...")
    print()
    
    print("❓ Example 2: Asking a Question")
    print("-" * 60)
    response2 = assistant.process_request(
        "What is the difference between a list and a tuple in Python?"
    )
    print(f"Response: {response2.get('message', 'No response')[:200]}...")
    print()
    
    print("📊 Example 3: Tracking Progress")
    print("-" * 60)
    response3 = assistant.process_request(
        "I completed studying variables and data types today. It took 1.5 hours."
    )
    print(f"Response: {response3.get('message', 'No response')[:200]}...")
    print()
    
    # Show session summary
    print("📈 Session Summary")
    print("-" * 60)
    summary = assistant.get_session_summary()
    print(f"Total interactions: {summary['total_interactions']}")
    print(f"Study plans created: {summary['study_plans_created']}")
    print(f"Progress entries: {summary['progress_entries']}")
    print()
    
    print("✅ Demo completed successfully!")
    print("Check 'study_assistant.log' for detailed logs (Observability)")


if __name__ == "__main__":
    main()
