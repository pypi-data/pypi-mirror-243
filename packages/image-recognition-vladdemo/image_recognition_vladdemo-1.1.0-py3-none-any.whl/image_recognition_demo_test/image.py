"""
This module contains main class for model Image
"""

from PIL import Image as PILImage

from singleton import SingletonMeta
from strategy import TextExtractionStrategy, EdgeDetectionStrategy


class Image(metaclass=SingletonMeta):
    """
    Class for processing images and text recognition using design pattern - Singleton
    """

    def __new__(cls):
        """
        Creates a single instance of the Image class.

        Returns:
            - Image: The single instance of the class.
        """
        try:
            cls._instance = super(Image, cls).__new__(cls)
            cls._instance.init_package()

        except Exception as e:
            print(f"Error while creating Image instance: {e}")

        return cls._instance

    def init_package(self):
        """
        Initializes the package and image processing strategies.
        """
        self.text_extraction_strategy = TextExtractionStrategy()
        self.edge_detection_strategy = EdgeDetectionStrategy()

    def process_image(self, image_path, strategy_type, language):
        """
        Processes an image according to the selected strategy.

        Args:
            - image_path (str): The path to the image to be processed.
            - strategy_type (str): The type of image processing strategy ('text' or 'edge').
            - language (str): Language code like 'eng' for define corresponding text

        Returns:
            - The result of image processing according to the selected strategy.
        """
        if strategy_type == 'text':
            return self.text_extraction_strategy.process(image_path, language)
        elif strategy_type == 'edge':
            return self.edge_detection_strategy.process(image_path)
