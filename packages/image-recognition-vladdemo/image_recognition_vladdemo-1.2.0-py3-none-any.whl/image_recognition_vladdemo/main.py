"""
This module contains simple function for test
"""

from recognition import Recognition


class ImageRecognition:
    """
    A class for image recognition that extracts text from an image using the Recognition class.

    Attributes:
        - image_path (str): The path to the image for text recognition.
        - language (str): The language for text recognition (default is 'eng' for English).

    Methods:
        - __init__(self, image_path, language='eng'): Initializes the ImageRecognition class 
            with the provided image path and language.
        - get_text_from_photo(self): Retrieves text from the image using text recognition.
    """

    def __new__(cls, *args, **kwargs):
        """
        Create new image obj for get text
        Args:
            *args: image path [0] and language [1]
            **kwargs: image path and language
        """
        image_path = ""
        if args:
            image_path = args[0]
        if kwargs:
            image_path = kwargs['image_path']

        if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValueError("Unsupported image format. Only PNG and JPEG are supported.")

        return super(ImageRecognition, cls).__new__(cls)

    def __init__(self, image_path, language='eng') -> None:
        """
        Initializes the ImageRecognition class with the provided image path and language.

        Args:
            - image_path (str): The path to the image for text recognition.
            - language (str): The language for text recognition (default is 'eng' for English).
        """
        self.image_path = image_path
        self.language = language

    def get_text_from_photo(self):
        """
        Retrieves text from the image using text recognition.

        Returns:
            - extracted_text (str): The extracted text from the image.
        """
        recognition = Recognition(self.image_path)
        extracted_text = recognition.process_text_extraction(self.language)

        cleaned_text = extracted_text.replace('\n', ' ').replace('\x0c', '').rstrip()
        return cleaned_text
    

if __name__ == '__main__':
    pass
    # text = ImageRecognition(image_path='new.png', language='eng').get_text_from_photo()
    # print(text)
