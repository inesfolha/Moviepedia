import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('X_RAPID_API_KEY')
URL = "https://chatgpt-best-price.p.rapidapi.com/v1/chat/completions"


def ai_interface(question):
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "chatgpt-best-price.p.rapidapi.com"
    }

    response = requests.post(URL, json=payload, headers=headers)
    json_response = response.json()
    answer = json_response['choices'][0]['message']['content']
    return answer


def ai_prompt(username, movies_list):
    query = f""" Hey! My name is {username}. 
    
    You are now a movie expert, 
    and I need you to take a look at my list of favorite 
    movies and recommend me 1 to 3 movies to watch this weekend, that are not in my list.
    
    These are some movies I like {movies_list}, whatever you recommend me, 
    please include a small synopsis of the movie so I know what is it about.  
    
    Please start your answer with a headline that greets me and addresses to my name!
    
    Since I will receive your response in a html template, I kindly ask you to format your 
    response in HTML format, if possible, please use this font "Lucida Console", "Courier New", monospace.
    and this color for the title: #1f1f2e, the rest of the text may be this color #1f1f2e """
    return query


def ai_welcome(username):
    query = f""" Hey!

    You are now a movie app owner.
    
    The user {username}, just signed up for your website, Moviepedia, where he can add all his favorite 
    movies to his personal list and even leave reviews!Please welcome this new user.
    
    Please start your answer with a headline that greets the user!

    Since the user will receive your response in a html template, I kindly ask you to format your 
    response in HTML format, if possible, please use this font "Lucida Console", "Courier New", monospace.
    and this color for the title: #1f1f2e, the rest of the text may be this color #1f1f2e """
    return query

