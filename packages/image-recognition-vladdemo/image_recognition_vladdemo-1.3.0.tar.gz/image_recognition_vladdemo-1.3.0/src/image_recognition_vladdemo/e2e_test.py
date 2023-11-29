"""
Main e2e test for current package
"""

import unittest
from main import ImageRecognition


class TestImageRecognitionE2E(unittest.TestCase):
    """
    Main e2e test for full process of get text from photo
    """

    def test_image_recognition(self):
        """
        Main e2e test about text extraction
        """
        image_path = 'new.png'
        language = 'eng'

        recognition = ImageRecognition(image_path, language)

        extracted_text = recognition.get_text_from_photo()

        self.assertIn('HOW TO ACCESS IMAGES WITHOUT ALT TEXT', extracted_text)


if __name__ == '__main__':
    unittest.main()
