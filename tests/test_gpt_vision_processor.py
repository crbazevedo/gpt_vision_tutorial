import unittest
from src.gpt_vision_processor import process_document

class TestGPTVisionProcessor(unittest.TestCase):

    def test_process_document(self):
        sample_content = "This is a sample document content."
        result = process_document(sample_content)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
