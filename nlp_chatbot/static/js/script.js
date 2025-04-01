// Enhanced JavaScript for NLP Chatbot
document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const themeToggle = document.getElementById('theme-toggle');
    
    // Focus on input field when page loads
    userInput.focus();
    
    // Theme toggle functionality
    let darkMode = true; // Start with dark mode by default
    
    themeToggle.addEventListener('click', function() {
        darkMode = !darkMode;
        document.body.classList.toggle('light-mode');
        themeToggle.innerHTML = darkMode ? '<i class="fas fa-moon"></i>' : '<i class="fas fa-sun"></i>';
    });

    // Function to format current time
    function getCurrentTime() {
        const now = new Date();
        let hours = now.getHours();
        let minutes = now.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'
        minutes = minutes < 10 ? '0' + minutes : minutes;
        
        return hours + ':' + minutes + ' ' + ampm;
    }

    // Function to add a message to the chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');

        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');

        const messageParagraph = document.createElement('p');
        messageParagraph.textContent = message;
        
        const messageTime = document.createElement('div');
        messageTime.classList.add('message-time');
        messageTime.textContent = getCurrentTime();

        messageContent.appendChild(messageParagraph);
        messageContent.appendChild(messageTime);
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);

        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Add a subtle animation effect
        setTimeout(() => {
            messageContent.style.transform = 'scale(1.03)';
            setTimeout(() => {
                messageContent.style.transform = 'scale(1)';
            }, 150);
        }, 50);
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message');
        typingDiv.id = 'typing-indicator';

        const typingContent = document.createElement('div');
        typingContent.classList.add('typing-indicator');

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            typingContent.appendChild(dot);
        }

        typingDiv.appendChild(typingContent);
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Function to send message to backend
    async function sendMessage(message) {
        try {
            showTypingIndicator();
            
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Simulate a slight delay for more natural conversation flow
            // Random delay between 1s and 2.5s based on message length
            const typingDelay = Math.min(1000 + message.length * 50, 2500);
            
            setTimeout(() => {
                removeTypingIndicator();
                addMessage(data.response, false);
                
                // Play a subtle notification sound
                const audio = new Audio('/static/sounds/message.mp3');
                audio.volume = 0.3;
                audio.play().catch(e => console.log('Audio play failed: Browser requires user interaction first'));
            }, typingDelay);
            
        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessage('Sorry, I encountered an error processing your request.', false);
        }
    }

    // Function to handle sending a message
    function handleSendMessage() {
        const message = userInput.value.trim();
        
        if (message) {
            // Add user message to chat
            addMessage(message, true);
            
            // Clear input field
            userInput.value = '';
            
            // Send message to backend
            sendMessage(message);
        }
    }

    // Event listener for send button
    sendButton.addEventListener('click', handleSendMessage);

    // Event listener for Enter key
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });

    // Add animation to input field when focused
    userInput.addEventListener('focus', function() {
        this.style.transform = 'scale(1.01)';
    });
    
    userInput.addEventListener('blur', function() {
        this.style.transform = 'scale(1)';
    });

    // Event listener for suggestions
    document.querySelectorAll('.suggestion').forEach(suggestion => {
        suggestion.addEventListener('click', function(e) {
            e.preventDefault();
            userInput.value = this.textContent;
            handleSendMessage();
        });
    });
    
    // Add welcome animation
    setTimeout(() => {
        document.querySelector('.chat-container').style.opacity = '1';
        document.querySelector('.chat-container').style.transform = 'translateY(0)';
    }, 300);
});
