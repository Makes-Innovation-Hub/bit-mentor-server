# bit-mentor-server  
  
## Table of Contents  
- [Team Members](#team-members)  
- [Overview](#overview)  
- [Technologies](#technologies)  
- [Diagram](#Diagram)  
- [Project Folder Structure](#project-folder-structure)  
  
## Team members: 
- Muhammad Sarahni    
- Adam Kaabiya    
- Najeeb Ibrahim    
- Maysa Zbidat    
- Aseel Khamis    
  
## Overview This web server powers the Bit Mentor Telegram bot. It receives a topic from the bot and dynamically generates questions and answers related to that topic, then sends them to the bot.     
  
## Technologies:   
The architecture for the Bit Mentor Telegram bot's web server consists of the following components:    
  
1. **FastAPI**: This serves as the web framework for the server, handling incoming requests from the Telegram bot and returning appropriate responses. I  
  
2. **MongoDB**: This NoSQL database is used to store and manage the questions and answers as well as user's score.    
  
3. **OpenAI API**: The OpenAI API is utilized to generate questions and answers dynamically. When the server receives a topic from the client, it uses the OpenAI API to create relevant trivia questions and answers.     
  
## Diagram   
![server](https://github.com/user-attachments/assets/528bf163-6b74-4fb5-904e-4ddae63b5d18)  
  
## Project Folder Structure:  
  
### MongoDB Folder  
- **`mongodb.py`**:  
  - **Class Definitions**: Contains MongoDB-related class for defining data schemas, managing collections, and handling connections to the MongoDB URI.  
  
- **`select_queries.py`**:  
  - Contains functions for ** retrieving data** based on specified criteria.  
  
- **`delete_queries.py`**:  
  - Contains functions or methods for **deleting documents** from MongoDB.  
  
- **`update_queries.py`**:  
  - Contains functions or methods for **updating existing documents** in MongoDB.  
  
- **`insert_queries.py`**:  
  - Contains functions or methods for **inserting new documents** into MongoDB.  
---  
  
### tests Folder  
The `tests` folder is dedicated to storing tests  for your application. Automated testing helps ensure that your   
  
---  
  
### server Folder  
  
The `server/` folder contains the core components of your server-side application, including the server setup, route controllers, and utility functions.   
  
  
- **`server.py`**:   
   The main entry point of the server application. This file typically contains the code to initialize and configure the server, such as setting up the web framework (FastAPI), defining middleware, and starting the server. -   
  
 - **`controllers/`**  
  Contains route handlers or controllers that define the endpoints for your application. Each file typically manages routes related to a specific aspect of the application.  
  
- **`utils/`**:   
Contains utility functions and helper methods that are used across different parts of the server application.  
such as :  
- open_ai.py: handles communication with open ai.  
  
  
env includes:  
- OPENAI_KEY = open ai key  
  
---  
This structure helps keep your data interaction code organized and separated by functionality, making it easier to maintain and scale your application.  
  
## Enviroment variables   
There needs to be an enviroment variable for the server link    
SERVER_URL="URL"    
- `MONGO_USERNAME`: Username for MongoDB Atlas.
- `MONGO_PASSWORD`: Password for MongoDB Atlas.
- `MONGO_CLUSTER_URL`: Cluster URL for MongoDB Atlas. 
## How to run  
  
In root directory, open terminal and run these commands    
```  
pip install -r requirements.txt  
python -m server.server  
```  
  
  
To run tests use this command    
```  
pytest  
```
---

## QuestDB
### Collections Overview:
**1. Questions Collection**
This collection stores individual questions with relevant details:

-   **Topic**: The subject of the question (e.g., Python).
-   **Difficulty**: The difficulty level of the question (e.g., easy).
-   **Question**: The text of the question.
-   **Options**: The possible answers to the question.
-   **Correct Answer Index**: The index of the correct answer in the options array.
-   **Explanation**: An explanation of the correct answer.
-   **Users Answered**: A list of users who have answered the question, with an indicator of whether their answer was correct.
```python
[
    {
        "topic": "python",
        "difficulty": "easy",
        "question": "What does the sum function in Python do?",
        "options": ["Adds all elements in a list", "Subtracts all elements in a list"],
        "correct_answer_idx": 0,
        "explanation": "The sum function adds all elements in an iterable.",
        "users_answered": [
            {"user_id": 123, "correct": True},
            {"user_id": 124, "correct": False}
        ]
    }
]

```
**2. Users Collection**

This collection stores data about individual users and their performance:

-   **tele_id**: Unique identifier for the user.
-   **Topics**: A nested structure containing performance metrics for different topics.
    -   **Difficulty**: Metrics for each difficulty level.
        -   **Questions Attempted**: Number of questions attempted.
        -   **Questions Correct**: Number of questions answered correctly.
```python
[
    {
        "tele_id": 123,
        "topics": {
            "python": {
                "difficulty": {
                    "easy": {
                        "questions_attempted": 10,
                        "questions_correct": 8
                    },
                    "medium": {
                        "questions_attempted": 5,
                        "questions_correct": 3
                    },
                    "hard": {
                        "questions_attempted": 2,
                        "questions_correct": 1
                    }
                }
            }
        }
    }
]

```

**3. Topic Collections**

This collection tracks statistics for each topic

-   **Topic**: The subject of the questions (e.g., Python).
-   **Difficulty**: metrics for each difficulty level.
    -   **Questions Attempted**: Total number of questions attempted.
    -   **Questions Correct**: Total number of questions answered correctly.

```python
[
    {
        "topic": "python",
        "difficulty": {
            "easy": {
                "questions_attempted": 50,
                "questions_correct": 40
            },
            "medium": {
                "questions_attempted": 30,
                "questions_correct": 20
            },
            "hard": {
                "questions_attempted": 20,
                "questions_correct": 10
            }
        },
        "questions_attempted": 100,
        "questions_correct": 70
    }
]

```

---
