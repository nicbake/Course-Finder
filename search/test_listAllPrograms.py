# Imports
import unittest
import sys
from io import StringIO
from searchFunctions.listAllPrograms import listAllProgs

"""
Unittest based python program to compare Course Search result with expected result when printing all program codes.
Last Updated: 01/23/2022, by Lourenço Velez
"""

class TestAllPrograms(unittest.TestCase):

    # Test information from programs at random and if the last element is printed, and at least one of each information type. Ex: description, prerequisites, e.t.c
    def test_list_all_programs(self):

        output = StringIO()
        sys.stdout = output

        # Function call
        listAllProgs()

        compSci = "CIS: Computing and Information Science - 48 courses"
        psychology = "PSYC: Psychology - 50 courses"
        engineering = "ENGG: Engineering - 101 courses"
        lastCourse = "ZOO: Zoology - 18 courses"
        self.assertTrue(output.getvalue().find(compSci) != -1 and output.getvalue().find(psychology) != -1 and output.getvalue().find(engineering) != -1 and output.getvalue().find(lastCourse) != -1)

        # Reset stdout
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()