#!/usr/bin/python3
from ctypes.wintypes import tagRECT
from tabnanny import check
from helper import *
from urllib import response
from flask import Flask, jsonify, render_template, request
import os.path
import json

# Program Information
__author__ = "Harsh Topiwala, Jainil Patel, Nicholas Baker, Lourenco Velez, Farid Hamid"
__version__ = "1.0.0"
__maintainer__ = "Harsh Topiwala"
__email__ = "htopiwal@uoguelph.ca"
__status__ = "Development"

"""
Flask-API that returns same data as CLI-based program in JSON format for use in webapp
Last Updated: 3/27/2022, by Harsh Topiwala
"""


app = Flask(__name__)

# test endpoint
@app.route("/api")
def index():
    return """
        Welcome to my website!<br /><br />
        <a href="/hello">Go to hello world</a>
    """

def getProgramData(school, programName):
    """
    Returns program courses if the program exists
    :param p1: school (string)
    :param p2: name of program (string)
    :return: (Array of objects) program information
    """ 
    path = os.path.dirname(__file__)
    path = path[:-1] + '/../scraper/json/'

    if school == 'uog':
        path += 'GuelphAllCourses.json'
    elif school == 'mcg':
        path += 'McGillAllCourses.json'

    file = open(path, encoding="utf-8")
    data = json.load(file)
    file.close()

    res = {}

    for program in data:
        if program['programName'].replace('&', '') == programName:
            res = program
            break
    return res

def getNodeColor(courseYear):
    """
    Returns color of node depending on course level
    :param p1: courseCode (string)
    :return: (String) color of node
    """

    if courseYear == '1':
        return '#FFB6A6'
    elif courseYear == '2':
        return '#FFE3A6'
    elif courseYear == '3':
        return '#C3FFA6'
    elif courseYear == '4':
        return '#A6FFE3'
    
    return '#F0FFA9'

# Generate a graph node
def generateGraphNode(courseCode):
    """
    Generates a course node
    :param p1: course code (string)
    :return: dictionary representing a course node (dictionary)
    """ 

    courseYear = 1
    if ' ' in courseCode:
        courseYear = courseCode.split(' ')[1][0]
    else:
        courseYear = courseCode.split('*')[1][0]

    return {
        'id': courseCode,
        'data' : { 'label' : courseCode},
        'style' : {
            'background': getNodeColor(courseYear)
        }
    }


# Generate edge between two ndoes
def generateGraphEdge(idFirst, idSecond, edgeType):
    """
    Generates an edge between two nodes
    :param p1: id of first node (string)
    :param p2: id of second node (string)
    :param p3: type of edge (dotted, solid) (boolean)
    :return: dictionary representing an edge between two courses (dictionary)
    """ 

    return {
        'id' : 'e{}-{}'.format(idFirst, idSecond),
        'source' : idFirst,
        'target' : idSecond,
        'animated' : edgeType
    }

def getCoursesData(courseCodes):
    """
    Returns an array of course data
    :param p1: the course codes to be searched for (array of strings)
    :return: array of dictionaries representing courses (array of dictionaries)
    """ 

    # Open file containing all course information for reading

    filePath = os.path.dirname(__file__)
    filePath = filePath[:-1] + '../scraper/json/GuelphAllCourses.json'
    file = open(filePath, encoding="utf-8")
    data = json.load(file)
    courseData = []

    for program in data:
        for course in program['programCourse']:
            if course['code'] in courseCodes:
                courseData.append(course)

    file.close()
    return courseData

def getMajorData(majorName):
    """
    Returns the data of a major
    :param p1: the name of the major we're looking for
    :return: dictionary with the major data
    """ 

    # Open file containing all course information for reading
    filePath = os.path.dirname(__file__)
    filePath = filePath[:-1] + '../scraper/json/GuelphMajorData.json'
    file = open(filePath, encoding="utf-8")
    data = json.load(file)
    majorData = {}
    # Traverse through all programs and find program with specified code 
    for major in data:
        if major['majorName'].replace('&', '') == majorName:
            majorData['programCourse'] = getCoursesData(major['majorCourses'])
            break
            
    file.close()
    return majorData


@app.route("/api/graph", methods=['GET'])
def majorAndProgramGraph():
    """
    Returns nodes and edges needed to build a prerequisite graph for a major or program
    :param p1: type (program, major)
    :param p1: school (uog, mcg)
    :param p1: programName (name of program)
    :param p1: majorName (name of major)
    :return: json string with node and edges formatted so react-flow can graph based on data
    """ 
    reqType = request.args.get('type')
    school = request.args.get('school')
    programName = request.args.get('programName')
    majorName = request.args.get('majorName')
    
    data = []
    # get program data
    if reqType == 'program':
        data = getProgramData(school, programName)
    elif reqType == 'major':
        data = getMajorData(majorName)

    # if no data returned 
    if len(data) == 0:
        return json.dumps({'message' : 'Could not generate graph, no program found with name {}'.format(programName)})
    
    # if no courses found for a program (mcgill)
    if len(data['programCourse']) == 0:
        return json.dumps({'nodes' : [{'id' : '1', 'data': { 'label' : 'No courses offered' }}], 'edges' : []})

    nodes = []
    edges = []

    addedNodes = set()
    addedEdges = set()

    for dataItem in data['programCourse']:
        prereqCodes = dataItem['prerequisiteCodes']
        currentCourseCode = dataItem['code']

        # generate current node
        currentNewNode = generateGraphNode(currentCourseCode)

        # only add node to final array if it hasn't been generated before
        if currentNewNode['id'] not in addedNodes: nodes.append(currentNewNode)
        addedNodes.add(currentCourseCode)

        # or case (1 of)
        for prereq in prereqCodes['or_courses']:
            
            # generate node and edge between current node and prerequisite
            newNode = generateGraphNode(prereq)
            newEdge = generateGraphEdge(prereq, currentCourseCode, True)

            # check for duplicates
            if newNode['id'] not in addedNodes: nodes.append(newNode) 
            if newEdge['id'] not in addedEdges: edges.append(newEdge)        

            # add node and edge id to duplicate set    
            addedNodes.add(newNode['id'])
            addedEdges.add(newEdge['id'])

        # mandatory courses
        for prereq in prereqCodes['mandatory']:
            newNode = generateGraphNode(prereq)
            newEdge = generateGraphEdge(prereq, currentCourseCode, False)
            if newNode['id'] not in addedNodes: nodes.append(newNode) 
            if newEdge['id'] not in addedEdges: edges.append(newEdge)            
            addedNodes.add(newNode['id'])
            addedEdges.add(newEdge['id'])

    return json.dumps({'nodes' : nodes, 'edges' : edges})

@app.route("/api/search/bar", methods=['GET'])
def searchBar():

    # Getting request parameters
    school = request.args.get('school')
    term = request.args.get('term')

    filePath = os.path.dirname(__file__)
    filePath = filePath[:-1] + '../scraper/json/'

    if school == '1':
        filePath += 'GuelphAllCourses.json'
    elif school == '2':
        filePath += 'McGillAllCourses.json'
    
    file = open(filePath, encoding="utf-8")
    data = json.load(file)
    file.close()

    response = []

    for i in range(len(data)):
        programCourses = data[i]['programCourse']
        for j in range(len(programCourses)):
            if term in programCourses[j]['name'] or term in programCourses[j]['code']:
                response.append(programCourses[j])

    return json.dumps(response)

@app.route("/api/search/getMajors", methods=['GET'])
def getGuelphMajors():
    """
    Returns list of all majors offered at uog
    :return: array of major names 
    """ 

    # Open major data file for reading
    filePath = os.path.dirname(__file__)
    filePath = filePath[:-1] + '../scraper/json/GuelphMajorData.json'
    file = open(filePath, encoding="utf-8")
    data = json.load(file)
    file.close()

    response = []

    # Get all major names
    for i in range(len(data)):
        response.append(data[i]['majorName'])
    
    return json.dumps(response)
    
@app.route("/api/search/university", methods=['GET'])
def updateUniversity():

    # Getting request parameters
    school = request.args.get('school')

    filePath = os.path.dirname(__file__)
    filePath = filePath[:-1] + '../scraper/json/'

    # Open file
    if school == 'uog':
        filePath += 'GuelphAllCourses.json'

    elif school == 'mcg':
        filePath += 'McGillAllCourses.json'
    
    else:
        return json.dumps([])
    
    file = open(filePath, encoding="utf-8")
    data = json.load(file)
    file.close()

    response = []

    for i in range(len(data)):
        currentProgramName = data[i]['programName'] 
        response.append(currentProgramName)
    
    return json.dumps(response)

# Filtered search
@app.route("/api/search/filtered", methods=['GET'])
def filteredSearch():
    

    # Getting request parameters
    school = request.args.get('school')
    program = request.args.get('program')
    credit = request.args.get('credit')
    offering = request.args.get('offering')

    filePath = os.path.dirname(__file__)
    filePath = filePath[:-1] + '../scraper/json/'
    
    # Open file
    if school == 'uog':
        filePath += 'Guelph'
        if offering != '' and program == '':
            filePath += offering + '.json'
        else:
            filePath += 'AllCourses.json'

    elif school == 'mcg':
        filePath += 'McGillAllCourses.json'
    
    else:
        return json.dumps([])

    file = open(filePath, encoding="utf-8")
    data = json.load(file)
    file.close()

    response = []
    programCourses = []
    
    #populate program courses with json file
    if program != '':

        for i in range(len(data)):
            currentProgramName = data[i]['programName'] 
            if currentProgramName == program:
                programCourses = data[i]['programCourse']
                break
        
        for i in range(len(programCourses)):
            if credit != '' and programCourses[i]['credit'] != credit:
                continue
            
            if offering != '' and offering[0] not in programCourses[i]['semester']:
                continue
                
            response.append(programCourses[i])

    elif offering == '':
        for i in range(len(data)):
            currentCourse = data[i]['programCourse']
            for j in range(len(currentCourse)):
                if currentCourse[j]['credit'] == credit or credit == '':
                    response.append(currentCourse[j])
    else:
        if school == 'uog':
            for i in range(len(data)):
                if credit != '' and data[i]['credit'] != credit:
                    continue
                
                response.append(data[i])
        elif school == 'mcg':
            for i in range(len(data)):
                currentCourse = data[i]['programCourse']
                for j in range(len(currentCourse)):
                    
                    if credit != '' and currentCourse[j]['credit'] != credit:
                        continue
                    if offering != '' and offering[0] not in currentCourse[j]['semester']:
                        continue

                    response.append(currentCourse[j])
    
    return json.dumps(response)

if __name__ == '__main__':
    # Will make the server available externally as well
    app.run(host='0.0.0.0')
