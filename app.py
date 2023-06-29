from flask import Flask
from data_manager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('data/data.json')


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


if __name__ == '__main__':
    app.run(debug=True)
