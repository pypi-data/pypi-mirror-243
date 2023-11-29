"""
This module about pattern Strategy for current staff
"""

import cv2
import pytesseract
from PIL import Image as PILImage


class ImageProcessingStrategy:
    """
    Base class for image processing with design pattern - Strategy.

    Methods:
        - process(self, image_path): Process an image based on the specific strategy.
    """

    def process(self, image_path):
        """
        Process an image based on the specific strategy.

        Args:
            - image_path (str): The path to the image to be processed.

        Returns:
            - The result of image processing based on the selected strategy.
        """
        pass


class TextExtractionStrategy(ImageProcessingStrategy):
    """
    Image processing strategy for text extraction.

    Methods:
        - process(self, image_path, language='eng'): Extract text from an image.
    """

    def process(self, image_path, language='eng'):
        """
        Extract text from an image.

        Args:
            - image_path (str): The path to the image to be processed.
            - language (str): The language for text recognition (default is 'eng' for English).

        Returns:
            - The extracted text from the image.
        """
        supported_languages = ['eng']
        if language not in supported_languages:
            raise ValueError(f"Unsupported language: {language}. Supported languages: {', '.join(supported_languages)}")
        image = PILImage.open(image_path)
        return pytesseract.image_to_string(image, lang=language)


class EdgeDetectionStrategy(ImageProcessingStrategy):
    """
    Image processing strategy for edge detection.

    Methods:
        - process(self, image_path): Detect edges in an image.
    """

    def process(self, image_path):
        """
        Detect edges in an image.

        Args:
            - image_path (str): The path to the image to be processed.

        Returns:
            - The image with detected edges.
        """
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_image, threshold1=30, threshold2=100)
        return edges
