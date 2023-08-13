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
    movies and recommend me 1 to 3 movies to watch this weekend.
    
    These are some movies I like {movies_list}, whatever you recomend me, 
    please include a small synopsis of the movie so I know what is it about.
    
    Please do not recommend movies that are on the list, as I have already seen them! 
    
    Please start your answer greeting me and use my name!
    
    Since I will receive your response in a html template, I kindly ask you to format your 
    response in HTML format, if possible, please use this font "Lucida Console", "Courier New", monospace.
    and this color for the title #1f1f2e, the rest of the text may be  #1f1f2e """

    return query
