import json
import csv


def load_json_data(file_path):
    """Loads a JSON file and returns the parsed data."""
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while loading JSON data from '{file_path}'.")
        print(f"Error message: {str(e)}")


def load_csv(file_path):
    """Loads a CSV file and returns the data as a list of rows."""
    try:
        data = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred while loading CSV data from '{file_path}'.")
        print(f"Error message: {str(e)}")


def save_csv(filename, data_to_save):
    """Saves the data as a CSV file with the given filename."""
    try:
        with open(filename, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data_to_save)
        return filename
    except Exception as e:
        print(f"An error occurred while saving CSV data to '{filename}'.")
        print(f"Error message: {str(e)}")


def load_document(file):
    """Loads the content of a file and returns it as a string."""
    try:
        with open(file, "r") as file:
            file_data = file.read()
        return file_data
    except FileNotFoundError:
        print(f"File '{file}' not found.")
    except Exception as e:
        print(f"An error occurred while loading document from '{file}'.")
        print(f"Error message: {str(e)}")


def save_json_file(filename, data_to_save):
    """Creates a new JSON file with the given filename and writes the provided content to it."""
    try:
        with open(filename, 'w') as f:
            json.dump(data_to_save, f)
        return filename
    except Exception as e:
        print(f"An error occurred while saving JSON data to '{filename}'.")
        print(f"Error message: {str(e)}")


def save_html(filename, data_to_save):
    """Creates a new HTML file with the given filename and writes the provided content to it."""
    try:
        with open(filename, 'w') as f:
            f.write(data_to_save)
        return filename
    except Exception as e:
        print(f"An error occurred while saving HTML data to '{filename}'.")
        print(f"Error message: {str(e)}")
