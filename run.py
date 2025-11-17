"""
Startup script for Smart Study Assistant.
This fixes Python path issues.
"""

import sys
import os

# Add the current directory to Python's module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("=" * 70)
print("🎓 SMART STUDY ASSISTANT - AI-Powered Learning Helper")
print("=" * 70)
print()

# Now import and run the main application
try:
    from dotenv import load_dotenv
    import google.generativeai as genai
    from agents.coordinator import CoordinatorAgent
    from agents.study_planner import StudyPlannerAgent
    from agents.question_answerer import QuestionAnswererAgent
    from agents.progress_tracker import ProgressTrackerAgent
    import logging
    from datetime import datetime
    
    # Load environment variables
    load_dotenv()
    
    # Configure logging
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
        """Main application class for the Smart Study Assistant."""
        
        def __init__(self, api_key: str):
            """Initialize the Smart Study Assistant with all agents."""
            logger.info("Initializing Smart Study Assistant...")
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Initialize session memory
            self.session_memory = {
                'conversation_history': [],
                'study_plans': [],
                'progress_history': [],
                'user_profile': {}
            }
            
            # Initialize agents
            self.coordinator = CoordinatorAgent(self.model)
            self.study_planner = StudyPlannerAgent(self.model)
            self.question_answerer = QuestionAnswererAgent(self.model)
            self.progress_tracker = ProgressTrackerAgent(self.model)
            
            logger.info("Smart Study Assistant initialized successfully!")
        
        def process_request(self, user_input: str) -> dict:
            """Process a user request through the coordinator agent."""
            logger.info(f"Processing request: {user_input}")
            
            # Add to conversation history
            self.session_memory['conversation_history'].append({
                'timestamp': datetime.now().isoformat(),
                'input': user_input
            })
            
            # Route through coordinator
            response = self.coordinator.route_request(
                user_input,
                self.session_memory,
                {
                    'study_planner': self.study_planner,
                    'question_answerer': self.question_answerer,
                    'progress_tracker': self.progress_tracker
                }
            )
            
            return response
        
        def get_session_summary(self) -> dict:
            """Get a summary of the current session."""
            return {
                'total_interactions': len(self.session_memory['conversation_history']),
                'study_plans_created': len(self.session_memory['study_plans']),
                'progress_entries': len(self.session_memory['progress_history'])
            }
    
    def main():
        """Main function to demonstrate the Smart Study Assistant."""
        
        # Get API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("❌ ERROR: GEMINI_API_KEY not set!")
            print()
            print("Please:")
            print("1. Create a file called '.env' in this folder")
            print("2. Add this line: GEMINI_API_KEY=your_actual_key_here")
            print("3. Save the file and run again")
            print()
            return
        
        print("✅ API key found!")
        print()
        
        # Initialize the assistant
        print("Initializing Smart Study Assistant...")
        assistant = SmartStudyAssistant(api_key)
        print("✅ Assistant ready!")
        print()
        
        # Demo 1: Study Planning
        print("=" * 70)
        print("📝 DEMO 1: Creating a Study Plan")
        print("=" * 70)
        print()
        print("User: I need to prepare for my Python exam in 2 weeks. I can study 2 hours daily.")
        print()
        
        response1 = assistant.process_request(
            "I need to prepare for my Python exam in 2 weeks. I can study 2 hours daily."
        )
        
        print(f"Agent: {response1.get('agent_used', 'unknown')}")
        print()
        print(response1.get('message', 'No response'))
        print()
        
        # Demo 2: Question Answering
        print("=" * 70)
        print("❓ DEMO 2: Answering a Question")
        print("=" * 70)
        print()
        print("User: What is the difference between a list and a tuple in Python?")
        print()
        
        response2 = assistant.process_request(
            "What is the difference between a list and a tuple in Python?"
        )
        
        print(f"Agent: {response2.get('agent_used', 'unknown')}")
        print()
        print(response2.get('message', 'No response'))
        print()
        
        # Demo 3: Progress Tracking
        print("=" * 70)
        print("📊 DEMO 3: Tracking Progress")
        print("=" * 70)
        print()
        print("User: I completed studying variables and data types today. It took 1.5 hours.")
        print()
        
        response3 = assistant.process_request(
            "I completed studying variables and data types today. It took 1.5 hours."
        )
        
        print(f"Agent: {response3.get('agent_used', 'unknown')}")
        print()
        print(response3.get('message', 'No response'))
        print()
        
        # Session summary
        print("=" * 70)
        print("📈 Session Summary")
        print("=" * 70)
        summary = assistant.get_session_summary()
        print(f"Total interactions: {summary['total_interactions']}")
        print(f"Study plans created: {summary['study_plans_created']}")
        print(f"Progress entries: {summary['progress_entries']}")
        print()
        
        print("=" * 70)
        print("✅ Demo completed successfully!")
        print("=" * 70)
        print()
        print("Smart Study Assistant Syamkpa!")
        print("Thank you 🚀")
    
    # Run the demo
    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Import Error: {e}")
    print()
    print("Make sure you:")
    print("1. Activated the virtual environment")
    print("2. Installed dependencies: pip install -r requirements.txt")
    print()
except Exception as e:
    print(f"❌ Error: {e}")
    print()
