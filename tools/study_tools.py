"""
Custom Tools for the Smart Study Assistant.

These are custom tool functions that agents can use to perform specific tasks.
This demonstrates the "Custom Tools" requirement for the competition.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List

logger = logging.getLogger(__name__)


def create_study_schedule(subject: str, days: int, hours_per_day: float) -> Dict:
    """
    Create a structured study schedule.
    
    This is a custom tool that generates a schedule based on parameters.
    
    Args:
        subject: The subject to study
        days: Number of days to study
        hours_per_day: Hours available per day
        
    Returns:
        Dictionary containing the schedule
    """
    logger.info(f"Creating study schedule for {subject}, {days} days, {hours_per_day} hours/day")
    
    total_hours = days * hours_per_day
    
    # Create daily breakdown
    schedule = {
        'subject': subject,
        'total_days': days,
        'hours_per_day': hours_per_day,
        'total_hours': total_hours,
        'daily_schedule': []
    }
    
    # Generate daily entries
    start_date = datetime.now()
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        daily_entry = {
            'day': day + 1,
            'date': current_date.strftime('%Y-%m-%d'),
            'hours': hours_per_day,
            'focus': f'Day {day + 1} topics for {subject}'
        }
        schedule['daily_schedule'].append(daily_entry)
    
    logger.info("Study schedule created successfully")
    return schedule


def save_progress(progress_data: Dict, filename: str = 'progress.json') -> bool:
    """
    Save progress data to a file.
    
    This is a custom tool for data persistence.
    
    Args:
        progress_data: Dictionary containing progress information
        filename: File to save to
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filename, 'a') as f:
            json.dump(progress_data, f)
            f.write('\n')
        logger.info(f"Progress saved to {filename}")
        return True
    except Exception as e:
        logger.error(f"Error saving progress: {e}")
        return False


def get_study_tips(category: str) -> List[str]:
    """
    Get study tips for a specific category.
    
    This is a custom tool that provides curated study advice.
    
    Args:
        category: Category of study tips (e.g., 'time_management', 'memory', 'focus')
        
    Returns:
        List of study tips
    """
    tips_database = {
        'time_management': [
            'Use the Pomodoro Technique: 25 minutes of focused study, 5-minute break',
            'Create a daily schedule and stick to it',
            'Prioritize difficult subjects when your energy is highest',
            'Break large tasks into smaller, manageable chunks',
            'Set specific, achievable goals for each study session'
        ],
        'memory': [
            'Use spaced repetition to reinforce learning',
            'Create mnemonics and memory aids',
            'Teach concepts to others to solidify understanding',
            'Use active recall instead of passive reading',
            'Connect new information to what you already know'
        ],
        'focus': [
            'Eliminate distractions (phone, social media)',
            'Create a dedicated study space',
            'Use background music or white noise if helpful',
            'Take regular breaks to maintain concentration',
            'Stay hydrated and maintain good posture'
        ],
        'exam_prep': [
            'Start preparing well in advance, not last minute',
            'Practice with past papers and sample questions',
            'Identify and focus on weak areas',
            'Get adequate sleep before the exam',
            'Review key concepts the morning of the exam'
        ],
        'motivation': [
            'Set clear, meaningful goals',
            'Reward yourself for achieving milestones',
            'Study with peers for accountability',
            'Track your progress visually',
            'Remember your long-term objectives'
        ]
    }
    
    tips = tips_database.get(category.lower(), [
        'Stay consistent with your study routine',
        'Ask for help when you need it',
        'Believe in your ability to learn and improve'
    ])
    
    logger.info(f"Retrieved {len(tips)} tips for category: {category}")
    return tips


def calculate_study_statistics(progress_history: List[Dict]) -> Dict:
    """
    Calculate statistics from progress history.
    
    This is a custom tool for data analysis.
    
    Args:
        progress_history: List of progress entries
        
    Returns:
        Dictionary containing calculated statistics
    """
    if not progress_history:
        return {
            'total_sessions': 0,
            'average_per_week': 0,
            'message': 'No data available yet'
        }
    
    total_sessions = len(progress_history)
    
    # Calculate time span
    if len(progress_history) > 1:
        first_date = datetime.fromisoformat(progress_history[0]['timestamp'])
        last_date = datetime.fromisoformat(progress_history[-1]['timestamp'])
        days_span = (last_date - first_date).days + 1
        weeks_span = days_span / 7
        average_per_week = total_sessions / weeks_span if weeks_span > 0 else total_sessions
    else:
        average_per_week = total_sessions
    
    stats = {
        'total_sessions': total_sessions,
        'average_per_week': round(average_per_week, 2),
        'message': f'Great progress! You have completed {total_sessions} study sessions.'
    }
    
    logger.info(f"Statistics calculated: {stats}")
    return stats


def generate_quiz_questions(topic: str, difficulty: str = 'medium', count: int = 5) -> List[Dict]:
    """
    Generate practice quiz questions for a topic.
    
    This is a custom tool for generating practice materials.
    
    Args:
        topic: The topic to generate questions for
        difficulty: Difficulty level ('easy', 'medium', 'hard')
        count: Number of questions to generate
        
    Returns:
        List of question dictionaries
    """
    # This is a simplified implementation
    # In a real system, this could use an LLM or question database
    
    questions = []
    for i in range(count):
        question = {
            'id': i + 1,
            'topic': topic,
            'difficulty': difficulty,
            'question': f'Sample question {i + 1} about {topic}',
            'type': 'multiple_choice'
        }
        questions.append(question)
    
    logger.info(f"Generated {count} {difficulty} questions for {topic}")
    return questions
