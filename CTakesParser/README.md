CTakes Parser
============

A simple command line utility which parses the output of of the Apache CTakes project (an xml file)
and dumps the concept UI and tokenization information into an Excel-readable CSV document. Requires
Python 2.7

##Usage

    python ctakes-parse.py [FLAGS] XML-FILE
* -d (--debug)			show debug output
* -v (--verbose)			print out more details
* -o (--output-file) OUTFILE	saved parsed XML data in a CSV spreadsheet
* -c (--cui-file) OUTFILE		save the CUIs as a newline separated list
* -h (--help)             displays the help text