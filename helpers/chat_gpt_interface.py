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


print(ai_interface('if I give you a list of movies I like, can you advise me some different movie recommendations?'))
