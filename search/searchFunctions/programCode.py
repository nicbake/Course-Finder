#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import json
import os.path

from printResults.printCourseResults import printCourseResults


# Program Information
__author__ = "Harsh Topiwala, Jainil Patel, Nicholas Baker, Lourenco Velez, Farid Hamid"
__version__ = "1.0.0"
__maintainer__ = "Farid Hamid"
__email__ = "fhamid@uoguelph.ca"
__status__ = "Development"

"""
Function to print all courses within a specific program.
Last Updated: 1/22/2022, by Farid Hamid
"""

def programCodeSearch(programCode):
    """
    programCodeSearch Function.
    :param p1: programCode (string)
    :return: N/A
    """ 
    
    file = open(os.path.dirname(__file__) + '/../../scraper/json/AllCourses.json')
    data = json.load(file)

    resultCount = 0

    print('\n-----------------------------------------------------\n')
    
    # Iterate through programs and list all courses in that a program. 
    for program in data:
        if program['programCode'] == programCode:
            for course in program['programCourse']:
                resultCount += 1
                print(printCourseResults(course))
                print('-----------------------------------------------------\n')

    
    if resultCount == 0:
        print("No results found.")
        print('-----------------------------------------------------\n')

    file.close()