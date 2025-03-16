import os

dirname = os.path.dirname(__file__)
AVATARS = [os.path.join(dirname, 'static/avatars/', f'cat{i}.jpg') for i in range(1, 9)]
BACKGROUND_COLORS = [ '#e0e0e0', '#d1c4e9', '#ffe0b2']
MAX_WISDOM_LINE_LENGTH = 50
LOG_FILE = 'cat_guru.log'
