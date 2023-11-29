"""
Main integration tests for current package
"""

import unittest
from main import ImageRecognition


class TestImageRecognitionIntegration(unittest.TestCase):
    """
    Main class about integration tests in package
    """

    def test_text_extraction_english(self):
        """
        Check about extraction text in eng
        """
        image_path = 'edit.jpg'
        language = 'eng'

        recognition = ImageRecognition(image_path, language)
        extracted_text = recognition.get_text_from_photo()
        self.assertTrue(extracted_text.strip(), "Edit Recordings")


if __name__ == '__main__':
    unittest.main()
