import os
from typing import Any

import pygame


class Setting():
    WINDOW = pygame.rect.Rect((0, 0), (700, 700))
    FPS = 60
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")