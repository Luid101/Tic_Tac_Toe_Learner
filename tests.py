import unittest
from AI import softmax
from functions import *

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


    def test_convert_to_lst(self):
        # the result should be a 2d list version of the dictionary
        self.assertEqual( \
                    convert_to_list({'hello':1,'goodbye':2}).sort(), \
                    ([['hello', 1], ['goodbye',2]]).sort() \
                    )
        self.assertEqual(convert_to_list({}), [])
    
    def test_positize_values(self):
        self.assertEqual(positize_values([-1, 1, -8]), [7, 9, 0])
        self.assertEqual(positize_values([1, 1, 8]), [1, 1, 8])

if __name__ == '__main__':
    unittest.main()