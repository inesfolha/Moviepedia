# MoviePedia  <img src="https://github.com/inesfolha/movie_web_app/blob/main/static/icon.png?raw=true" alt="Logo Title" width="40" />

<p id="top"></p>

## Introduction                                     
Welcome to MoviePedia, an innovative movie web application that allows users to create and manage their favorite movies, leave reviews, and receive movie recommendations powered by AI!

This README provides an overview of the project's structure, features, and installation instructions.


## Table of Contents
- [Introduction](#introduction)
- [Description](#description)
  - [Project Structure](#project-structure)
  - [App Features](#app-features)
  - [API Integration](#api-integration)
  - [Error Handling](#error-handling)
- [Deployment](#deployment)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
- [How does it work?](#how-does-it-work)
  - [Watch demo](https://www.youtube.com/watch?v=kAIS983QBS8)
- [Limitations](#limitations)
- [Contributions](#contributions)
- [Contact Information](#contact-information)

[Back to the Top](#top)

## Description

### Project Structure
The MoviePedia project is structured as follows:
```
├── .data
├── .data_manager
├── .helpers
├── .routes
├── .static
├── .templates
├── .env
├── app.py
├── readme.md
├── requirements.txt
```
- `.data`: Contains the SQLite database file (`movie_web_app.sqlite3`) and other data files from older versions.


- `.data_manager`: Includes data management modules for handling user data and queries.


- `.helpers`: Helper modules, including authentication, ChatGPT integration, and more.


- `.routes`: Routing modules for API endpoints and email handling.


- `.static`: CSS files and image/icon assets.


- `.templates`: HTML templates for web pages.


- `.env`: Configuration file for environment variables.


- `app.py`: The main application file that connects routes and manages error handling.


[Back to the Top](#top)
### App Features

MoviePedia offers a range of features, including:
- User authentication with Flask-Login.
- Create, edit, and delete user-specific movie lists.
- Detailed movie information retrieval using the OMDB API.
- Leave reviews for movies and like other users' reviews.
- User settings for password changes and account deletion.
- AI integration to receive personalized movie recommendations via email.
- Welcome email and password recovery functionality.
- Future friend list feature planned for implementation.


[Back to the Top](#top)

### API Integration

MoviePedia seamlessly integrates the following APIs:

#### OMDB API
The [OMDB API](https://www.omdbapi.com/) is utilized to fetch detailed information about movies. When a user adds a movie to their list, MoviePedia queries the OMDB API to retrieve data such as movie title, director, release year, and rating. This information is then displayed in the user's profile grid.

#### Elasticmail API
The [Elasticmail API](https://app.elasticemail.com/api/login) is used to facilitate email functionality within MoviePedia. It handles various email-related tasks, including:
  - Sending a welcome email to new users upon registration, provided by chat GPT.
  - Sending a temporary code to users who have forgotten their passwords for password recovery.
  - Sending movie recommendations emails written by chat GPT.

#### ChatGPT Integration
MoviePedia leverages [ChatGPT's](https://rapidapi.com/truongvuhung102/api/chatgpt-best-price) capabilities to provide movie recommendations, as well as to write personalized welcome emails for each new user.

By clicking a button in the app, users can request personalized movie suggestions. ChatGPT receives the user's list of favorite movies and responds with tailored recommendations, enhancing the user's movie-watching experience.

Please note that while these API integrations are functional and enhance the user experience, they are based on free API plans and may have limitations as the website's user base grows. Consider upgrading to paid API plans or exploring alternative solutions if necessary.


### Error Handling
Robust error handling is implemented throughout the application to ensure a smooth user experience. Detailed error messages and templates are provided to guide users in case of issues.

## Deployment


MoviePedia is currently hosted on [PythonAnywhere](https://www.pythonanywhere.com/), and you can access the live version of the application at [https://moviepedia.pythonanywhere.com/](https://moviepedia.pythonanywhere.com/).

[Back to the Top](#top)
## Installation

### Prerequisites

To run this project, you'll need Python 3 and the following dependencies:

- Flask
- Dotenv (for environment variable management)
- Required Python packages (listed in requirements.txt)


### Installation Steps

1. Clone this repository or download the script file:

```bash
git clone https://github.com/inesfolha/movie_web_app.git
```
If you downloaded a ZIP archive, extract its contents to a directory of your choice.

2. Change to the script's directory:

 ```bash
  cd movie_web_app
```

3. Install the required dependencies:
 ```bash
  pip install -r requirements.txt
```

4. Create a .env file in the project directory and add the following variables:
 ```bash
DATABASE=<your_database_uri>
SECRETKEY=<your_secret_key>
X_RAPID_API_KEY=<your_api_key>
API_KEY=<your_omdbapi_key>
ELASTICMAILAPIKEY=<your_elasticmail_api_key>
```
5. To run the script, open your terminal and execute the following command:
```bash
python app.py
```
The application will be accessible at http://localhost:5000 by default.

[Back to the Top](#top)

## How does it work?
For a visual demonstration of how MoviePedia works, you can watch a demo here:

 * [Watch Demo](https://www.youtube.com/watch?v=kAIS983QBS8)


## Limitations
- MoviePedia relies on free APIs, and as the user base grows, these APIs may become limited or require upgrading to paid versions.


- Features that require requests to the email API and chat GPT still require further optimization as they are currently a bit slow. 


- Since emails are sent with a free API, usually emails end up in the spam box. 

[Back to the Top](#top)


## Contributions

Contributions to this project are welcome. If you'd like to contribute, please fork the repository, make your changes, and create a pull request.

Thank you for exploring MoviePedia! We hope you enjoy using it as much as we enjoyed creating it.

[Back to the Top](#top)

## Contact Information
For inquiries or support, please contact `moviepedia.app@gmail.com`.

[Back to the Top](#top)