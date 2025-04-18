import unittest
from unittest.mock import patch, MagicMock
import sys
import json
import requests

# Add the project path to the system path to allow importing the 'app' module
sys.path.append('../FlaskCatguru')
from app import app, get_cat_fact, format_wisdom, AVATARS, BACKGROUND_COLORS

class FlaskCatGuruTests(unittest.TestCase):
    """
    A test suite for the FlaskCatguru application.
    It includes unit tests for various parts of the application,
    such as API calls, text formatting, and route handling.
    """

    def setUp(self):
        """
        Set up method called before each test. Initializes the testing environment.
        Creates a test client for the Flask application and sets the testing flag.
        """
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.requests.get')
    def test_get_cat_fact_success(self, mock_get):
        """
        Tests the successful retrieval of a cat fact from the API.
        Mocks the `requests.get` call to prevent actual HTTP requests.
        Verifies that the returned value is the expected cat fact.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {'fact': 'Cats are awesome!'}
        mock_response.raise_for_status = MagicMock()  # Simulate a successful HTTP status code
        mock_get.return_value = mock_response

        fact = get_cat_fact()
        self.assertEqual(fact, 'Cats are awesome!')

    @patch('app.requests.get')
    def test_get_cat_fact_missing_key(self, mock_get):
        """
        Tests the scenario where the API response is missing the expected 'fact' key.
        Verifies that the function returns the default message indicating unavailability of wisdom.
        """
        mock_response = MagicMock()
        mock_response.json.return_value = {'not_a_fact': 'Something else'}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        fact = get_cat_fact()
        self.assertEqual(fact, 'Meow! Cat wisdom unavailable.')

    @patch('app.requests.get')
    def test_get_cat_fact_connection_error(self, mock_get):
        """
        Tests the scenario where a connection error occurs during the API call.
        Mocks `requests.get` to raise a `requests.exceptions.ConnectionError` exception.
        Verifies that the function returns the appropriate error message.
        """
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        fact = get_cat_fact()
        self.assertEqual(fact, 'Failed to connect to the server. Please check your internet connection.')

    @patch('app.requests.get')
    def test_get_cat_fact_timeout_error(self, mock_get):
        """
        Tests the scenario where the API call times out.
        Mocks `requests.get` to raise a `requests.exceptions.Timeout` exception.
        Verifies that the function returns the appropriate error message.
        """
        mock_get.side_effect = requests.exceptions.Timeout("Timeout error")

        fact = get_cat_fact()
        self.assertEqual(fact, 'Request timed out. Please try again later.')

    @patch('app.requests.get')
    def test_get_cat_fact_request_exception(self, mock_get):
        """
        Tests a general request error during the API call.
        Mocks `requests.get` to raise a generic `requests.exceptions.RequestException`.
        Verifies that the returned error message includes information about the error.
        """
        mock_get.side_effect = requests.exceptions.RequestException("Generic request error")

        fact = get_cat_fact()
        self.assertIn('An unexpected error occurred during the request', fact)

    def test_format_wisdom_short_text(self):
        """
        Tests formatting a short wisdom text that should not be split into multiple lines.
        Verifies that the formatted text is the same as the original.
        """
        text = "Short wisdom."
        formatted = format_wisdom(text)
        self.assertEqual(formatted, "Short wisdom.")

    def test_format_wisdom_long_text(self):
        """
        Tests formatting a long wisdom text that should be split into multiple lines.
        Verifies that the resulting text has more than one line and that the length of each line
        does not exceed the assumed maximum line length.
        """
        text = "This is a long wisdom text that needs to be split into multiple lines because it exceeds the maximum allowed length for a single line of wisdom."
        formatted = format_wisdom(text)
        lines = formatted.split('\n')
        self.assertTrue(len(lines) > 1)
        for line in lines:
            self.assertLessEqual(len(line), 50) # Assuming MAX_WISDOM_LINE_LENGTH is around 50

    def test_index_route(self):
        """
        Tests the response of the main page ('/').
        Verifies that the HTTP status code is 200 (OK) and that the response contains the keywords 'avatar' and 'background-color'.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'avatar', response.data)
        self.assertIn(b'background-color', response.data)

    @patch('app.get_cat_fact', return_value="Cats are great!")
    def test_get_wisdom_route(self, mock_get_cat_fact):
        """
        Tests the response of the '/wisdom' route.
        Mocks the `get_cat_fact` function to ensure a predictable response.
        Verifies that the HTTP status code is 200, the content type is JSON, and that the JSON response
        contains the expected wisdom. Also verifies that the mocked function was called.
        """
        response = self.app.get('/wisdom')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['wisdom'], 'Cats are great!')
        mock_get_cat_fact.assert_called_once()

    @patch('app.random.choice', side_effect=[AVATARS[0], BACKGROUND_COLORS[0]])
    def test_index_route_content(self, mock_random_choice):
        """
        Tests the content of the main page ('/'), specifically the presence of a selected avatar and background color.
        Mocks `random.choice` to ensure the first elements from the AVATARS and BACKGROUND_COLORS lists are selected.
        Verifies that these values are present in the response data.
        """
        response = self.app.get('/')
        self.assertIn(AVATARS[0].encode('utf-8'), response.data)
        self.assertIn(BACKGROUND_COLORS[0].encode('utf-8'), response.data)

    def test_change_avatar_route_success(self):
        """
        Tests the successful changing of the avatar via a POST request to '/change_avatar'.
        Sends the current avatar in the JSON data and verifies that the response contains the new avatar
        (the next one in the AVATARS list).
        """
        initial_avatar = AVATARS[0]
        response = self.app.post('/change_avatar', json={'current_avatar': initial_avatar})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['new_avatar'], AVATARS[1])

    def test_change_avatar_route_missing_data(self):
        """
        Tests the scenario where the 'current_avatar' key is missing in the POST request to '/change_avatar'.
        Verifies that the server returns a 400 (Bad Request) status code and an error message.
        """
        response = self.app.post('/change_avatar', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Missing current_avatar')

    def test_change_avatar_route_avatar_not_found(self):
        """
        Tests the scenario where a non-existent avatar is sent in the POST request to '/change_avatar'.
        Verifies that the server returns a 400 status code and the error message 'Avatar not found'.
        """
        response = self.app.post('/change_avatar', json={'current_avatar': 'nonexistent_avatar.png'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Avatar not found')

    def test_change_background_route_success(self):
        """
        Tests the successful changing of the background color via a POST request to '/change_background'.
        Sends the current color in the JSON data and verifies that the response contains the new color
        (the next one in the BACKGROUND_COLORS list).
        """
        initial_color = BACKGROUND_COLORS[0]
        response = self.app.post('/change_background', json={'current_color': initial_color})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['new_color'], BACKGROUND_COLORS[1])

    def test_change_background_route_missing_data(self):
        """
        Tests the scenario where the 'current_color' key is missing in the POST request to '/change_background'.
        Verifies that the server returns a 400 status code and an error message.
        """
        response = self.app.post('/change_background', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Missing current_color')

    def test_change_background_route_color_not_found(self):
        """
        Tests the scenario where a non-existent color is sent in the POST request to '/change_background'.
        Verifies that the server returns a 400 status code and the error message 'Color not found'.
        """
        response = self.app.post('/change_background', json={'current_color': 'nonexistent_color'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Color not found')

if __name__ == '__main__':
    unittest.main()