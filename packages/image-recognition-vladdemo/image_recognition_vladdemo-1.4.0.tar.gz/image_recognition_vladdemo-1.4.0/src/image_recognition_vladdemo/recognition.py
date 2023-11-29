"""
This module contains main controller about gets text from image
"""

import os
from .image import Image
from .facade import ImageFacade


class Recognition:
    """
    A class for text recognition from an image using design patterns and a facade.

    Attributes:
        - image_path (str): The path to the image for text recognition.
        - image_package (Image): An instance of the Image class for image processing.
        - image_facade (ImageFacade): An instance of the ImageFacade class for using design patterns.

    Methods:
        - __init__(self, image_path): Initializes the Recognition class with the provided image path.
        - process_text_extraction(self, language='eng'): Processes text extraction from the image using a specified language.
    """

    def __init__(self, image_path):
        """
        Initializes the Recognition class with the provided image path.

        Args:
            - image_path (str): The path to the image for text recognition.
        """
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Image file not found at path: {image_path}")
        self.image_path = image_path
        self.image_package = Image()
        self.image_facade = ImageFacade(self.image_package)

    def process_text_extraction(self, language='eng'):
        """
        Processes text extraction from the image using a specified language.

        Args:
            - language (str): The language for text recognition (default is 'eng' for English).

        Returns:
            - extracted_text (str): The extracted text from the image.
        """
        extracted_text = self.image_facade.process_image(self.image_path, 'text', language)
        return extracted_text
