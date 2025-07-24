import unittest

import publish

class TestPublish(unittest.TestCase):
    def test_extract_title(self):
        md = "# Happy "
        title = publish.extract_title(md)
        self.assertEqual(title, "Happy")
        md = """
# Happy 

There is a title"""  # .strip()
        title = publish.extract_title(md)
        self.assertEqual(title, "Happy")