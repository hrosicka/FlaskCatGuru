# Cat Guru

![Python](https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Powered%20by-Flask-000000?logo=flask)
![MIT License](https://img.shields.io/badge/License-MIT-green.svg)
![Cat Facts API](https://img.shields.io/badge/API-Cat%20Facts-ffb347?logo=cat)
![Customize%20your%20Cat](https://img.shields.io/badge/Customize-your_Cat!-purple?logo=github)
![Not%20for%20dogs](https://img.shields.io/badge/Not%20for%20dogs-%F0%9F%90%B1-red)
![100% Catitude](https://img.shields.io/badge/100%25-Catitude-orange?logo=github)
![Zero%20Boring%20Webpages](https://img.shields.io/badge/Zero-Boring%20Webpages-blue?logo=smashingmagazine)

This is a simple Flask web application that provides cat wisdom and allows users to change the avatar and background color. Based on Cat Facts API: https://catfact.ninja/fact.

![](https://github.com/hrosicka/FlaskCatGuru/blob/master/doc/CatGuru1.png)

## Features

-   Displays a random cat avatar.
-   Provides a random cat fact as "wisdom" fetched from an external API.
-   Allows users to change the cat avatar.
-   Allows users to change the background color.
-   Logs application events and errors.

## Prerequisites

-   Python 3.6 or later
-   Flask
-   Requests

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  Install the required packages:

    ```bash
    pip install Flask requests
    ```

## Configuration

The application's configuration is stored in the `config.py` file.

-   `AVATARS`: A list of file paths to the cat avatar images.
-   `BACKGROUND_COLORS`: A list of background color hex codes.
-   `MAX_WISDOM_LINE_LENGTH`: The maximum length of a line in the wisdom text.
-   `LOG_FILE`: The path to the log file.

You can modify these values to customize the application.

## Running the Application

To run the application, execute the following command:

```bash
python app.py
