"""
Question Answerer Agent - Answers student questions about various topics.

This is a specialist agent that provides detailed explanations and answers.
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)


class QuestionAnswererAgent:
    """
    Question Answerer Agent that provides detailed answers to student questions.
    
    This agent demonstrates:
    - LLM-powered question answering
    - Context-aware responses using session memory
    - Educational explanation generation
    """
    
    def __init__(self, model):
        """
        Initialize the Question Answerer Agent.
        
        Args:
            model: Gemini model instance for LLM-powered answering
        """
        self.model = model
        logger.info("Question Answerer Agent initialized")
    
    def answer_question(self, user_input: str, session_memory: Dict) -> Dict:
        """
        Answer a student's question with detailed explanation.
        
        This demonstrates:
        - LLM reasoning for educational responses
        - Context integration from session memory
        - Structured answer generation
        
        Args:
            user_input: Student's question
            session_memory: Session memory for context
            
        Returns:
            Dictionary containing the answer and metadata
        """
        logger.info("Answering question...")
        
        # Extract context from session memory
        conversation_history = session_memory.get('conversation_history', [])
        study_plans = session_memory.get('study_plans', [])
        
        # Build context from recent interactions
        context = ""
        if study_plans:
            recent_plan = study_plans[-1]
            context += f"\nStudent is currently studying: {recent_plan.get('request', 'various topics')}"
        
        if len(conversation_history) > 0:
            context += f"\nThis is interaction #{len(conversation_history) + 1} in this session"
        
        prompt = f"""You are a knowledgeable and patient tutor helping a student learn.

Student's question: "{user_input}"
{context}

Provide a clear, detailed answer that:
1. Directly answers the question
2. Explains the concept in simple terms
3. Provides examples where helpful
4. Suggests related topics to explore
5. Encourages the student's learning

Be educational, encouraging, and thorough in your explanation.
"""
        
        try:
            # Use LLM to generate the answer
            response = self.model.generate_content(prompt)
            answer_content = response.text
            
            logger.info("Question answered successfully")
            
            return {
                'status': 'success',
                'agent_used': 'question_answerer',
                'message': answer_content,
                'question': user_input
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return {
                'status': 'error',
                'agent_used': 'question_answerer',
                'message': f'Unable to answer question: {str(e)}'
            }
    
    def get_related_topics(self, question: str) -> list:
        """
        Get related topics for a given question.
        
        This is a custom tool function.
        
        Args:
            question: The original question
            
        Returns:
            List of related topics
        """
        # Simple keyword-based related topics
        # In a real implementation, this could use more sophisticated NLP
        
        keywords_to_topics = {
            'python': ['variables', 'functions', 'loops', 'data structures'],
            'list': ['arrays', 'tuples', 'dictionaries', 'sets'],
            'function': ['parameters', 'return values', 'scope', 'recursion'],
            'loop': ['for loops', 'while loops', 'iteration', 'break and continue'],
            'class': ['objects', 'inheritance', 'methods', 'attributes']
        }
        
        question_lower = question.lower()
        related = []
        
        for keyword, topics in keywords_to_topics.items():
            if keyword in question_lower:
                related.extend(topics)
        
        return list(set(related))[:5]  # Return up to 5 unique topics
