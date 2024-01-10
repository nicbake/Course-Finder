# Imports
import unittest
import sys
from io import StringIO
from searchFunctions.courseWeightSeason import courseWS

"""
Unittest based python program to test compare Course Search result with expected result when given Course Weight and Season.
Last Updated: 01/23/2022, by Lourenço Velez
"""

class TestWeightSeasonSearch(unittest.TestCase):   

    def test_course_quarter_credit_fall(self):

        output = StringIO()
        sys.stdout = output

        courseWS('0.25', 'F')

        courseOne = "MUSC*2550"
        courseTwo = "ZOO*3610 - Lab Studies in Animal Physiology I - F"
        self.assertTrue(output.getvalue().find(courseOne) != -1 and output.getvalue().find(courseTwo) != -1, output.getvalue())

        # Reset stdout
        sys.stdout = sys.__stdout__

    def test_course_half_credit_summer(self):

        output = StringIO()
        sys.stdout = output

        courseWS('0.50', 'S')

        courseOne = "ANTH*4890 - Special Projects in Anthropology - SFW"
        courseTwo = "COOP*5000 - Co-op Work Term V - SFW"
        self.assertTrue(output.getvalue().find(courseOne) != -1 and output.getvalue().find(courseTwo) != -1)
        sys.stdout = sys.__stdout__

    def test_course_credit_default(self):

        output = StringIO()
        sys.stdout = output

        courseWS('0.50', 'ALL')
        
        courseOne = "ECON*1050 - Introductory Microeconomics - SFW"
        courseTwo = "WMST*2000 - Women and Representation - W"
        courseThree = "ANTH*4890 - Special Projects in Anthropology - SFW"
        courseFour = "COOP*5000 - Co-op Work Term V - SFW"
        self.assertTrue(output.getvalue().find(courseOne) != -1 and output.getvalue().find(courseTwo) != -1 and output.getvalue().find(courseThree) != -1 and output.getvalue().find(courseFour) != -1, output.getvalue())

        # Reset stdout
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()