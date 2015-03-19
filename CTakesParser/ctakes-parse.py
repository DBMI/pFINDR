"""
January 29, 2015
Author: Dexter Friedman
Division of BioMedical Informatics, UCSD

This file parses the XML output from CTakes, and dumps out all of the UMLS concepts CTakes was
able to detect from the input string into a CSV file.

Eventual Goal:
	CTakes UMLS XML Output Parser -> MetaMap Output (preserving existing PhenDisco pipeline)
Python 2.7.9
"""

import sys
import getopt
import os
import xml.etree.ElementTree as XML

class UMLSConcept:
	"""Container for an individual concept in the UMLS hierarchy. Stores the concept ID and tui, 
	   as well as the id of the concept in the XML output from CTakes."""
	# Constructor
	def __init__(self):
		"""
		Creates a mew UMLSConcept object, setting the concept ID and tui to 
		None by default
		"""
		self.cui = None # Concept unique identifier
		self.tui = None 
		self.tok = None # String token/phrase this concept was mapped to
		self.codingScheme = "" # RXNORM or SNOWMED
		self.elementID = None  # Corresponds to attribute _id in the XML input

	def __repr__(self):
		"""Returns a string describing the relevant information about this UMLSConcept"""
		return "<UMLSConcept: CUI: %s, TUI: %s >" % (self.cui, self.tui)

	def setProperties(self,elt,tokstr):
		"""Takes a UmlsConcept XML element object, and autofills this instances's properties accordingly"""
		self.tok = tokstr
		if 'cui' in elt.attrib and 'tui' in elt.attrib:
			self.elementID = elt.attrib['_id']
			self.cui = elt.attrib['cui']
			self.tui = elt.attrib['tui']
			self.codingScheme = elt.attrib['codingScheme']

	# def writeToCSV(self):

class OntologyConcept:
	"""Container for an individual ontology concept, encoded using the RXNORM scheme. RXNORM
	concepts do not have cui & tui."""
	def __init__(self):
		self.elementID = ""

class OntologyConceptArray:
	"""Tokens from the input may map to multiple concepts. This class contains a token string,
	and a list of all the UMLS or ontology concepts that it could be interpreted as. This data is extracted
	from a single <...FSArray> element in the CTakes xml output."""

	# Constructor
	def __init__(self,tokstr,fsArrayElement):
		"""Takes an FSArray element from the XML, and parses its children, thereby locating the
		concept elements, which are either ontology concepts (RXNORM) or UMLS concepts (SNOWMED)"""
		self.token = tokstr
		self.element = fsArrayElement
		self.concepts = []    # List of all the concepts we found, as UMLSConcept objects

	def findConcepts(self,xmlDict,vb=False,db=False):
		"""Given an array of potential concepts, iterate through that array. Each element of the array
		should map to a unique _id attribute in the XML file, which we can use to extract the CUI & TUI"""
		if self.element is not None:
			if db:
				print "Len of self.element = %d, self.element.tag = %s" % (len(list(self.element)),self.element.tag)
			for child in list(self.element):
				conceptID = child.text
				if db:
					print "Found conceptID: %s" % conceptID
				if conceptID not in xmlDict and vb:
					# An error!
					print "Given conceptID (%s) is could not be found from the post-parsing data." % conceptID
				elif 'cui' in xmlDict[conceptID].attrib and 'tui' in xmlDict[conceptID].attrib:
					# We've found a UMLS concept!
					umls = UMLSConcept()
					umls.setProperties(xmlDict[conceptID],self.token)
					self.concepts.append(umls)
				else:
					if db:
						print "Concept ID (%s) did not resolve to a UMLSConcept" % conceptID
		if vb:
			print "Found %d concepts for token '%s'" % (len(self.concepts),self.token)

def main():
	"""
	Reads in the XML output from CTakes and outputs the UMLS concepts in a CSV file
	"""

	USAGE_TEXT = "Usage: ctakes-parse.py [FLAGS] XML-FILE\n-d (--debug)\t\t\tshow debug output\n-v (--verbose)\t\t\tprint out more details\n-o (--output-file) OUTFILE\tsaved parsed XML data in a CSV spreadsheet\n-c (--cui-file) OUTFILE\t\tsave the CUIs as a newline separated list"
	
	# It may be useful later on to process CL arguments and options
	try:
		options, args = getopt.getopt(sys.argv[1:],"dvo:c:h",["debug","verbose","output-file","cui-file","help"])
	except getopt.error:
		print 'Invalid argument or option specified'
		return 1

	# Default Settings 
	verbose = False
	writeToCSV = False
	writeCUIFile = False
	debug = False
	outfile = ""
	cuifile = ""

	# Handle the command line options
	for opt, argument in options:
		if opt == "-v" or opt == "--verbose":
			verbose = True
		elif opt == "-d" or opt == "--debug":
			debug = True
		elif opt == "-o" or opt == "--output-file":
			writeToCSV = True
			outfile = argument
		elif opt == "-c" or opt == "--cui-file":
			writeCUIFile = True
			cuifile = argument

	# First argument is the XML file we wish to parse
	if len(args) < 1:
		print USAGE_TEXT
		return 1

	try:
		if verbose:
			print 'Parsing {} ...'.format(args[0])
		tree = XML.parse(args[0])
	except XML.ParseError:
		print 'The file specified is not valid XML.'
		return 2
	else:
		if verbose:
			print 'Parsing Complete!'

	root = tree.getroot()
	inputText = root[0].attrib['sofaString']
	if verbose:
		print "Untokenized input string (sofaString) is %d characters long." % len(inputText)

	xmlDict = {}
	conceptsFound = []
	if verbose:
		print 'Searching for concept data...'

	for elt in root:
		if '_id' in elt.attrib:
			xmlDict[elt.attrib['_id']] = elt # Allow random access to the entire tree by _id field

	for elt in root:
		if '_ref_ontologyConceptArr' in elt.attrib:
			# We've located some kind of token or phrase which is in UMLS or another ontology
			beginPos = int(elt.attrib['begin'])
			endPos = int(elt.attrib['end'])
			arr = OntologyConceptArray( inputText[beginPos:endPos], xmlDict[ elt.attrib['_ref_ontologyConceptArr'] ] )
			arr.findConcepts(xmlDict,vb=verbose,db=debug)
			conceptsFound.append(arr)
	
	if verbose:
		print 'Found %d potential concepts.' % (len(conceptsFound))

	# Dump everything in a CSV file
	if writeToCSV:
		file = None
		try:
			file = open(outfile, "wb")
		except IOError:
			print 'An I/O error occurred while trying to open or write to %s.' % (outfile)
		else:
			print 'Opened "%s" for writing.' % (outfile)
			file.write('TYPE, TOKEN, CUI, TUI, "CODING SCHEME", "XML \'_id\'"\r\n')
			for conceptArray in conceptsFound: 			# conceptsFound is a list of OntologyConceptArray(s)
				for concept in conceptArray.concepts:   # grab each UMLSConcept from list called 'concepts' found within a given OntologyConceptArray
					file.write( "UMLSConcept, %s, %s, %s, %s, %s\r\n" % (concept.tok, concept.cui, concept.tui, concept.codingScheme, concept.elementID))
			file.close()
			print 'Finished writing to "%s."' % (outfile)

	# Dump a list of newline delimeted for Alex
	if writeCUIFile:
		file = None
		cuiSet = set()
		try:
			file = open(cuifile, "wb")
		except IOError:
			print 'An I/O error occurred while trying to open or write to %s.' % (cuifile)
		else:
			print 'Opened "%s" for writing.' % (cuifile)
			for conceptArray in conceptsFound: 			# conceptsFound is a list of OntologyConceptArray(s)
				for concept in conceptArray.concepts:   # grab each UMLSConcept from list called 'concepts' found within a given OntologyConceptArray
					if concept not in cuiSet:
						cuiSet.add(concept)
			for concept in cuiSet:
				file.write( "%s\n" % (concept.cui))
			file.close()
			print 'Finished writing to "%s."' % (cuifile)

	return 0

# If we're called from the command line, call main
if __name__ == "__main__":
	sys.exit(main()) # The return value from main is our exit code