"""
Study Planner Agent - Creates personalized study plans and schedules.

This is a specialist agent that uses LLM reasoning combined with custom tools.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict

logger = logging.getLogger(__name__)


class StudyPlannerAgent:
    """
    Study Planner Agent that creates personalized study schedules
    based on user requirements and constraints.
    
    This agent demonstrates:
    - LLM-powered reasoning
    - Custom tool usage
    - Memory integration
    """
    
    def __init__(self, model):
        """
        Initialize the Study Planner Agent.
        
        Args:
            model: Gemini model instance for LLM-powered planning
        """
        self.model = model
        logger.info("Study Planner Agent initialized")
    
    def create_plan(self, user_input: str, session_memory: Dict) -> Dict:
        """
        Create a personalized study plan based on user requirements.
        
        This demonstrates:
        - LLM reasoning for plan creation
        - Integration with session memory
        - Custom tool usage (schedule creation)
        
        Args:
            user_input: User's study planning request
            session_memory: Session memory for context
            
        Returns:
            Dictionary containing the study plan and metadata
        """
        logger.info("Creating study plan...")
        
        # Extract context from session memory
        previous_plans = session_memory.get('study_plans', [])
        user_profile = session_memory.get('user_profile', {})
        
        # Build context-aware prompt
        context = ""
        if previous_plans:
            context = f"\nPrevious plans created: {len(previous_plans)}"
        if user_profile:
            context += f"\nUser profile: {user_profile}"
        
        prompt = f"""You are an expert study planner helping a student create an effective study schedule.

User request: "{user_input}"
{context}

Create a detailed, personalized study plan that includes:
1. Overall strategy and approach
2. Daily breakdown of topics to study
3. Time allocation for each topic
4. Study techniques and tips
5. Milestones and checkpoints

Provide a comprehensive, actionable study plan in a clear format.
"""
        
        try:
            # Use LLM to generate the study plan
            response = self.model.generate_content(prompt)
            plan_content = response.text
            
            # Create structured plan object
            study_plan = {
                'created_at': datetime.now().isoformat(),
                'request': user_input,
                'plan_content': plan_content,
                'status': 'active'
            }
            
            # Store in session memory (demonstrates memory management)
            session_memory['study_plans'].append(study_plan)
            
            # Update user profile if new information is available
            if 'exam' in user_input.lower() or 'test' in user_input.lower():
                session_memory['user_profile']['has_upcoming_exam'] = True
            
            logger.info("Study plan created successfully")
            
            return {
                'status': 'success',
                'agent_used': 'study_planner',
                'message': plan_content,
                'plan_id': len(session_memory['study_plans']) - 1
            }
            
        except Exception as e:
            logger.error(f"Error creating study plan: {e}")
            return {
                'status': 'error',
                'agent_used': 'study_planner',
                'message': f'Unable to create study plan: {str(e)}'
            }
    
    def get_study_tips(self, topic: str) -> str:
        """
        Get study tips for a specific topic.
        
        This is a custom tool function.
        
        Args:
            topic: The topic to get tips for
            
        Returns:
            Study tips as a string
        """
        # This is a simple custom tool implementation
        tips = {
            'programming': [
                'Practice coding daily, even if just for 30 minutes',
                'Work on small projects to apply concepts',
                'Use debugging as a learning tool',
                'Read other people\'s code to learn different approaches'
            ],
            'mathematics': [
                'Practice problems regularly',
                'Understand concepts before memorizing formulas',
                'Work through examples step by step',
                'Create summary sheets for quick review'
            ],
            'languages': [
                'Practice speaking daily',
                'Immerse yourself in the language (media, books)',
                'Use spaced repetition for vocabulary',
                'Focus on practical conversation skills'
            ]
        }
        
        # Return relevant tips or general tips
        for key in tips:
            if key in topic.lower():
                return '\n'.join(tips[key])
        
        return "Study consistently, take breaks, and review regularly."
