#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import argparse
import sys
from searchFunctions import courseCode, courseWeightSeason, programCode, listAllPrograms

# Program Information
__author__ = "Harsh Topiwala, Jainil Patel, Nicholas Baker, Lourenco Velez, Farid Hamid"
__version__ = "1.0.0"
__maintainer__ = "Harsh Topiwala"
__email__ = "htopiwal@uoguelph.ca"
__status__ = "Development"


"""
A CLI-based program with the purpose of searching through UoG's courses.
Last Updated: 1/19/2022, by Harsh Topiwala
"""

def parseCLIArgs():
    """
    Runs a specific type of search depending on flag set in the command.
    :return: (String) Result to be displayed back to user.
    """ 


    # Parser initialization
    parser = argparse.ArgumentParser(prog='tool', formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=10))
    subparsers = parser.add_subparsers(help='Search Methods')

    # Case 1: list all programs
    #   courseSearch lp
    listProgramsParser = subparsers.add_parser('lp', help='List all programs and their codes, i.e python3 courseSearch.py lp')
    listProgramsParser.set_defaults(which='lp')

    
    # Case 2: search by course code: 
    #   courseSearch cc {Course code, i.e: ACCT*1000}
    ccParser = subparsers.add_parser('cc', help='Search by course code, i.e python3 courseSearch.py cc {course code, i.e ACCT*1220}')
    ccParser.add_argument('[Course Code]')
    ccParser.set_defaults(which='cc')

    # Case 3: search by program code: 
    #   courseSearch pc {Program code}
    pcParser = subparsers.add_parser('pc', help='Search by program code, i.e python3 courseSearch.py pc {program code, i.e ACCT}')
    pcParser.add_argument('[Program Code]')
    pcParser.set_defaults(which='pc')


    # Case 4: search by credit weight and season: 
    #   courseSearch cw {0.25, 0.5, 0.75, ... } {Season: optional, default all seasons}
    cwParser = subparsers.add_parser('cw', help='Search by course weight and season (optional), i.e python3 courseSearch.py cw {course weight, i.e 0.25}, {season (optional), i.e S}')
    cwParser.add_argument('[Course Weight]', choices=['0.00', '0.25', '0.50', '0.75', '1.00'])
    cwParser.add_argument('[Offering Season]', type=str.upper, nargs='?', default='all', choices=['S', 'W', 'F', 'ALL'])
    cwParser.set_defaults(which='cw')

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = vars(parser.parse_args())

    # Call search functions based on command type    
    if args['which'] == 'cc':
        courseCode.courseCodeSearch(args['[Course Code]'])

    elif args['which'] == 'pc':
        programCode.programCodeSearch(args['[Program Code]'])

    elif args['which'] == 'cw':
        courseWeightSeason.courseWS(args['[Course Weight]'], args['[Offering Season]'])
    else:
        listAllPrograms.listAllProgs()

def main():
    """
    Main Function.
    :param p1: N/A
    :return: N/A
    """ 

    parseCLIArgs()

if __name__ == "__main__":
    main()
