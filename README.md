# bit-mentor-server

## Team members:  
- Muhammad Sarahni  
- Adam Kaabiya  
- Najeeb Ibrahim  
- Maysa Zbidat  
- Aseel Khamis  

## Overview  
This web server powers the Bit Mentor Telegram bot. It receives a topic from the bot and dynamically generates questions and answers related to that topic, then sends them to the bot.   

## Architecture  

The architecture for the Bit Mentor Telegram bot's web server consists of the following components:  

1. **FastAPI**: This serves as the web framework for the server, handling incoming requests from the Telegram bot and returning appropriate responses. I

2. **MongoDB**: This NoSQL database is used to store and manage the questions and answers as well as user's score.  

3. **OpenAI API**: The OpenAI API is utilized to generate questions and answers dynamically. When the server receives a topic from the client, it uses the OpenAI API to create relevant trivia questions and answers.   
