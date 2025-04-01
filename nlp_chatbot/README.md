# NLP Chatbot

A  chatbot built with Python, leveraging Natural Language Processing (NLP) capabilities through NLTK and spaCy libraries. This project features a beautiful dark-themed interface and robust backend processing for natural language understanding.


## Features

- **Natural Language Understanding**: Processes and understands user inputs using NLTK and spaCy
- **Intent Recognition**: Identifies user intentions from messages
- **Entity Recognition**: Extracts important entities from user queries
- **Sentiment Analysis**: Detects the emotional tone of user messages
- **Context Management**: Maintains conversation context for more natural interactions
- **Beautiful Dark-Themed Interface**: Modern, responsive design with animations and visual effects
- **Theme Toggle**: Switch between dark and light modes
- **Typing Indicators**: Realistic typing simulation for a more natural feel
- **Easy Deployment**: Simple setup process with clear instructions

## Demo

The chatbot can handle various types of queries including:
- Greetings and farewells
- Questions about its capabilities
- Requests for jokes
- General conversation

The chatbot responds appropriately based on the detected intent, entities, and sentiment of the user's message.

## Technology Stack

- **Backend**: Python, Flask
- **NLP Libraries**: NLTK, spaCy
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with responsive design and animations

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/mohammed-alan/fullstack-nlp-chatbot.git
   cd nlp-chatbot
   ```


2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Download NLTK data:
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
   ```

4. Download spaCy model:
   ```
   python -m spacy download en_core_web_sm
   ```

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Start chatting with the bot!


## Extending the Chatbot

### Adding New Intents

To add new intents, modify the `intents` dictionary in the `NLPProcessor` class:

```python
self.intents = {
    'new_intent': [
        'pattern1', 'pattern2', 'pattern3'
    ],
    # other intents...
}
```

Then add corresponding responses:

```python
self.responses = {
    'new_intent': [
        'Response 1', 'Response 2', 'Response 3'
    ],
    # other responses...
}
```

### Improving NLP Capabilities

- Use a larger spaCy model (e.g., `en_core_web_md` or `en_core_web_lg`) for better language understanding
- Implement machine learning models for intent classification
- Add more sophisticated sentiment analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Created by **Mohammed Al Ani**
