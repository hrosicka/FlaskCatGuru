# Cat Guru

This is a simple Flask web application that provides cat wisdom and allows users to change the avatar and background color.

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
