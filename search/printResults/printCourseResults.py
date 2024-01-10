#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import json
import os.path

# Program Information
__author__ = "Harsh Topiwala, Jainil Patel, Nicholas Baker, Lourenco Velez, Farid Hamid"
__version__ = "1.0.0"
__maintainer__ = "Harsh Topiwala"
__email__ = "htopiwal@uoguelph.ca"
__status__ = "Development"

"""
Formats a list of course results, returns a string.
Last Updated: 1/22/2022, by Harsh Topiwala
"""

def formattedInfo(courseInfo):
    """
    Formats course data, seperating by newline
    :param p1: string (containing course data)
    :return: string (an easy-to-digest block of course information)
    """ 

    lines = courseInfo.split('\n')
    res = []
    for line in lines:
        res.append(line)
    return '\n'.join(res)

def printIfExists(courseData):
    """
    Returns "None" if certain course data isn't present
    :param p1: courseData (dictionary containing course data)
    :return: string (None or the course data if it exists)
    """ 

    return "None" if len(courseData) == 0 else courseData

def printCourseResults(course):
    """
    Prints course results in a formatted manner.
    :param p1: course (dictionary containing course data)
    :return: string (an easy-to-digest block of course information)
    """ 

    courseName = '{} - {} - {}\n'.format(course['code'], course['name'], course['credit'])
    description = 'Description: {}\n'.format(printIfExists(course['description']))
    prerequisites = 'Prerequisite(s): {}\n'.format(printIfExists(course['prerequisites']))
    offerings = 'Offering(s): {}\n'.format(printIfExists(course['offering']))
    restrictions = 'Restriction(s): {}\n'.format(printIfExists(course['restriction']))
    equates = 'Equate(s): {}\n'.format(printIfExists(course['equate']))
    department = 'Department(s): {}\n'.format(printIfExists(course['department']))
    locations = 'Location(s): {}\n'.format(printIfExists(course['location']))

    unformattedString = courseName + description + prerequisites + offerings + restrictions + equates + department + locations    
    return formattedInfo(unformattedString)
