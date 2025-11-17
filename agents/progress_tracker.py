"""
Progress Tracker Agent - Tracks and analyzes student study progress.

This is a specialist agent that monitors learning progress and provides insights.
"""

import logging
from datetime import datetime
from typing import Dict

logger = logging.getLogger(__name__)


class ProgressTrackerAgent:
    """
    Progress Tracker Agent that monitors and analyzes student study progress.
    
    This agent demonstrates:
    - LLM-powered progress analysis
    - Memory management for tracking history
    - Data analysis and insights generation
    """
    
    def __init__(self, model):
        """
        Initialize the Progress Tracker Agent.
        
        Args:
            model: Gemini model instance for LLM-powered analysis
        """
        self.model = model
        logger.info("Progress Tracker Agent initialized")
    
    def track_progress(self, user_input: str, session_memory: Dict) -> Dict:
        """
        Track and analyze student progress.
        
        This demonstrates:
        - LLM reasoning for progress analysis
        - Memory management (storing progress history)
        - Insight generation based on historical data
        
        Args:
            user_input: User's progress update
            session_memory: Session memory for context
            
        Returns:
            Dictionary containing progress analysis and metadata
        """
        logger.info("Tracking progress...")
        
        # Create progress entry
        progress_entry = {
            'timestamp': datetime.now().isoformat(),
            'update': user_input
        }
        
        # Store in session memory
        session_memory['progress_history'].append(progress_entry)
        
        # Get historical context
        progress_history = session_memory.get('progress_history', [])
        study_plans = session_memory.get('study_plans', [])
        
        # Build context for analysis
        context = f"""
Progress history: {len(progress_history)} entries recorded
Active study plans: {len(study_plans)}
"""
        
        if len(progress_history) > 1:
            context += f"\nPrevious progress updates:\n"
            for entry in progress_history[-3:-1]:  # Last 2 entries before current
                context += f"- {entry['update']}\n"
        
        prompt = f"""You are a supportive study coach analyzing a student's progress.

Latest progress update: "{user_input}"
{context}

Provide an encouraging response that:
1. Acknowledges the progress made
2. Provides positive reinforcement
3. Offers insights or suggestions for continued improvement
4. Identifies any patterns or trends (if applicable)
5. Suggests next steps or areas to focus on

Be encouraging, specific, and actionable in your feedback.
"""
        
        try:
            # Use LLM to analyze progress
            response = self.model.generate_content(prompt)
            analysis_content = response.text
            
            # Calculate simple statistics
            total_entries = len(progress_history)
            
            logger.info(f"Progress tracked successfully. Total entries: {total_entries}")
            
            return {
                'status': 'success',
                'agent_used': 'progress_tracker',
                'message': analysis_content,
                'total_progress_entries': total_entries,
                'progress_recorded': True
            }
            
        except Exception as e:
            logger.error(f"Error tracking progress: {e}")
            return {
                'status': 'error',
                'agent_used': 'progress_tracker',
                'message': f'Unable to track progress: {str(e)}'
            }
    
    def get_progress_summary(self, session_memory: Dict) -> Dict:
        """
        Get a summary of all progress made.
        
        This is a custom tool function that analyzes progress data.
        
        Args:
            session_memory: Session memory containing progress history
            
        Returns:
            Dictionary with progress statistics
        """
        progress_history = session_memory.get('progress_history', [])
        
        if not progress_history:
            return {
                'total_entries': 0,
                'message': 'No progress recorded yet'
            }
        
        # Calculate statistics
        total_entries = len(progress_history)
        
        # Get date range
        if progress_history:
            first_entry = progress_history[0]['timestamp']
            last_entry = progress_history[-1]['timestamp']
        else:
            first_entry = last_entry = 'N/A'
        
        return {
            'total_entries': total_entries,
            'first_entry_date': first_entry,
            'last_entry_date': last_entry,
            'message': f'You have recorded {total_entries} progress updates. Keep up the great work!'
        }
