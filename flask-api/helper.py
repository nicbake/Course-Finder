from ast import NotIn
import sys
import os.path
import json
from searchFunctions import courseCode, courseWeightSeason, programCode, listAllPrograms

def searchCodesCourse():
    courseCode.courseCodeSearch()
    pass

def searchSeasonWeightCourse():
    courseWeightSeason.courseWS()
    pass

def searchCodeProgram():
    programCode.programCodeSearch()
    pass

def searchProgramsAllList():
    listAllPrograms.listAllProgs()
    pass

def tempFunc():
    courses = { 
        "ENG": "Engineer" 
    }
    print(courses)
    return courses

def testerFunc():
    # Getting request parameters
    filePath = os.path.dirname(__file__) + '/../scraper/json/'
    
    #filePath += 'GuelphAllCourses.json'

    filePath += 'McGillAllCourses.json'
    
    file = open(filePath, encoding="utf-8")
    data = json.load(file)
    file.close()

    response = []
         
    for i in range(len(data)):
        currentCourse = data[i]['programCourse']
        for j in range(len(currentCourse)):
            if currentCourse[j]['credit'] not in response:
                response.append(currentCourse[j]['credit'])
    
    print(sorted(response))

testerFunc()
