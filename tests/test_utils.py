import unittest
from src.utils import load_document

class TestUtils(unittest.TestCase):

    def test_load_document(self):
        document_path = 'data/sample_documents/document1.pdf'
        content = load_document(document_path)
        self.assertIsInstance(content, str)

if __name__ == '__main__':
    unittest.main()
