"""
sample test
"""

from django.test import SimpleTestCase

from app import calc

class CalTest(SimpleTestCase):
    #test the calc module

    def test_add(self):
        #test adding numbers together
        res = calc.add(100, 150)
        self.assertEqual(res, 250)

    def test_substracting_numbers(self):
        #test substracting numbers
        res = calc.substract(200, 150)
        self.assertEqual(res, 50)
