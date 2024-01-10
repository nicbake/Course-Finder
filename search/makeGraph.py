#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import argparse
from heapq import merge
import json
import os
import sys
import pygraphviz as pgv
from PyPDF2 import PdfFileMerger, PdfFileReader
#import win32file as wfile

# Program Information
__author__ = "Harsh Topiwala, Jainil Patel, Andrew Heft, Nicholas Baker, Lourenco Velez, Farid Hamid"
__version__ = "1.0.0"
__maintainer__ = "Harsh Topiwala, Farid Hamid and Jainil Patel"
__email__ = "htopiwal@uoguelph.ca"
__status__ = "Development"

"""
A CLI-based program with the purpose of generating a graph to visualize courses and their prerequisties.
Last Updated: 2/3/2022, by Harsh Topiwala
"""

def noPrerequisiteNodes(data, graph, delimeter):
    """
    Create a node for courses that don't have any prerequisites
    :return: (graph) a graph with an unconnected node
    """

    # If there are no prerequisites, then create a singular node with out any edges
    for course in data:
        coursePrereq = course['prerequisiteCodes']
        if len(coursePrereq['or_courses']) == 0 and len(coursePrereq['mandatory']) == 0:
            graph.add_node(course['code'], color=getNodeColor(course['code'], delimeter))
    
    return graph

def getCodes(graphType):
    """
    Creates an array of all subject codes
    :return: (string array) Return a string array of subject codes
    """

    # Open file and append program code to string array (codeData)
    if graphType == 'subject':
        file = open(os.path.dirname(__file__) + '/../scraper/json/McGillAllCourses.json', encoding="utf-8")
    elif graphType == 'program':
        file = open(os.path.dirname(__file__) + '/../scraper/json/GuelphAllCourses.json', encoding="utf-8")
    
    data = json.load(file)
    codeData = []
    for courses in data:
        codeData.append(courses['programCode'])
    
    file.close()
    return codeData

def getName(code, graphType):
    """
    Returns name of program or major
    :param p1: code (string) program/major code
    :param p2: graphType (string)
    :return: (string) name of program or major
    """ 

    # Open file based on the graphType
    if graphType == 'program':
        file = open(os.path.dirname(__file__) + '/../scraper/json/GuelphAllCourses.json')
    elif graphType == 'major':
        # Open file containing major courses information for reading
        file = open(os.path.dirname(__file__) + '/../scraper/json/GuelphMajorData.json')
    elif graphType == 'subject':
        graphType = 'program'
        file = open(os.path.dirname(__file__) + '/../scraper/json/McGillAllCourses.json', encoding="utf-8")

    # Set the variable name and tCode to the object names from the json file
    title = ""
    name = graphType + 'Name'
    tCode = graphType + 'Code'
    
    # Obtain the program/major name based on the code passed in
    data = json.load(file)
    for graphType in data:
        if(graphType[tCode] == code):
            title = graphType[name]

    file.close()

    return title

def grabProgramData(programCode, graphType):
    """
    Returns program courses if the program exists
    :param p1: programCode (string)
    :return: (Array of objects) program information
    """ 

    # Open file containing all course information for reading
    if graphType == 'program':
        file = open(os.path.dirname(__file__) + '/../scraper/json/GuelphAllCourses.json')
    elif graphType == 'subject':
        file = open(os.path.dirname(__file__) + '/../scraper/json/McGillAllCourses.json', encoding="utf-8")
    
    data = json.load(file)
    courseData = ['\0']
    # Traverse through all programs and find program with specified code 
    for program in data:
        if program['programCode'] == programCode:
            courseData = program['programCourse']
            break

    file.close()
    return courseData

def grabMajorData(majorCode):
    """
    Returns a list of courses (objects) that are required for a major
    :param p1: majorCode (string)
    :return: (Array of objects) major information
    """ 

    # Open file containing all course information for reading
    file = open(os.path.dirname(__file__) + '/../scraper/json/GuelphMajorData.json')
    data = json.load(file)
    majorData = []
    # Traverse through all programs and find program with specified code 
    for major in data:
        if major['majorCode'] == majorCode:
            for courseCode in major['majorCourses']:
                majorData.append(getCourseData(courseCode))
            
    file.close()
    return majorData

def getCourseData(courseCode):
    """
    Returns data for a singular course 
    :param p1: courseCode (string)
    :return: single object containing course data
    """

    # Open file containing all course information for reading
    file = open(os.path.dirname(__file__) + '/../scraper/json/GuelphAllCourses.json')
    data = json.load(file)
    courseObj = {}

    for program in data:
        for course in program['programCourse']:
            if course['code'] == courseCode:
                courseObj = course

    file.close()
    return courseObj

def listAllMajors():
    """
    Prints all majors and their codes
    :return: N/A
    """ 
    # Open file containing all course information for reading
    file = open(os.path.dirname(__file__) + '/../scraper/json/GuelphMajorData.json')
    data = json.load(file)
    # Traverse through all programs and find program with specified code 
    print('\n-----------------------------------------------------\n')

    for major in data:
        print('{} - {}'.format(major['majorName'], major['majorCode']))

    print('\n-----------------------------------------------------\n')        
    file.close()

def add_graph_nodes(graph, prereq, currCourse, courseType, graphType):
    """
    Adds nodes to graph
    :param p1: graph (graph)
    :param p2: prereq (string)
    :param p3: currCourse (string)
    :return: (String) color of node
    """ 

    delimeter = " "
    if (graphType == "program") or (graphType == "major"):
        delimeter = "*"
    
    graph.add_node(prereq, color=getNodeColor(prereq, delimeter))
    graph.add_node(currCourse, color=getNodeColor(currCourse, delimeter))
    # If the course is optional from a set of courses, the edges become a dashed line to connect nodes
    if courseType == 'or':
        graph.add_edge(prereq, currCourse, dir='forward', style='dashed')
    # Course is mandatory will have solid lines to connect nodes
    else:
        graph.add_edge(prereq, currCourse, dir='forward')
        
    return graph

def getNodeColor(courseCode, delimeter):
    """
    Returns color of node depending on course level
    :param p1: courseCode (string)
    :return: (String) color of node
    """
    if delimeter in courseCode:
        courseYear = (courseCode.split(delimeter))[1][0]
    else:
        return 'magenta'
    if courseYear == '1':
        return 'red'
    elif courseYear == '2':
        return 'blue'
    elif courseYear == '3':
        return 'orange'
    
    return 'magenta'

def generateGraph(code, graphType):
    """
    Generates a graph based on program code specified in command.
    :param p1: code (string)
    :param p1: type (string)
    :return: None
    """

    # Grabbing data based on graph type
    data = []
    if graphType == 'major':
        data = grabMajorData(code)
    elif graphType == 'program':
        data = grabProgramData(code, graphType)
    elif graphType == 'subject':
        data = grabProgramData(code, graphType)

    # Initialize empty graph
    graph = pgv.AGraph(ranksep='5')

    # Create title, set font size to 30 and center to top of page
    name = getName(code, graphType)
    graph.graph_attr["label"] = name
    graph.graph_attr["fontsize"] = 30
    graph.graph_attr["labelloc"] = "t"
    #graph.graph_attr["size"] = "7.75, 10.25"
    #graph.graph_attr["ratio"] = "fill"

    if len(data) == 1:
        if data[0] == '\0':
            print("Could not find program with code '{}'".format(code))
            graph.close()
            sys.exit(1)
            
    elif len(data) == 0:
        graph.add_node("No courses offered")

    # Generate graph
    for dataItem in data:
        # Traverse through prerequisites and create nodes and edges
        prereqCodes = dataItem['prerequisiteCodes']
        
        # '1 of' case
        for prereq in prereqCodes['or_courses']:
            graph = add_graph_nodes(graph, prereq, dataItem['code'], 'or', graphType)
        
        # 'Mandatory' case
        for prereq in prereqCodes['mandatory']:
            graph = add_graph_nodes(graph, prereq, dataItem['code'], 'mandatory', graphType)
    
    delimeter = " "
    if (graphType == "program") or (graphType == "major"):
        delimeter = "*"

    # Codes with no prerequisites 
    noPrerequisiteNodes(data, graph, delimeter)

    # Layout and export graph
    graph.layout(prog='dot')

    # Case 1: If graphtype is subject, create all the graphs and merge the files into one pdf file
    if graphType == 'subject':
        graph.draw('graphs/{}_{}_graph.pdf'.format(code, graphType))
    # Case 2: Otherwise if graphtype is 'program' or 'major', create only one graph
    else:
        graph.draw('graphs/{}_{}_graph.pdf'.format(code, graphType))
    
    graph.close()


# Fix issue where files combine regardless of what contents they have when generating all
# Fix issue where existing merge files are appended to instead of deleted
# Fix issue where graphs folder is not generated
# Fix issue with order of merge (add names to array and iterate through there when merging)
def mergeFiles(graphType, finalFileName):
    """
    Merges all prerequisite graphs into a single file ONLY IF the 'All' flag is specified
    :return: (String) Result to be displayed back to user.
    """ 
    mergeFile = PdfFileMerger()
    codes = getCodes(graphType)
    existingFiles = set()
    mergeOrder = []

    mergedNamePath = './graphs/' + finalFileName
    if os.path.exists(mergedNamePath):
        os.remove(mergedNamePath)

    for filename in os.scandir('./graphs'):
        existingFiles.add(filename.name)

    # Generate graph for each subject or major if it doesn't already exist
    for code in codes:
        currFileName = '{}_{}_graph.pdf'.format(code, graphType)
        mergeOrder.append(currFileName)
        if os.path.exists('./graphs/' + currFileName) == False:
            generateGraph(code, graphType)

    # Merge graphs
    for filename in mergeOrder:
        if filename.split("_")[1] == graphType:
            mergeFile.append(PdfFileReader('./graphs/' + filename, 'r'))
            # Only remove file if it wasn't in the graphs directory before
            if filename not in existingFiles:
                os.remove('./graphs/' + filename)

    mergeFile.write(mergedNamePath)

def parseArguments():
    """
    Parses CLI command to get program to generate graph for.
    :return: (String) Result to be displayed back to user.
    """ 
    # Parser initialization
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='Graph Generation Methods')

    # Program code parsing
    prerequisiteParser = subparsers.add_parser('prg', help='Generate prerequisite graph for all courses in a program. e.g python3 makeGraph.py prg CIS ')
    prerequisiteParser.add_argument('[Program Code]')
    prerequisiteParser.set_defaults(which='prg')

    # Major code parsing
    prerequisiteMajorParser = subparsers.add_parser('mrg', help='Generate prerequisite graph for all courses in a major. e.g python3 makeGraph.py mrg CIS ')
    prerequisiteMajorParser.add_argument('[Major Code]')
    prerequisiteMajorParser.set_defaults(which='mrg')

    # Subject code parsing
    prerequisiteSubjectParser = subparsers.add_parser('sbg', help='Generate prerequisite graph for all courses in a subject. e.g python3 makeGraph.py sbg COMP')
    prerequisiteSubjectParser.add_argument('[Subject Code]')
    prerequisiteSubjectParser.set_defaults(which='sbg')

    # Parser for listing majors and their codes
    listMajorsParser = subparsers.add_parser('lm', help='List all majors and their codes, i.e python3 makeGraph.py lp')
    listMajorsParser.set_defaults(which='lm')

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = vars(parser.parse_args())

    # Check if directory for graphs exists
    if not os.path.exists('graphs'):
        os.makedirs('graphs')

    # If the user chooses the program flag and requests all courses, then merge all graphs into one pdf
    if args['which'] == 'prg':
        if(args['[Program Code]'] == 'All'):
            mergeFiles('program', 'Guelph_Merged_Programs.pdf')
        else: 
            generateGraph(args['[Program Code]'], 'program')
    elif args['which'] == 'mrg':
        generateGraph(args['[Major Code]'], 'major')
    # If the user chooses the program flag and requests all courses, then merge all graphs into one pdf
    elif args['which'] == 'sbg':
        if(args['[Subject Code]'] == 'All'):
            mergeFiles('subject', 'McGill_Merged_Programs.pdf')
        else:
            generateGraph(args['[Subject Code]'], 'subject')
    else:
        listAllMajors()

def main():
    """
    Main Function.
    :param p1: N/A
    :return: N/A
    """

    # Increase the max standard input
    #wfile._setmaxstdio(775)
    parseArguments()

if __name__ == "__main__":
    main()
