"""
Modified NLP Processor Module for Chatbot
This module handles the core NLP functionality including text preprocessing,
intent recognition, and response generation.
"""

import re
import random
import nltk
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

class NLPProcessor:
    def __init__(self):
        """Initialize the NLP processor with necessary components"""
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Load spaCy model
        self.nlp = spacy.load('en_core_web_sm')
        
        # Define intents and their patterns
        self.intents = {
            'greeting': [
                'hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 
                'good evening', 'howdy', 'what\'s up', 'sup'
            ],
            'goodbye': [
                'bye', 'goodbye', 'see you', 'see you later', 'farewell', 
                'take care', 'until next time', 'cya'
            ],
            'thanks': [
                'thank you', 'thanks', 'appreciate it', 'thank you so much',
                'thanks a lot', 'grateful', 'thank you for your help'
            ],
            'help': [
                'help', 'can you help me', 'i need help', 'assist me', 'support',
                'how do i', 'how can i', 'what can you do', 'your capabilities'
            ],
            'weather': [
                'weather', 'temperature', 'forecast', 'is it raining',
                'is it sunny', 'how hot is it', 'how cold is it', 'climate'
            ],
            'time': [
                'time', 'what time is it', 'current time', 'clock', 'hour'
            ],
            'name': [
                'what is your name', 'who are you', 'your name', 'what should i call you',
                'introduce yourself', 'your identity'
            ],
            'capabilities': [
                'what can you do', 'your abilities', 'your functions', 'your capabilities',
                'how can you help me', 'what are you capable of', 'your features'
            ],
            'joke': [
                'joke', 'tell me a joke', 'be funny', 'make me laugh', 'humor me',
                'something funny', 'comedy'
            ],
            'unknown': []
        }
        
        # Define responses for each intent
        self.responses = {
            'greeting': [
                'Hello! How can I help you today?',
                'Hi there! What can I do for you?',
                'Hey! How can I assist you?',
                'Greetings! How may I be of service?'
            ],
            'goodbye': [
                'Goodbye! Have a great day!',
                'See you later! Take care!',
                'Farewell! Come back anytime you need assistance!',
                'Bye for now! It was nice chatting with you!'
            ],
            'thanks': [
                'You\'re welcome!',
                'Happy to help!',
                'Anytime!',
                'My pleasure!'
            ],
            'help': [
                'I can help with various tasks. Try asking me about the weather, time, or tell me to share a joke!',
                'I\'m here to assist you. You can ask me questions or request information on different topics.',
                'How can I help you today? I can answer questions, provide information, or just chat!'
            ],
            'weather': [
                'I\'m sorry, I don\'t have access to real-time weather data. You might want to check a weather service for that information.',
                'I can\'t provide current weather information, but I can help with other questions!'
            ],
            'time': [
                'I don\'t have access to the current time. You might want to check your device clock.',
                'I\'m unable to tell the current time, but I can assist with other queries!'
            ],
            'name': [
                'I\'m an NLP-powered chatbot created to assist you!',
                'You can call me NLP Bot. I\'m here to help!',
                'I\'m your friendly AI assistant powered by natural language processing.'
            ],
            'capabilities': [
                'I can understand natural language, answer questions, provide information, and have simple conversations.',
                'I\'m designed to process natural language and respond to various queries and requests.',
                'I can chat with you, answer questions, and assist with information on different topics.'
            ],
            'joke': [
                'Why don\'t scientists trust atoms? Because they make up everything!',
                'What did one wall say to the other wall? I\'ll meet you at the corner!',
                'Why did the scarecrow win an award? Because he was outstanding in his field!',
                'How does a penguin build its house? Igloos it together!',
                'Why don\'t eggs tell jokes? They\'d crack each other up!'
            ],
            'unknown': [
                'I\'m not sure I understand. Could you rephrase that?',
                'I don\'t have information about that. Is there something else I can help with?',
                'I\'m still learning and don\'t have an answer for that yet.',
                'I didn\'t quite catch that. Could you try asking in a different way?'
            ]
        }
        
        # Track conversation context
        self.context = {
            'current_topic': None,
            'previous_intent': None,
            'conversation_history': []
        }

    def preprocess_text(self, text):
        """
        Preprocess the input text by converting to lowercase,
        removing punctuation, tokenizing with spaCy, removing stopwords, and lemmatizing
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        
        # Use spaCy for tokenization instead of NLTK
        doc = self.nlp(text)
        
        # Remove stopwords and get lemmas
        processed_tokens = [
            token.lemma_ 
            for token in doc 
            if token.text not in self.stop_words
        ]
        
        return processed_tokens

    def recognize_intent(self, text):
        """Determine the intent of the user's message"""
        processed_tokens = self.preprocess_text(text)
        
        # Check for intent matches
        intent_scores = {}
        
        for intent, patterns in self.intents.items():
            score = 0
            for pattern in patterns:
                pattern_tokens = self.preprocess_text(pattern)
                # Count matching tokens
                for token in processed_tokens:
                    if token in pattern_tokens:
                        score += 1
            
            # Normalize score by the number of tokens in the input
            if processed_tokens:
                intent_scores[intent] = score / len(processed_tokens)
            else:
                intent_scores[intent] = 0
        
        # Get the intent with the highest score
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        
        # If the best score is too low, return 'unknown'
        if best_intent[1] < 0.2:
            return 'unknown'
        
        return best_intent[0]

    def extract_entities(self, text):
        """Extract entities from the text using spaCy"""
        doc = self.nlp(text)
        
        entities = {
            'nouns': [token.text for token in doc if token.pos_ == 'NOUN'],
            'verbs': [token.text for token in doc if token.pos_ == 'VERB'],
            'adjectives': [token.text for token in doc if token.pos_ == 'ADJ'],
            'named_entities': [(ent.text, ent.label_) for ent in doc.ents]
        }
        
        return entities

    def analyze_sentiment(self, text):
        """Analyze the sentiment of the text using spaCy"""
        doc = self.nlp(text)
        
        # Simple sentiment analysis based on positive and negative words
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'love', 'like', 'enjoy']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'sad', 'hate', 'dislike', 'poor', 'angry']
        
        sentiment_score = 0
        for token in doc:
            if token.text.lower() in positive_words:
                sentiment_score += 1
            elif token.text.lower() in negative_words:
                sentiment_score -= 1
        
        if sentiment_score > 0:
            return 'positive'
        elif sentiment_score < 0:
            return 'negative'
        else:
            return 'neutral'

    def update_context(self, text, intent):
        """Update the conversation context"""
        self.context['previous_intent'] = intent
        self.context['conversation_history'].append((text, intent))
        
        # Limit history to last 5 exchanges
        if len(self.context['conversation_history']) > 5:
            self.context['conversation_history'] = self.context['conversation_history'][-5:]

    def generate_response(self, text):
        """Generate a response based on the recognized intent and context"""
        intent = self.recognize_intent(text)
        entities = self.extract_entities(text)
        sentiment = self.analyze_sentiment(text)
        
        # Update conversation context
        self.update_context(text, intent)
        
        # Get a random response for the recognized intent
        if intent in self.responses:
            responses = self.responses[intent]
            response = random.choice(responses)
        else:
            response = random.choice(self.responses['unknown'])
        
        # Personalize response based on entities if appropriate
        if intent == 'greeting' and entities['named_entities']:
            for entity, label in entities['named_entities']:
                if label == 'PERSON':
                    response = f"Hello {entity}! How can I help you today?"
                    break
        
        # Acknowledge sentiment if strongly positive or negative
        if intent not in ['greeting', 'goodbye', 'thanks'] and sentiment != 'neutral':
            if sentiment == 'positive':
                response += " I'm glad you're feeling positive about this!"
            elif sentiment == 'negative':
                response += " I understand this might be frustrating."
        
        return response

    def process_message(self, message):
        """Process the user message and return a response"""
        if not message.strip():
            return "I didn't receive any message. How can I help you?"
        
        return self.generate_response(message)
