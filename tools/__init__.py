"""
Tools package for Smart Study Assistant.
"""

from .study_tools import (
    create_study_schedule,
    save_progress,
    get_study_tips,
    calculate_study_statistics,
    generate_quiz_questions
)

__all__ = [
    'create_study_schedule',
    'save_progress',
    'get_study_tips',
    'calculate_study_statistics',
    'generate_quiz_questions'
]
