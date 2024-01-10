# Imports
import unittest
import sys
from io import StringIO
from searchFunctions.courseCode import courseCodeSearch

"""
Unittest based python program to compare Course Search result with expected result when given the Course Code.
Last Updated: 01/23/2022, by Lourenço Velez
"""

class TestCCSearches(unittest.TestCase):
    # This function revolves around tests dealing with Course Code search, A test of an existing course, a bad input, and a non-existent code
    def test_cc_search(self): 

        output = StringIO()
        sys.stdout = output

        courseCodeSearch("ACCT*1220")

        # Information about Acct 1220 on the website / Also on the file created with scraper.
        courseName = "ACCT*1220 - Introductory Financial Accounting - 0.50"
        courseDescription = """This course requires students to apply the fundamental principles emanating from accounting's conceptual framework and undertake the practice of financial accounting. Students will become adept at performing the functions related to each step in the accounting cycle, up to and including the preparation of the financial statements and client reports. Students will also develop the skills necessary for assessing an organization's system of internal controls and financial conditions."""
        coursePrerequisites = "None"
        courseOfferings = "Also offered through Distance Education format."
        courseRestrictions = "ACCT*2220. This is a Priority Access Course. Enrolment may be restricted to particular programs or specializations. See department for more information."
        courseEquate = "None"
        courseDepartment = "Department of Management"
        courseLocation = "Guelph"

        # Check if the result has all information
        self.assertTrue(output.getvalue().find(courseName) != -1 and output.getvalue().find(courseDescription) != -1 and
                        output.getvalue().find(coursePrerequisites) != -1 and output.getvalue().find(courseOfferings) != -1 and output.getvalue().find(courseRestrictions) != -1 and
                        output.getvalue().find(courseEquate) != -1 and output.getvalue().find(courseDepartment) != -1 and output.getvalue().find(courseLocation) != -1)


        # Reset stdout
        sys.stdout = sys.__stdout__

    def test_cc_search_invalid(self):

        output = StringIO()
        sys.stdout = output
        
        # Same code as used in previous test, however there is a space which should result in nothing being returned
        courseCodeSearch("ACCT* 1220")
        
        expectedOutput = "No results found."
        self.assertTrue(output.getvalue().find(expectedOutput) != -1)

        # Reset stdout
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()