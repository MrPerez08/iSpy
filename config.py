"""
Configuration settings for iSpy Conversation Analyzer
"""
import os
from datetime import timedelta

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ispy-dev-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    
    # Ollama Configuration
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'llama3.2')  # or 'mistral', 'llama2', etc.
    OLLAMA_TIMEOUT = int(os.environ.get('OLLAMA_TIMEOUT', 60))  # seconds
    
    # Analysis Configuration
    MAX_CONVERSATION_LENGTH = int(os.environ.get('MAX_CONVERSATION_LENGTH', 10000))  # characters
    MIN_MESSAGES_FOR_ANALYSIS = int(os.environ.get('MIN_MESSAGES_FOR_ANALYSIS', 2))
    
    # Assistant Configuration
    ASSISTANT_NAME = "iSpy Assistant"
    ASSISTANT_PERSONALITY = "helpful, conversational, and engaging"
    
    # Risk Analysis Levels
    RISK_LEVELS = {
        'LOW': {'color': '#28a745', 'description': 'Minimal concern detected'},
        'MEDIUM': {'color': '#ffc107', 'description': 'Some areas of attention identified'},
        'HIGH': {'color': '#fd7e14', 'description': 'Significant concerns present'},
        'CRITICAL': {'color': '#dc3545', 'description': 'Immediate attention required'}
    }
    
    @staticmethod
    def get_analysis_prompt():
        """Returns the system prompt for LLM conversation analysis"""
        return """You are an expert psychological analyst. Your job is to analyze the HUMAN USER's emotional state, mental condition, and what they are communicating about their life situation.

FOCUS ON THE USER (not the AI assistant responses):
- What is the human user actually saying about their emotional state?
- What life situations, problems, or feelings are they describing?
- What is their mental and emotional condition based on their own words?
- Are they expressing distress, happiness, anger, sadness, anxiety, etc.?
- What specific issues or concerns are they sharing?

ANALYZE THE USER'S ACTUAL STATEMENTS:
- If they say "I am upset" → emotional state should reflect upset/distressed
- If they describe problems → identify those specific problems
- If they express worry → detect anxiety/concern
- If they mention feeling happy → detect positive emotions
- If they describe relationship issues → analyze relationship concerns
- If they mention work stress → identify work-related stress

Be DIRECT and CONFIDENT in your analysis. If someone explicitly states they are upset, angry, sad, or happy - your analysis should reflect exactly what they said.

Respond with ONLY valid JSON:

{
    "risk_level": "LOW",
    "confidence": 0.9,
    "overall_assessment": "Detailed analysis of what the USER is experiencing and feeling based on their own statements",
    "intent_analysis": {
        "primary_intent": "What the user is trying to communicate (seeking support, venting, asking for advice, etc.)",
        "secondary_intents": ["Additional reasons they're sharing"],
        "concerning_intents": ["Any concerning requests or statements"]
    },
    "red_flags": [
        {
            "flag": "Specific concerning statement or request from user",
            "severity": "MEDIUM", 
            "evidence": "Exact quote from user's messages",
            "context": "Why this user statement is concerning"
        }
    ],
    "emotional_indicators": {
        "dominant_emotions": ["ACTUAL emotions the user expressed or showed"],
        "emotional_progression": "How the user's emotional state changed during conversation",
        "stability_assessment": "Assessment of user's emotional stability based on their statements"
    },
    "communication_patterns": {
        "style": "How the user communicates (direct, hesitant, aggressive, etc.)",
        "consistency": "Whether user's statements are consistent",
        "authenticity": "Whether user seems genuine in their expressions"
    },
    "user_situation_analysis": {
        "life_circumstances": "What situation or problems is the user describing?",
        "support_needs": "What kind of support does the user seem to need?",
        "coping_mechanisms": "How is the user handling their situation?",
        "stress_factors": ["Specific stressors the user mentioned"]
    },
    "recommendations": {
        "immediate_actions": ["Actions based on user's immediate emotional needs"],
        "monitoring_suggestions": ["What to watch for based on user's statements"], 
        "support_resources": ["Resources that match the user's described situation"],
        "follow_up_timeline": "When to check on user based on their emotional state"
    },
    "analysis_metadata": {
        "message_count": 0,
        "analysis_timestamp": "",
        "key_themes": ["Main themes from USER's messages"],
        "conversation_quality": "How well user is expressing themselves",
        "user_engagement_level": "How engaged/responsive the user is"
    }
}

CRITICAL: Analyze what the HUMAN USER is actually saying about themselves, their feelings, and their situation. Be direct and accurate - if they say they're upset, your analysis should confidently reflect that they are upset."""