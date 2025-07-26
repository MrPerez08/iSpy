"""
Flask backend for iSpy Conversation Analyzer
"""
import json
import uuid
import requests
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# In-memory storage for conversations (use Redis/Database in production)
conversations = {}

class ConversationManager:
    @staticmethod
    def get_session_id():
        """Get or create session ID"""
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
            session.permanent = True
        return session['session_id']
    
    @staticmethod
    def get_conversation(session_id):
        """Get conversation for session"""
        if session_id not in conversations:
            conversations[session_id] = {
                'messages': [],
                'created_at': datetime.now().isoformat(),
                'last_analysis': None
            }
        return conversations[session_id]
    
    @staticmethod
    def add_message(session_id, role, content):
        """Add message to conversation"""
        conversation = ConversationManager.get_conversation(session_id)
        message = {
            'id': str(uuid.uuid4()),
            'role': role,  # 'user' or 'assistant'
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        conversation['messages'].append(message)
        return message

class OllamaService:
    @staticmethod
    def is_available():
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    @staticmethod
    def generate_response(prompt, model=None):
        """Generate response using Ollama"""
        if not model:
            model = Config.OLLAMA_MODEL
            
        try:
            # Different settings for analysis vs chat
            is_analysis = "JSON" in prompt and "analyze" in prompt.lower()
            
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1 if is_analysis else 0.7,  # Lower temp for analysis
                    "top_p": 0.9,
                    "max_tokens": 4096 if is_analysis else 2048,  # More tokens for analysis
                    "repeat_penalty": 1.1,
                    "stop": ["```"] if is_analysis else None  # Stop at code blocks for analysis
                }
            }
            
            app.logger.info(f"Sending request to Ollama: {Config.OLLAMA_BASE_URL}/api/generate")
            
            response = requests.post(
                f"{Config.OLLAMA_BASE_URL}/api/generate",
                json=payload,
                timeout=Config.OLLAMA_TIMEOUT
            )
            
            app.logger.info(f"Ollama response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '').strip()
                
                if not generated_text:
                    return "Error: Empty response from Ollama"
                
                app.logger.info(f"Generated response length: {len(generated_text)} characters")
                return generated_text
            else:
                error_msg = f"Ollama returned status {response.status_code}"
                try:
                    error_detail = response.json().get('error', 'Unknown error')
                    error_msg += f": {error_detail}"
                except:
                    pass
                app.logger.error(error_msg)
                return f"Error: {error_msg}"
                
        except requests.exceptions.Timeout:
            error_msg = "Request timed out. Please try again."
            app.logger.error(error_msg)
            return f"Error: {error_msg}"
        except requests.exceptions.RequestException as e:
            error_msg = f"Could not connect to Ollama service. {str(e)}"
            app.logger.error(error_msg)
            return f"Error: {error_msg}"
    
    @staticmethod
    def analyze_conversation(messages):
        """Analyze conversation using Ollama"""
        # Format conversation for analysis with clear focus on user messages
        conversation_text = "CONVERSATION ANALYSIS - Focus on USER emotional state and statements:\n\n"
        
        user_message_count = 0
        for msg in messages:
            timestamp = msg['timestamp'][:19]  # Remove microseconds
            if msg['role'] == 'user':
                user_message_count += 1
                conversation_text += f"=== USER MESSAGE #{user_message_count} [{timestamp}] ===\n"
                conversation_text += f"USER SAYS: {msg['content']}\n\n"
            else:
                conversation_text += f"[{timestamp}] AI Assistant Response: {msg['content']}\n\n"
        
        conversation_text += f"\nANALYSIS FOCUS: What is the USER experiencing emotionally? What are they telling you about their situation, feelings, and state of mind? Base your analysis on the USER's actual statements.\n"
        
        # Create analysis prompt
        analysis_prompt = f"{Config.get_analysis_prompt()}\n\n{conversation_text}"
        
        try:
            # Use a specialized analysis model if available, otherwise use default
            analysis_model = Config.OLLAMA_MODEL
            response = OllamaService.generate_response(analysis_prompt, analysis_model)
            
            app.logger.info(f"Raw LLM response: {response[:500]}...")  # Log first 500 chars
            
            # Multiple attempts to parse JSON response
            json_attempts = [
                response.strip(),  # Try as-is
                response.strip().replace('```json', '').replace('```', '').strip(),  # Remove markdown
                response[response.find('{'):response.rfind('}')+1] if '{' in response and '}' in response else response,  # Extract JSON block
            ]
            
            analysis_result = None
            parse_error = None
            
            for attempt in json_attempts:
                try:
                    if attempt:
                        analysis_result = json.loads(attempt)
                        app.logger.info("Successfully parsed JSON response")
                        break
                except json.JSONDecodeError as e:
                    parse_error = str(e)
                    continue
            
            if analysis_result is None:
                app.logger.error(f"All JSON parsing attempts failed. Last error: {parse_error}")
                # Create structured analysis from text response
                return OllamaService.create_fallback_analysis(response, messages)
            
            # Validate and enhance the parsed result
            analysis_result = OllamaService.validate_and_enhance_analysis(analysis_result, messages)
            
            return analysis_result
                
        except Exception as e:
            app.logger.error(f"Analysis error: {str(e)}")
            return OllamaService.create_error_analysis(str(e), messages)
    
    @staticmethod
    def validate_and_enhance_analysis(analysis, messages):
        """Validate and enhance analysis result"""
        # Ensure required fields exist
        required_fields = {
            'risk_level': 'MEDIUM',
            'confidence': 0.7,
            'overall_assessment': 'Analysis completed successfully'
        }
        
        for field, default in required_fields.items():
            if field not in analysis:
                analysis[field] = default
        
        # Ensure risk_level is valid
        valid_risk_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        if analysis['risk_level'] not in valid_risk_levels:
            analysis['risk_level'] = 'MEDIUM'
        
        # Ensure confidence is a number between 0 and 1
        try:
            confidence = float(analysis.get('confidence', 0.7))
            analysis['confidence'] = max(0.0, min(1.0, confidence))
        except (ValueError, TypeError):
            analysis['confidence'] = 0.7
        
        # Ensure nested structures exist
        if 'intent_analysis' not in analysis:
            analysis['intent_analysis'] = {
                'primary_intent': 'General conversation',
                'secondary_intents': [],
                'concerning_intents': []
            }
        
        if 'emotional_indicators' not in analysis:
            analysis['emotional_indicators'] = {
                'dominant_emotions': ['neutral'],
                'emotional_progression': 'Stable throughout conversation',
                'stability_assessment': 'No major concerns detected'
            }
        
        if 'communication_patterns' not in analysis:
            analysis['communication_patterns'] = {
                'style': 'Conversational and appropriate',
                'consistency': 'Messages are consistent',
                'authenticity': 'Appears genuine'
            }
        
        if 'recommendations' not in analysis:
            analysis['recommendations'] = {
                'immediate_actions': [],
                'monitoring_suggestions': ['Continue normal interaction'],
                'support_resources': [],
                'follow_up_timeline': 'As needed'
            }
        
        if 'red_flags' not in analysis:
            analysis['red_flags'] = []
        
        # Enhance metadata
        if 'analysis_metadata' not in analysis:
            analysis['analysis_metadata'] = {}
        
        analysis['analysis_metadata'].update({
            'message_count': len(messages),
            'analysis_timestamp': datetime.now().isoformat(),
            'parsing_method': 'standard_json'
        })
        
        return analysis
    
    @staticmethod
    def create_fallback_analysis(raw_response, messages):
        """Create analysis from unparseable response"""
        app.logger.info("Creating fallback analysis from text response")
        
        # Extract user messages for better analysis
        user_messages = [msg['content'].lower() for msg in messages if msg['role'] == 'user']
        user_text = ' '.join(user_messages)
        response_lower = raw_response.lower()
        
        # Enhanced emotion detection from user messages
        emotions = []
        emotion_map = {
            'upset': ['upset', 'frustrated', 'annoyed'],
            'sad': ['sad', 'depressed', 'down', 'unhappy', 'miserable'],
            'angry': ['angry', 'mad', 'furious', 'rage', 'pissed'],
            'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'panic'],
            'happy': ['happy', 'joy', 'excited', 'glad', 'cheerful', 'great'],
            'confused': ['confused', 'lost', 'unsure', 'don\'t know'],
            'tired': ['tired', 'exhausted', 'drained', 'worn out'],
            'overwhelmed': ['overwhelmed', 'too much', 'can\'t handle']
        }
        
        detected_emotions = []
        for emotion, keywords in emotion_map.items():
            if any(keyword in user_text for keyword in keywords):
                detected_emotions.append(emotion)
        
        # Check for explicit emotional statements
        emotional_phrases = [
            'i am ', 'i feel ', 'i\'m ', 'feeling ', 'i have been ', 'i\'ve been '
        ]
        
        for user_msg in user_messages:
            for phrase in emotional_phrases:
                if phrase in user_msg:
                    # Extract what comes after the phrase
                    start_idx = user_msg.find(phrase) + len(phrase)
                    following_text = user_msg[start_idx:start_idx+50]  # Next 50 chars
                    
                    # Check if it contains emotion words
                    for emotion, keywords in emotion_map.items():
                        if any(keyword in following_text for keyword in keywords):
                            detected_emotions.append(emotion)
        
        if not detected_emotions:
            detected_emotions = ['neutral']
        
        # Remove duplicates while preserving order
        emotions = list(dict.fromkeys(detected_emotions))
        
        # Determine risk level based on emotional content
        risk_level = 'LOW'
        high_risk_emotions = ['angry', 'furious', 'suicidal', 'hopeless']
        medium_risk_emotions = ['upset', 'sad', 'anxious', 'overwhelmed', 'depressed']
        
        if any(emotion in user_text for emotion in high_risk_emotions):
            risk_level = 'HIGH'
        elif any(emotion in user_text for emotion in medium_risk_emotions):
            risk_level = 'MEDIUM'
        
        # Extract key concerns from user messages
        user_concerns = []
        concern_keywords = ['problem', 'issue', 'trouble', 'difficult', 'hard', 'struggle', 'can\'t', 'won\'t', 'help']
        for msg in user_messages:
            for keyword in concern_keywords:
                if keyword in msg:
                    # Extract sentence containing the keyword
                    sentences = msg.split('.')
                    for sentence in sentences:
                        if keyword in sentence:
                            user_concerns.append(sentence.strip())
                            break
        
        return {
            'risk_level': risk_level,
            'confidence': 0.8 if detected_emotions != ['neutral'] else 0.5,
            'overall_assessment': f"User expresses {', '.join(emotions)} emotions. Analysis extracted from user's direct statements about their emotional state and situation.",
            'intent_analysis': {
                'primary_intent': 'Expressing emotional state and seeking support',
                'secondary_intents': ['Sharing personal situation', 'Looking for understanding'],
                'concerning_intents': user_concerns[:2] if user_concerns else []  # Top 2 concerns
            },
            'red_flags': [],
            'emotional_indicators': {
                'dominant_emotions': emotions,
                'emotional_progression': f"User has expressed {', '.join(emotions)} emotions throughout conversation",
                'stability_assessment': 'Based on user statements about their emotional state'
            },
            'communication_patterns': {
                'style': 'User is directly communicating their emotional state',
                'consistency': 'Consistent with expressed emotions',
                'authenticity': 'Appears genuine in emotional expression'
            },
            'user_situation_analysis': {
                'life_circumstances': 'User has shared emotional concerns requiring attention',
                'support_needs': 'Emotional support and understanding',
                'coping_mechanisms': 'Seeking conversation and support',
                'stress_factors': user_concerns[:3] if user_concerns else ['General emotional distress']
            },
            'recommendations': {
                'immediate_actions': ['Acknowledge user\'s emotional state', 'Provide appropriate support'],
                'monitoring_suggestions': ['Continue checking on emotional well-being'],
                'support_resources': ['Emotional support resources', 'Professional guidance if needed'],
                'follow_up_timeline': 'Regular check-ins based on emotional state'
            },
            'analysis_metadata': {
                'message_count': len(messages),
                'analysis_timestamp': datetime.now().isoformat(),
                'key_themes': emotions + ['emotional_support_needed'],
                'conversation_quality': 'User is expressing genuine emotions',
                'parsing_method': 'enhanced_text_fallback',
                'user_emotional_keywords_detected': list(set(detected_emotions)),
                'raw_response_sample': raw_response[:200]
            }
        }
    
    @staticmethod
    def create_error_analysis(error_msg, messages):
        """Create analysis for complete errors"""
        return {
            'risk_level': 'HIGH',
            'confidence': 0.3,
            'overall_assessment': 'Analysis failed - manual review required',
            'intent_analysis': {
                'primary_intent': 'Analysis error occurred',
                'secondary_intents': [],
                'concerning_intents': []
            },
            'red_flags': [
                {
                    'flag': 'Analysis system failure',
                    'severity': 'HIGH',
                    'evidence': 'Technical error during processing',
                    'context': 'Manual review required due to system limitations'
                }
            ],
            'emotional_indicators': {
                'dominant_emotions': ['unknown'],
                'emotional_progression': 'Could not analyze',
                'stability_assessment': 'Manual review required'
            },
            'communication_patterns': {
                'style': 'Analysis incomplete',
                'consistency': 'Unknown',
                'authenticity': 'Could not assess'
            },
            'recommendations': {
                'immediate_actions': ['Manual conversation review', 'Check system logs'],
                'monitoring_suggestions': ['Continue observation', 'Retry analysis later'],
                'support_resources': ['Technical support', 'Manual analysis'],
                'follow_up_timeline': 'Immediate technical review needed'
            },
            'analysis_metadata': {
                'message_count': len(messages),
                'analysis_timestamp': datetime.now().isoformat(),
                'key_themes': ['system_error'],
                'conversation_quality': 'Could not assess',
                'error': error_msg,
                'parsing_method': 'error_fallback'
            }
        }

# Routes
@app.route('/')
def index():
    """Main chat interface"""
    session_id = ConversationManager.get_session_id()
    return render_template('index.html', session_id=session_id)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        session_id = ConversationManager.get_session_id()
        
        # Add user message
        user_message = ConversationManager.add_message(session_id, 'user', message)
        
        # Generate assistant response
        conversation = ConversationManager.get_conversation(session_id)
        
        # Create context for assistant (last few messages)
        context_messages = conversation['messages'][-6:]  # Last 6 messages for context
        context = ""
        for msg in context_messages[:-1]:  # Exclude the current message
            role = "User" if msg['role'] == 'user' else "Assistant"
            context += f"{role}: {msg['content']}\n"
        
        # Generate response
        assistant_prompt = f"""You are {Config.ASSISTANT_NAME}, a {Config.ASSISTANT_PERSONALITY} AI assistant. 

Previous conversation context:
{context}

Current user message: {message}

Respond naturally and helpfully. Keep responses conversational and engaging, but concise when appropriate."""

        assistant_response = OllamaService.generate_response(assistant_prompt)
        
        # Add assistant message
        assistant_message = ConversationManager.add_message(session_id, 'assistant', assistant_response)
        
        return jsonify({
            'user_message': user_message,
            'assistant_message': assistant_message,
            'conversation_length': len(conversation['messages'])
        })
        
    except Exception as e:
        return jsonify({'error': f'Chat error: {str(e)}'}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze the conversation"""
    try:
        # Add debug logging
        app.logger.info("Analysis request received")
        
        session_id = ConversationManager.get_session_id()
        conversation = ConversationManager.get_conversation(session_id)
        messages = conversation['messages']
        
        app.logger.info(f"Session ID: {session_id}, Messages: {len(messages)}")
        
        if len(messages) < Config.MIN_MESSAGES_FOR_ANALYSIS:
            return jsonify({
                'error': f'Need at least {Config.MIN_MESSAGES_FOR_ANALYSIS} messages for analysis'
            }), 400
        
        # Check conversation length
        total_length = sum(len(msg['content']) for msg in messages)
        if total_length > Config.MAX_CONVERSATION_LENGTH:
            return jsonify({
                'error': 'Conversation too long for analysis'
            }), 400
        
        app.logger.info("Starting conversation analysis...")
        
        # Perform analysis
        analysis_result = OllamaService.analyze_conversation(messages)
        
        app.logger.info("Analysis completed successfully")
        
        # Store analysis result
        conversation['last_analysis'] = analysis_result
        
        return jsonify({
            'analysis': analysis_result,
            'conversation_stats': {
                'message_count': len(messages),
                'total_length': total_length,
                'analysis_timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        app.logger.error(f"Analysis error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Analysis error: {str(e)}'}), 500

@app.route('/api/conversation', methods=['GET'])
def get_conversation():
    """Get current conversation"""
    try:
        session_id = ConversationManager.get_session_id()
        conversation = ConversationManager.get_conversation(session_id)
        
        return jsonify({
            'messages': conversation['messages'],
            'created_at': conversation['created_at'],
            'last_analysis': conversation.get('last_analysis'),
            'message_count': len(conversation['messages'])
        })
        
    except Exception as e:
        return jsonify({'error': f'Error retrieving conversation: {str(e)}'}), 500

@app.route('/api/new-conversation', methods=['POST'])
def new_conversation():
    """Start a new conversation"""
    try:
        # Generate new session ID
        new_session_id = str(uuid.uuid4())
        session['session_id'] = new_session_id
        
        # Initialize new conversation
        ConversationManager.get_conversation(new_session_id)
        
        return jsonify({
            'session_id': new_session_id,
            'message': 'New conversation started'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error starting new conversation: {str(e)}'}), 500

@app.route('/api/debug', methods=['GET'])
def debug():
    """Debug endpoint to check system state"""
    session_id = ConversationManager.get_session_id()
    conversation = ConversationManager.get_conversation(session_id)
    
    return jsonify({
        'session_id': session_id,
        'message_count': len(conversation['messages']),
        'ollama_available': OllamaService.is_available(),
        'ollama_url': Config.OLLAMA_BASE_URL,
        'ollama_model': Config.OLLAMA_MODEL,
        'routes': [str(rule) for rule in app.url_map.iter_rules()],
        'last_analysis': conversation.get('last_analysis') is not None
    })

@app.route('/api/status', methods=['GET'])
def status():
    """Get system status"""
    ollama_available = OllamaService.is_available()
    
    return jsonify({
        'status': 'online',
        'ollama_available': ollama_available,
        'ollama_model': Config.OLLAMA_MODEL,
        'session_count': len(conversations),
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)