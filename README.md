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

## Overview  
This web server powers the Bit Mentor Telegram bot. It receives a topic from the bot and dynamically generates questions and answers related to that topic, then sends them to the bot.   

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

### setting Folder
The `setting/` folder contains configuration files.
- **`config.py`**: 
dynamically loads environment-specific settings such as database credentials and API keys based on the provided environment argument (dev or prod).

---
This structure helps keep your data interaction code organized and separated by functionality, making it easier to maintain and scale your application.

## Enviroment variables  
These files should be located in the root directory of your project
* .env_dev For Dev

- `SERVER_URL_DEV`: Url of server.
- `MONGO_USERNAME_DEV`: Username for MongoDB Atlas.
- `MONGO_PASSWORD_DEV`: Password for MongoDB Atlas.
- `MONGO_CLUSTER_DEV`: Cluster URL for MongoDB Atlas. 
- `OPENAI_KEY_DEV`: API key for OpenAI services.
* .env_prod For Prod

- `SERVER_URL_PROD`: Url of server.
- `MONGO_USERNAME_PROD`: Username for MongoDB Atlas.
- `MONGO_PASSWORD_PROD`: Password for MongoDB Atlas.
- `MONGO_CLUSTER_PROD`: Cluster URL for MongoDB Atlas. 
- `OPENAI_KEY_PROD`: API key for OpenAI services.
## How to Run      
 In the root directory, open terminal and run these commands:        
1.Install the required packages:    

``` pip install -r requirements.txt ```

 2.Run the server    
* for Development    
``` 
python -m server.server --env dev 
 ``` 
 * or simply:    
``` 
python -m server.server  
 ```
 * for Production:    
``` 
python -m server.server --env prod
 ``` 

To run tests use this command      
``` pytest ```
