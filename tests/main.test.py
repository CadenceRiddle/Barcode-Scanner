import unittest
from src import hello

class TestSample(unittest.TestCase):
    def test_function(self):
        self.assertEqual(hello(), 'hello world')

if __name__ == '__main__':
    unittest.main()