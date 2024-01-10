# Imports
import unittest
import sys
from io import StringIO
from searchFunctions.programCode import programCodeSearch

"""
Unittest based python program to test compare Course Search result with expected result when given the Program Code.
Last Updated: 01/23/2022, by Lourenço Velez
"""

class TestCCSearches(unittest.TestCase):

    def test_cc_search_invalid(self):

        output = StringIO()
        sys.stdout = output
        
        # Call programcodesearch with CIS, then check it with expected output
        programCodeSearch("CIS")
        
        randomCourseCode = "CIS*4250 - Software Design V - 0.50"
        randomDescription = "This course is a study of data organization and data management principles with the perspective of analyzing applications suitable for implementation using a DBMS. This will include an analysis of several data base models, query specification methods, and query processing techniques. Overview of several related issues including concurrency control, security, integrity and recovery. Students will demonstrate concepts through project assignments."
        randomRestrictions = "Restricted to BCOMP.SENG majors."
        self.assertTrue(output.getvalue().find(randomCourseCode) != -1 and output.getvalue().find(randomDescription) != -1 and output.getvalue().find(randomRestrictions) != -1)

        # Reset stdout
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()