import unittest
from AI import softmax

class TestAIMethods(unittest.TestCase):
    """
    Examples:

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    """
    
    def test_softmax(self):
        # sum of lists should sum to 1
        self.assertEqual(sum(softmax([2,3])), 1)
        self.assertEqual(sum(softmax([0.2, 0.3, 0.7])), 1)

if __name__ == '__main__':
    unittest.main()