from flask import Flask, render_template, jsonify, request
import requests
import random
import logging
import os
from config import AVATARS, BACKGROUND_COLORS, MAX_WISDOM_LINE_LENGTH, LOG_FILE

app = Flask(__name__)

logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

avatar_cache = {}
CAT_FACT_URL = "https://catfact.ninja/fact"  # Constant for the cat fact API URL

def get_cat_fact():
    """
    Fetches a random cat fact from the cat fact API.

    Returns:
        str: A string containing the cat fact, or an error message if fetching fails.
    """
    try:
        response = requests.get(CAT_FACT_URL)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        cat_fact_data = response.json()
        if "fact" in cat_fact_data:
            return cat_fact_data["fact"]
        else:
            logging.error("Cat fact API response missing 'fact' key.")
            return "Meow! Cat wisdom unavailable."  # Fallback message in English
    except requests.exceptions.ConnectionError as e:
        error_message = "Failed to connect to the server. Please check your internet connection."  # Error message in English
        logging.error(error_message)
        return error_message
    except requests.exceptions.Timeout as e:
        error_message = "Request timed out. Please try again later."  # Error message in English
        logging.error(error_message)
        return error_message
    except requests.exceptions.RequestException as e:
        error_message = f"An unexpected error occurred during the request: {e}"  # Error message in English
        logging.error(error_message)
        return error_message

def format_wisdom(wisdom_text):
    """
    Formats the wisdom text into lines with a maximum length.

    Args:
        wisdom_text (str): The raw wisdom text.

    Returns:
        str: The formatted wisdom text with line breaks.
    """
    lines = []
    for word in wisdom_text.split():
        if lines and len(" ".join(lines[-1:])) + len(word) + 1 > MAX_WISDOM_LINE_LENGTH:
            lines.append(word)
        elif not lines:
            lines.append(word)
        else:
            lines[-1] += f" {word}"
    return "\n".join(lines)

@app.route('/')
def index():
    """
    Renders the main page with a random avatar and background color.
    """
    avatar = random.choice(AVATARS)  # Choose a random avatar from the list
    background_color = random.choice(BACKGROUND_COLORS)  # Choose a random background color from the list
    return render_template('index.html', avatar=avatar, background_color=background_color)

@app.route('/wisdom', methods=['GET'])
def get_wisdom():
    """
    Handles GET requests to retrieve and format a piece of cat wisdom.

    Returns:
        jsonify: A JSON response containing the formatted wisdom.
    """
    wisdom = get_cat_fact()
    formatted_wisdom = format_wisdom(wisdom)
    return jsonify({'wisdom': formatted_wisdom})

@app.route('/change_avatar', methods=['POST'])
def change_avatar():
    """
    Handles POST requests to change the cat avatar.

    Returns:
        jsonify: A JSON response containing the new avatar path,
                 or an error if the current avatar is not found.
    """
    data = request.get_json()
    current_avatar = data.get('current_avatar')
    if not current_avatar:
        return jsonify({'error': 'Missing current_avatar'}), 400

    try:
        current_filename = os.path.basename(current_avatar)
        current_index = [os.path.basename(a) for a in AVATARS].index(current_filename)
        new_index = (current_index + 1) % len(AVATARS)
        new_avatar = AVATARS[new_index]
        return jsonify({'new_avatar': new_avatar})
    except ValueError:
        return jsonify({'error': 'Avatar not found'}), 400

@app.route('/change_background', methods=['POST'])
def change_background():
    """
    Handles POST requests to change the background color.

    Returns:
        jsonify: A JSON response containing the new background color,
                 or an error if the current color is not found.
    """
    data = request.get_json()
    current_color = data.get('current_color')
    if not current_color:
        return jsonify({'error': 'Missing current_color'}), 400

    try:
        current_index = BACKGROUND_COLORS.index(current_color)
        new_index = (current_index + 1) % len(BACKGROUND_COLORS)
        new_color = BACKGROUND_COLORS[new_index]
        return jsonify({'new_color': new_color})
    except ValueError:
        return jsonify({'error': 'Color not found'}), 400

if __name__ == '__main__':
    app.run(debug=True)