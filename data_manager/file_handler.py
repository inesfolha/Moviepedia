import json
import csv


def load_json_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def load_csv(file_path):
    """loads a csv into a dict"""
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data


def save_csv(filename, data_to_save):
    """loads a csv into a dict"""
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data_to_save)
    return filename


def load_document(file):
    """loads the content of a  file"""
    with open(file, "r") as file:
        file_data = file.read()
        return file_data


def save_json_file(filename, data_to_save):
    """Creates a new json file with the given file name and writes the provided content to it."""
    try:
        with open(filename, 'w') as f:
            json.dump(data_to_save, f)
            return filename

    except Exception as e:
        print('An unexpected error occurred while saving movie. Please try again later.')
        print(f'Error message: {str(e)}')


def save_html(filename, data_to_save):
    """Creates a new HTML file with the given file name and writes the provided content to it."""
    with open(filename, 'w') as f:
        f.write(data_to_save)
    return f
