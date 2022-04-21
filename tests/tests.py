import unittest


class TestCase(unittest.TestCase):

    def test1(self):
        self.assertEqual(3, 3)


if __name__ == '__main__':
    unittest.main()