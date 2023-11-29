"""
This module about pattern Facade for current staff
"""


class ImageFacade:
    """
    This class about design pattern - Facade
    """

    def __init__(self, package):
        """
        Initializing thi starter package
        """
        self.package = package

    def process_image(self, image_path, strategy_type, language):
        """
        Processing images depending on the chosen strategy

        Args:
            - image_path (str): path to current image.
            - strategy_type (str): type of strategy
            - language (str): language code

        Returns:
            - The result of image processing depending on the chosen strategy        
        """
        return self.package.process_image(image_path, strategy_type, language)
