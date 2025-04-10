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
cat_fact_url = "https://catfact.ninja/fact"

def get_cat_fact():
    try:
        response = requests.get(cat_fact_url)
        response.raise_for_status()
        cat_fact_data = response.json()
        return cat_fact_data["fact"]
    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.exceptions.ConnectionError):
            error_message = "Failed to connect to the server. Please check your internet connection."
        elif isinstance(e, requests.exceptions.Timeout):
            error_message = "Request timed out. Please try again later."
        else:
            error_message = f"An unexpected error occurred: {str(e)}"
        logging.error(error_message)
        return error_message

def format_wisdom(wisdom_text):
    lines = []
    for word in wisdom_text.split():
        if lines:
            if len(" ".join(lines[-1:])) + len(word) > MAX_WISDOM_LINE_LENGTH:
                lines.append("")
        else:
            lines.append("")
        lines[-1] += " " + word
    return "\n".join(lines)

@app.route('/')
def index():
    avatar_index = random.randint(0, len(AVATARS) - 1)
    background_color_index = random.randint(0, len(BACKGROUND_COLORS) - 1)
    return render_template('index.html',
                           avatar=AVATARS[avatar_index],
                           background_color=BACKGROUND_COLORS[background_color_index])

@app.route('/wisdom', methods=['GET'])
def get_wisdom():
    wisdom_text = get_cat_fact()
    formatted_wisdom = format_wisdom(wisdom_text)
    return jsonify({'wisdom': formatted_wisdom})

@app.route('/change_avatar', methods=['POST'])
def change_avatar():
    current_avatar = request.json.get('current_avatar')
    current_filename = os.path.basename(current_avatar)
    avatar_filenames = [os.path.basename(avatar) for avatar in AVATARS]
    try:
        current_index = avatar_filenames.index(current_filename)
    except ValueError:
        return jsonify({'error': 'Avatar not found'}), 400
    new_index = (current_index + 1) % len(AVATARS)
    new_avatar = AVATARS[new_index]
    return jsonify({'new_avatar': new_avatar})

@app.route('/change_background', methods=['POST'])
def change_background():
    current_color = request.json.get('current_color')
    current_index = BACKGROUND_COLORS.index(current_color)
    new_index = (current_index + 1) % len(BACKGROUND_COLORS)
    new_color = BACKGROUND_COLORS[new_index]
    return jsonify({'new_color': new_color})

if __name__ == '__main__':
    app.run(debug=True)