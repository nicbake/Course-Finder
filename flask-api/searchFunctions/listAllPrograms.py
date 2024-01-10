#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import json
import os.path

# Program Information
__author__ = "Harsh Topiwala, Jainil Patel, Nicholas Baker, Lourenco Velez, Farid Hamid"
__version__ = "1.0.0"
__maintainer__ = "Farid Hamid"
__email__ = "fhamid@uoguelph.ca"
__status__ = "Development"

"""
Function to print all program names and codes.
Last Updated: 1/22/2022, by Farid Hamid
"""

def listAllProgs():
    """
    listAllProgs Function.
    :return: N/A
    """ 
    
    file = open(os.path.dirname(__file__) + '/../../scraper/json/GuelphAllCourses.json')
    data = json.load(file)

    print('\n-----------------------------------------------------\n')

    # Iterate through json objects and list all program names and respective codes.
    for program in data:
        print('{}: {} - {}'.format(program['programCode'], program['programName'], '{} courses'.format(str(len(program['programCourse'])))))

    print('\n-----------------------------------------------------\n')

    file.close()