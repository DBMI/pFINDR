# 	$Id$	
# Query module for information retrieval
# This is a part if PFINDR project implemented at DBMI, UCSD
# This program is to write into format such as HTML, JSON in order to diplaying and exporting data
# Written by Son Doan, Aug 2012

import os,sys
import getopt
import html2text
import json
from whoosh.index import create_in
from whoosh import index, store, fields
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import MultifieldParser
from whoosh import highlight
from whoosh import scoring
from whoosh import sorting
from whoosh import analysis
from whoosh.query import FuzzyTerm
import MySQLdb
from DB import Table
from TextMap import *
import textwrap
import re

##################
# Replace MySQL username and password below
MySQLname = ""
MySQLpassword = ""

# Path of indexing storage
StoragePATH = "./PhD"

##################

def checkBool(str1):
	if str1.lower()=='(and' or str1.lower() =='and)' or str1.lower()=='and':
		return True
	if str1.lower()=='(or' or str1.lower()=='or)' or str1.lower()=='or':
		return True
	if str1.lower()=='(not' or str1.lower() =='not)' or str1.lower()=='not':
		return True

	return False

def HighlightX(terms1,docText):
	docText=docText.decode('utf-8') 
	for value in terms1:
		# Method 2
		docText = re.sub(re.escape(value), ur'<strong class="match term0">\g<0></strong>', docText, flags=re.IGNORECASE | re.UNICODE)

	return docText

def AddQuote(Query):
	Temp1 = Query.strip('"').split()
	Temp2 = '' + '"'
	for item in Temp1:
		if checkBool(item)==False:
			Temp2 = Temp2 + ' ' + item.strip('"')
		else:
			Temp2 = Temp2 + '" ' + item.strip('"') + ' "'
	Temp2 = Temp2 + '"'
	return Temp2

def QueryAnalys(query,concept):
	''' This function return query analysis with concept or not
	query default is free text 
	concept default is False
	'''

	# Process query
	# uppercase in case matched 'and','or','not' 
	if query.find(' and ')>0:
		query = query.replace(' and ', ' AND ')
	if query.find(' or ')>0:
		query = query.replace(' or ', ' OR ')			
	if query.find(' not ')>0:
		query = query.replace(' not ', ' NOT ')	
	if query.find(' And ')>0:
		query = query.replace(' And ', ' AND ')
	if query.find(' Or ')>0:
		query = query.replace(' Or ', ' OR ')			
	if query.find(' Not ')>0:
		query = query.replace(' Not ', ' NOT ')	

	if query.find('\%93')>=0:
		query = query.replace('\%93', '"')

	if query.find('\%94')>=0:
		query = query.replace('\%94', '"')

	# Add double quotes into keyword search
	# Query reformulation

	substudies1 = ["phs000568.v1.p1",
		"phs000487.v1.p1",
		"phs000544.v1.p6",
		"phs000534.v1.p1", 
		"phs000533.v1.p1",
		"phs000532.v1.p1", 
		"phs000531.v1.p1", 
		"phs000530.v1.p1",
		"phs000529.v1.p1", 
		"phs000528.v1.p1",
		"phs000527.v1.p1",
		"phs000515.v2.p1", 
		"phs000503.v2.p2", 
		"phs000499.v1.p1",
		"phs000498.v1.p1", 
		"phs000489.v2.p6",
		"phs000471.v3.p1",
		"phs000470.v3.p1", 
		"phs000469.v3.p1", 
		"phs000468.v3.p1", 
		"phs000467.v3.p1", 
		"phs000466.v3.p1", 
		"phs000465.v3.p1",
		"phs000464.v3.p1",
		"phs000463.v3.p1", 
		"phs000441.V2.P6", 
		"phs000429.v1.p1", 
		"phs000420.v3.p2",
		"phs000386.v4.p2",
		"phs000377.v1.p1", 
		"phs000363.v5.p7", 
		"phs000342.v6.p7", 
		"phs000315.v4.p2", 
		"phs000307.v3.p7", 
		"phs000301.v1.p1",
		"phs000296.v1.p2",
		"phs000283.v4.p2", 
		"phs000282.v7.p7",
		"phs000281.v4.p2",
		"phs000246.v1.p1",
		"phs000227.v1.p2",
		"phs000184.v1.p1",
		"phs000123.v1.p1"]

	substudies = ["phs000568",
		"phs000487",
		"phs000544",
		"phs000534", 
		"phs000533",
		"phs000532", 
		"phs000531", 
		"phs000530",
		"phs000529", 
		"phs000528",
		"phs000527",
		"phs000515", 
		"phs000503", 
		"phs000499",
		"phs000498", 
		"phs000489",
		"phs000471",
		"phs000470", 
		"phs000469", 
		"phs000468", 
		"phs000467", 
		"phs000466", 
		"phs000465",
		"phs000464",
		"phs000463", 
		"phs000441", 
		"phs000429", 
		"phs000420",
		"phs000386",
		"phs000377", 
		"phs000363", 
		"phs000342", 
		"phs000315", 
		"phs000307", 
		"phs000301",
		"phs000296",
		"phs000283", 
		"phs000282",
		"phs000281",
		"phs000246",
		"phs000227",
		"phs000184",
		"phs000272",
		"phs000123"]

	q1=''
	for sub in substudies:
		q1 += ' NOT ' + sub

	# Browse top-level studies
	if query=='top':
		q2 = 'phs* OR egas* ' + q1
		return unicode(q2)

	if concept==True:
		if query.find('phs')>=0 or query.find('egas')>=0:
			return unicode(query)

		if query !='top':
			if query.lower().find(' and ')>=0 or query.lower().find(' or ')>=0 or query.lower().find(' not ')>=0: 

				# Add double quotes into query before running MetaMap
				# query like this
				# s = "heart attack" and ("lung cancer" or copd)

				# Must add quotes before parsing
				queryQuote = AddQuote(query)
				#print queryQuote

				#QueryParse1 = QueryParse(query)
				QueryParse1 = QueryParse(queryQuote)
				QueryParseStr = QueryParse1.Parse()
				return unicode(QueryParseStr)

			else:
				ExtendedQ = QueryMap(query)
				MetaMap = ExtendedQ.wrapper()
				
				# Show the query extension
				try:
					MetaMapOut = ExtendedQ.getMapping(MetaMap)
				except:
					MetaMapOut = query
				
				if len(MetaMapOut.strip())>0:
					return unicode(MetaMapOut)
				else:
					return unicode(query)
	else:
		return unicode(query)
'''
Reformat text so that it fits the cell
'''
def ReformatTitle(TextInput):
      
	# Display title with maxium n words, n=5	

	Text1 = textwrap.wrap(TextInput,34)
	TextInput1 = '<br>'.join(Text1[0:])

	return TextInput1

'''
Reformat text so that it fits the cell
'''
def ReformatOther(TextInput):

	TextInput1 = TextInput.replace(',',' <br> ')
	return TextInput1

'''
Reformat text so that it fits the cell
'''
def ReformatOther1(TextInput):

	TextInput1 = TextInput.replace(';',' <br> ')
	return TextInput1

'''
Reformat text so that it fits the cell
'''
def ReformatWidth(TextInput,size):

        Text1 = textwrap.wrap(TextInput,size)
        TextInput1 = '<br>'.join(Text1[0:])

        return TextInput1

def usage():

	print '''Usage:

This program is for retrieval of relevant studies from dbGaP

python Query_All_HTML.py -i <input query> -p <page number> [-f] [-c] [-d] [-l]
-h, --help: This function
-i, --input <Query> : Input query
-p, --page <Page> : Page number
-f, --format: Output format, defaul as HTML, otherwise is JSON format
-c, --concept: Use concept extension or not. Default False
-d, --debug: True or False. Default False
-l, --limit: Limitation search, can be Study, StudyDesc, StudyTitle, StudyID, Variable, VariableID, VariableDesc

Examples:
python Query_All.py -i "lung cancer" -p 1 -c
'''

def AddSubstudy(StudyIDx):

	# Add mother and sub-studies information on Apr 2013.
	Substudies = {}
	Substudies['phs000185'] = ['phs000123;Genome-Wide Association Study of Serum YKL-40 Levels','phs000184;Genome-Wide Association Study of Plasma Lp(a) Levels Identifies Multiple Genes on Chromosome 6q']
        Substudies['phs000200'] = ['phs000227;PAGE: Women\'s Health Initiative (WHI)','phs000281;NHLBI GO-ESP: Women\'s Health Initiative Exome Sequencing Project (WHI) - WHISP','phs000315;WHI GARNET','phs000386;NHLBI WHI SHARe','phs000503;Women\'s Health Initiative Sight Examination (WHISE)']
	Substudies['phs000182'] = ['phs000246;Fuchs\' Corneal Dystrophy: A Secondary Genome Wide Association Study']
	Substudies['phs000007'] = ['phs000282;NHLBI Framingham Candidate Gene Association Resource (CARe)','phs000307;NHLBI Framingham Heart Study Allelic Spectrum Project','phs000342;NHLBI Framingham SNP Health Association Resource (SHARe)','phs000363;NHLBI Framingham SABRe CVD','phs000401;NHLBI GO-ESP: Heart Cohorts Exome Sequencing Project (FHS)']
	Substudies['phs000209'] = ['phs000283;NHLBI MESA Candidate Gene Association Resource (CARe)','phs000420;NHLBI MESA SHARe','phs000403;NHLBI GO-ESP: Heart Cohorts Component of the Exome Sequencing Project (MESA)']
	Substudies['phs000179'] = ['phs000296;NHLBI GO-ESP: Lung Cohorts Exome Sequencing Project (COPDGene)']
	Substudies['phs000287'] = ['phs000301;PAGE: CALiCo: Cardiovascular Health Study (CHS)','phs000377;NHLBI Cardiovascular Health Study (CHS) Candidate Gene Association Resource (CARe)','phs000226;STAMPEED: Cardiovascular Health Study (CHS)','phs000400;NHLBI GO-ESP: Heart Cohorts Exome Sequencing Project (CHS)']
	Substudies['phs000001'] = ['phs000429;NEI Age-Related Eye Disease Study (AREDS)']
	Substudies['phs000178'] = ['phs000441;Integrated Genomic Analyses of Ovarian Carcinoma (OV)','phs000489;Comprehensive Genomic Characterization Defines Human Glioblastoma Genes and Core Pathways','phs000544;Molecular Characterization of Human Colorectal Cancer (CRC)','phs000570;Comprehensive Genomic Characterization of Squamous Cell Lung Cancers (LUSC)','phs000569;Comprehensive Molecular Portraits of Human Breast Tumors (BRCA)']
	Substudies['phs000218'] = ['phs000463;TARGET: Acute Lymphoblastic Leukemia (ALL) Pilot Phase 1','phs000464;TARGET: Acute Lymphoblastic Leukemia (ALL) Expansion Phase 2','phs000465;TARGET: Acute Myeloid Leukemia (AML)','phs000466;TARGET: Kidney, Clear Cell Sarcoma of the Kidney (CCSK)','phs000467;TARGET: Neuroblastoma (NBL)','phs000468;TARGET: Osteosarcoma (OS)','phs000469;TARGET: Cell Lines and Xenografts (PPTP)','phs000470;TARGET: Kidney, Rhabdoid Tumor (RT)','phs000471;TARGET: Kidney, Wilms Tumor (WT)','phs000515;TARGET: Acute Myeloid Leukemia (AML), Induction Failure Subproject']
	Substudies['phs000286'] = ['phs000498;Jackson Heart Study Allelic Spectrum Project','phs000499;NHLBI Jackson Heart Study Candidate Gene Association Resource (CARe)']
	Substudies['phs000235'] = ['phs000527;CGCI: Burkitt Lymphoma Genome Sequencing Project (BLGSP)','phs000528;CGCI: HIV+ Tumor Molecular Characterization Project - Cervical Cancer (HTMCP - CC)','phs000529;CGCI: HIV+ Tumor Molecular Characterization Project - Diffuse Large B-Cell Lymphoma (HTMCP - DLBCL)','phs000530;CGCI: HIV+ Tumor Molecular Characterization Project - Lung Cancer (HTMCP - LC)','phs000531;CGCI: Medulloblastoma','phs000532;CGCI: Non-Hodgkin Lymphoma - Diffuse Large B-Cell Lymphoma (NHL - DLBCL)','phs000533;CGCI: Non-Hodgkin Lymphoma - Follicular Lymphoma (NHL - FL)','phs000534;CGCI: Office of Cancer Genomics (OCG) Grants - RC1 Human Lung Carcinogenesis']

	if Substudies.has_key(StudyIDx):

		print """
                          <div class='node mother'>											
                          <div class="node-info" style="DISPLAY:none">"""
		print ';'.join(Substudies[StudyIDx][0:])
							
		print """
                         </div>										
                         </div>
                      """
	else:
		pass
         ## ======= End added

def Retrieval(Qinput,Page,concept,debug,format1,limit,PhenTab,pagePhen):	

	page = int(Page)

	# Retrieve the storage index
	schema = Schema(IDName=TEXT(stored=True),path=ID(stored=True), title=TEXT(stored=True), desc=TEXT(stored=True), Type=TEXT(stored=True), cohort=NUMERIC(stored=True), inexclude=TEXT(stored=True),  platform=TEXT(stored=True), MESHterm=TEXT(stored=True), history=TEXT(stored=True), attributes=TEXT(stored=True), topic=TEXT(stored=True),disease=TEXT(stored=True),measurement=TEXT(stored=True),demographics=TEXT(stored=True),geography=TEXT(stored=True),age=TEXT(stored=True),gender=TEXT(stored=True),category=TEXT(stored=True),IRB=TEXT(stored=True),ConsentType=TEXT(stored=True),phen=TEXT(stored=True),phenID=TEXT(stored=True),phenDesc=TEXT(stored=True),phenName=TEXT(stored=True),phenCUI=TEXT(stored=True),phenMap=TEXT(stored=True), AgeMin=NUMERIC(stored=True), AgeMax=NUMERIC(stored=True), MaleNum=NUMERIC(stored=True), FemaleNum=NUMERIC(stored=True), OtherGenderNum=NUMERIC(stored=True), UnknownGenderNum=NUMERIC(stored=True), Demographics=TEXT(stored=True), phenType=TEXT(stored=True))

	storage = FileStorage(StoragePATH)
	ix = storage.open_index()

	# limit is Default as all fields
	mparser = MultifieldParser(["IDName","path","title","desc","Type","cohort","platform","topic","disease","measurement","demographics","geography","age","gender","category","phenID","phenName","phenDesc","phenCUI","phenMap","Demographics","phenType"], schema=ix.schema)

	# ============= SPECIAL CASES for query =============
	
	# If type nothing then Qinput will show the top studies
	if len(Qinput.strip())==0 or Qinput.find('*')==0:
		Qinput='top'
	
	# set up if Qinput=='top'
	if Qinput=='top':
		limit='StudyID'

	# set up if Qinput=='Search e.g. ...'
	if Qinput.find('Search e.g.')==0:
		try:
			Qinput = Qinput.split('Search e.g.')[1].strip()
		except:
			Qinput = ''

	# set up if Qinput=='Search ...'
	if Qinput.find('Search ')==0:
		try:
			Qinput = Qinput.split('Search ')[1].strip()
		except:
			Qinput = ''

	# set up if Qinput=='search ...'
	if Qinput.find('search ')==0:
		try:
			Qinput = Qinput.split('search ')[1].strip()
		except:
			Qinput = ''

	if debug==True:
		print Qinput

	# ===================================================

	# Limitation search
	if limit == 'Attribution':
		mparser = MultifieldParser(["attributes"], schema=ix.schema)
	elif limit == 'ConsentType':
		mparser = MultifieldParser(["ConsentType"], schema=ix.schema)
	elif limit == 'DataSet':
		mparser = MultifieldParser(["phen"], schema=ix.schema)
	elif limit == 'DataSetID':
		mparser = MultifieldParser(["phen"], schema=ix.schema)
	elif limit == 'DataSetName':
		mparser = MultifieldParser(["phen"], schema=ix.schema)
	elif limit == 'TopicDisease':
		mparser = MultifieldParser(["disease","topic"], schema=ix.schema)
	elif limit == 'Platform':
		mparser = MultifieldParser(["platform"], schema=ix.schema)
	elif limit == 'Geography':
		mparser = MultifieldParser(["demographics"], schema=ix.schema)
	elif limit == 'IRB':
		mparser = MultifieldParser(["IRB"], schema=ix.schema)
	elif limit == 'TopicDisease':
		mparser = MultifieldParser(["topic","disease"],schema=ix.schema)
	elif limit == 'Study':
		mparser = MultifieldParser(["title","IDName","desc"], schema=ix.schema)
	elif limit == 'Study Name':
		mparser = MultifieldParser(["title"], schema=ix.schema)
	elif limit == 'Study ID':
		mparser = MultifieldParser(["IDName"], schema=ix.schema)
	elif limit == 'Variable':
		mparser = MultifieldParser(["phen"], schema=ix.schema)
	elif limit == 'Variable ID':
		mparser = MultifieldParser(["phenID"], schema=ix.schema)
	elif limit == 'Variable Name':
		mparser = MultifieldParser(["phenName"], schema=ix.schema)
	elif limit == 'Variable Description':
		mparser = MultifieldParser(["phenDesc"], schema=ix.schema)

	# ------- SORT BY RELEVANCE  BMF25 algorithm ---
	with ix.searcher() as searcher:
		
		# ====================================================================
		# Retrieve the first page to show in the interface

		if Qinput.strip()[0]=='(' and Qinput.strip()[-1]==')':
			query_text = QueryAnalys(Qinput, False)
		elif Qinput[0]=='"' and Qinput[1]=='(' and Qinput[len(Qinput)-2]==')' and Qinput[len(Qinput)-1]=='"':
			query_text = QueryAnalys(Qinput, False)
		elif Qinput.find(':')>=0:
			query_text = QueryAnalys(Qinput, False)
		else:
			query_text = QueryAnalys(Qinput, concept)

		if Qinput!='top':
			if query_text.find(':')==-1 and query_text.find('"')==-1:
				query_text = '"' + query_text.strip() + '"'

		query = mparser.parse(query_text)

		if debug==True:
			print query

		results = searcher.search_page(query,page,pagelen=25,terms=True)

		# Added on May 2013, note that work only for concept-search
		if concept==True:
			hl1=query_text.split('"')
			hl2 = [hl1[item].strip() for item in xrange(1,len(hl1),2)]
			
			if len(hl1)==1:
				hl2=hl1			
		else:
			hl_temp = query_text.replace('AND',':::')
			hl_temp = hl_temp.replace('OR',':::')			
			hl2 = [item.strip() for item in hl_temp.split(':::')]

		if query_text.find(':')>0:
			hl_temp = query_text.replace('AND',':::')
			hl_temp = hl_temp.replace('OR',':::')
			hl2 = [item.strip() for item in hl_temp.split(':::')]

		# =====================================================================
		#### CHECK CONCEPT-BASED SEARCH IS OK, IF NOT THEN SKIP
		# Check if MetaMap are errors, default is concept-based
		if results.total==0:
			query_text = QueryAnalys(Qinput, False)
			query = mparser.parse(query_text)
			results = searcher.search_page(query,page,pagelen=25,terms=True)
		# ======================================================================

		# Get all Study ID 
		AllStudy={}
		resultALL = searcher.search(query,limit=None)

		for hit in resultALL:
			AllStudy[hit['path']]=1
			
		# ---------- SET UP RESULTS FRAGMENTS  -----------------
		results.fragmenter = highlight.SentenceFragmenter(charlimit=100000000)
		
		pagecount = results.pagecount
		if len(results) >= 0:
			if format1 =='html':
				print """<html>
        <head>
                <title>PhenDisco - Search Results</title>
		<link rel="icon" type="image/ico" href="./images/favicon.ico" />	
                <link href="./css/styles.css" rel="stylesheet" type="text/css">
		<script src="./js/jquery-1.8.2.min.js" language="JavaScript" type="text/javascript"></script>
		<script src="./js/utility.js" language="JavaScript" type="text/javascript"></script>
                <script src="./js/variableDefinitions.js" language="JavaScript" type="text/javascript"></script>
        	<script type="text/javascript" src="./lib/jquery.autocomplete.js"></script>
        	<script type="text/javascript" src="./lib/localdata.js"></script>

        	<meta name="robots" content="index, folow"/>
        	<link rel="stylesheet" type="text/css" href="./lib/jquery.autocomplete.css" />

        	<script type="text/javascript">
        	$().ready(function() {
                	$("#search-bar").focus().autocomplete(keywords);
        	});

(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-15356450-11', 'ucsd.edu');
  ga('send', 'pageview');

        </script>

	</head>

        <body>

		<!-- Front page main container -->
		<div id='main-container'>

                      <div id="help-tooltip" class='rounded shadow border'></div>
			<!-- main page header -->
			<div id='main-header' class='rounded shadow border'>

				<div class='top'>
					<a href='./index.php'><h1 class='alignleft'>Phenotype Discoverer</h1></a> 
					<div style="clear: both;"></div>
				</div>
                         
				<div class='body'>

	                          <a href='./'><img src="PhenDisco_Logo.jpg" alt="logo" height="87" width="80" style='float:left;'></a>

                                <div>

                                        <form method="get" action="./query.php" autocomplete="off">"""
				if Qinput!='top':
					print '<input id="search-bar" type="text" size="50" name="Fname" value=\'%s\'>' % query_text
				else:
					print '<input id="search-bar" type="text" size="50" name="Fname" value=\'%s\'>' % Qinput
				print """<input type="hidden" name="Page" value="1">
                                         <input type="hidden" name="PhenTab" value="0">
                                         <input type="hidden" name="phenPage" value="1">
                                         <button type="submit" class="search">Search</button>
                                        <input type="checkbox" name="search-checkbox"
"""
				if concept==True:
					print 'checked'
				print """
>Concept-based</br>
                                </div>
				<div>
					<a href='./AdvanceSearchPage.html'><button type='button' id='advanced-button' >Advanced Search</button></a><button type='button' id='limit-button' >Limits</button>
                                </div>
				</div>

				<div class='bottom'>
					<div class='container'>

						<img id='search-bar-help' class='alignright' src="./images/help.png" alt="help" height="24" width="24" border="0">
					</div>
					<div style="clear: both;"></div>
				</div>

			</div>

			<div id='limit-container' class='hide rounded shadow border'>
				
				<div class='top'>
					<h3 class ='alignleft'>Limits</h3>
				</div>

				<div class="body">

					<div class='container'>
						<label for="LimitsField">Field:</label>
						<select name="LimitField" size="1">
							<option selected="selected" value="AllFields">All Fields</option>
                                                        <option value="Attribution">Attribution</option>
							<option value="ConsentType">Consent Type</option>
							<option value="Dataset">Dataset</option>
							<option value="DatasetID">Dataset ID</option>
							<option value="DatasetName">Dataset Name</option>
							<option value="TopicDisease">Disease</option>
							<option value="Platform">Genotype Platform</option>
							<option value="Geography">Geography</option>
							<option value="IRB">IRB</option>
							<option value="Study">Study</option>
							<option value="Study ID">Study ID</option>
							<option value="Study Name">Study Name</option>
							<option value="Variable">Variable</option>
							<option value="Variable Description">Variable Description</option>
							<option value="Variable ID">Variable ID</option>
							<option value="Variable Name">Variable Name</option>						</select>
					</div>
				</div>

				<div class='bottom'> """

				print """
					<button type='button' class='alignright' id='limit-reset-button'>Reset</button>
					<div style="clear: both;"></div>
				</div>
                        </form>
			</div>

			<!-- Results Body content -->
			<div id='results-body' class='rounded shadow border'>
				
			<!-- Meta Data Options -->

				<!-- Navigation -->
				<div id='results-body-right-container'>

					<!-- Navigation START -->

					<!-- Getting Started -->
					<div class='container'>
						<div class='top'>
							<h2>Getting Started</h2>
						</div>
						<div class='body'>
							<ul>
								<li><a href="./">PhenDisco</a></li>
								<li><a href="./query.php?Fname=top&Page=1&PhenTab=1&phenPage=1&LimitField=StudyID&search-checkbox=on">Browse Top Level Studies</a></li>
	                                                        <li><a href="http://pfindr-data.ucsd.edu/_PhDVer1/Manual.pdf">Download Manual</a></li>
								<li><a href="http://pfindr-data.ucsd.edu/_PhDVer1/LDAM.png">Download PhenDisco domain model</a></li>
								<li><a href="http://pfindr-data.ucsd.edu/_PhDVer1/sdGapMR_3.25.13.owl">Download PhenDisco ontology</a></li>
							</ul>
						</div>
					</div>

					<hr>

					<!-- Important Links -->
					<div class='container'>
					</div>	

					<!-- Navigation ENDS -->

                                </div>

                                <!-- Results -->
                                <div id='results-body-left-container'>

                                        <div class='top'>
                                                <h2>Results</h2>
                                        </div>
                                        <div class='body'>"""

				startNum = 25*(page-1)+1
				if results.total > startNum + 25:
					endNum = startNum + 24
				else:
					endNum = results.total

				if Qinput.find('"')>=0:
					Qinput = Qinput.replace('"','%22')
					Qinput = Qinput.replace(' ','+')

				if concept==True:
					check1 = 'on'
				else:
					check1='off'
		
				print """
						<div class='container alignright spaced '>
							<button id="resultsDisplayButton">Display All</button>
						        <button id="resultsCheckButton">Check All</button>
			                                <form style="display:inline" action="check-form.php" method="post">
							<button type="submit">Export Selections</button>

						</div> """

				print """
					</div>

					<div style="clear: both;"></div>

					<div class='body'>
						<div id="tooltip" class='rounded shadow border'></div>
                                                <div id="nodeToolTip" class="rounded shadow border"></div>
						<div>
						    <ul id="tabs">"""
				if PhenTab==0:
					print """
						        <li class="target" id="tabs-1">Studies</li>
                                                        <li id="tabs-2">Variables</li>"""

				else:
					print """
						        <li id="tabs-1">Studies</li>
						        <li class="target" id="tabs-2">Variables</li>"""

				print """	    </ul>
						</div>
						<div class="wrapper1">
						<div class="div1">
						</div>
						</div>"""

				if PhenTab==0:
					print """
  					         <div id="tabs-1" class="wrapper2"> 
						"""
				else:
					print """
  					         <div id="tabs-1" class="wrapper2 hide">
						 """

				if startNum <= endNum:
					print 'Displaying: ' + str(startNum) + ' - '+str(endNum) +' of '+str(results.total) + ' studies.'
				
				if page<=1:
					print  '<p class="alignright spaced"><a href="query.php?Fname=%s&Page=%s&PhenTab=0&phenPage=1&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_stop_left.png" alt="help" height="16" width="16" border="0"></a> <a href="query.php?Fname=%s&Page=%s&PhenTab=0&phenPage=1&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_left.png" alt="help" height="16" width="16" border="0"></a>' %(Qinput,1,limit,check1,Qinput,1,limit,check1)
				else:
					print  '<p class="alignright spaced"><a href="query.php?Fname=%s&Page=%s&PhenTab=0&phenPage=1&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_stop_left.png" alt="help" height="16" width="16" border="0"></a> <a href="query.php?Fname=%s&Page=%s&PhenTab=0&phenPage=1&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_left.png" alt="help" height="16" width="16" border="0"></a>' %(Qinput,1,limit,check1,Qinput,page-1,limit,check1)
				
				print " 		Page " + str(Page) +" of " + str(pagecount)
				if page<=pagecount-1:
					print '<a href="query.php?Fname=%s&submit=Search&Page=%s&PhenTab=0&phenPage=1&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_right.png" alt="help" height="16" width="16" border="0"></a> <a href="query.php?Fname=%s&submit=Search&Page=%s&PhenTab=0&phenPage=1&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_stop_right.png" alt="help" height="16" width="16" border="0"></a></p>' %(Qinput,page+1,limit,check1,Qinput,pagecount,limit,check1)
				else:
					print '<a href="query.php?Fname=%s&submit=Search&Page=%s&PhenTab=0&phenPage=1&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_right.png" alt="help" height="16" width="16" border="0"></a> <a href="query.php?Fname=%s&submit=Search&Page=%s&PhenTab=0&phenPage=1&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_stop_right.png" alt="help" height="16" width="16" border="0"></a></p>' %(Qinput,pagecount,limit,check1,Qinput,pagecount,limit,check1)

				# Added on June 1, 2013
				print """
  			        <!-- Meta Data Options -->
				<div class='container alignleft'>
					<div class='top'>
						<h2>Study Display Options</h2>                                                
					</div>
					<div class='body'>
						<div id="display-options-help-tooltip" class='rounded shadow border'></div>
						<table id='filters'>
							<tr>
								<td><input type="checkbox" checked="true" class='filter' id="title" >Title</td>
								<td><input type="checkbox" checked="true" class='filter' id="embargoRelease" >Embargo Release</td>
								<td><input type="checkbox" class='filter' id="links" >Links</td>
								<td><input type="checkbox" class='filter' id="geography" >Geography</td>
							</tr>
							<tr>
								<td><input type="checkbox" checked="true" class='filter' id="studyType" >Study Type</td>
								<td><input type="checkbox" checked="true" class='filter' id="platform" >Platform</td>
								<td><input type="checkbox" class='filter' id="consentType" >Consent Type</td>
								<td><input type="checkbox" class='filter' id="irb" >IRB</td>
							</tr>
							<tr>
								<td><input type="checkbox" checked="true" class='filter' id="sampleSize" >Sample Size</td>
								<td><input type="checkbox" checked="true" class='filter' id="details" >Details</td>
								<td><input type="checkbox" class='filter' id="topicDisease" >Topic Disease</td>
							</tr>
						</table>		
					</div>
				</div>

				<div style="clear: both;"></div>
			<div class='bottom'>
						<div class='container alignleft'>
							<button type=button id='filter_apply' >Apply</button>
							<button type=reset id='filter_defaults' >Restore Defaults</button>
						</div>

						<div class='container alignright'>
							<img src="./images/help.png" id='display-options-help' alt="help" height="24" width="24" border="0">
						</div>

					</div>

				<div style="clear: both;"></div>

				<hr>

                                """

				# SHOWING THE RESULTS OF STUDIES

				if results.total==0:
					print "Your search returned 0 studies"

				else:
					# Print header table first
					print 	"""		<table id='results_table' class='results' >
								<thead>
                                                                        <th></th>
									<th class='title'>Title</th>
									<th class='embargoRelease'>Embargo Release</th>
									<th class='details'>Details</th>
									<th class='sampleSize'>Participants</th>
									<th class='studyType'>Type of Study</th>
									<th class='platform'>Platform</th>
									<th class='links'>Links</th>
									<th class='geography'>Geography</th>
									<th class='irb'>IRB</th>
									<th class='consentType'>Consent Type</th>
									<th class='topicDisease'>Topic Disease</th>
								</thead>
                                                                <tbody>
"""


			## DISPLAYING THE RESULTS

			# ===========================================================
			# Display studies
			# ===========================================================

			PhenOut = {}

			# Connect to the database
			# Relace MySQL username and password below		
			db = MySQLdb.connect("localhost", MySQLusername, MySQLpassword, "sdGaPv2")

			#records = Table(db, "Phenotypes")
			records = Table(db, "Phenotypes")
			Release1 = Table(db, "Release1")
			Study1 = Table(db, "Study")
			Abstraction1 = Table(db, "AbstractionNew")
			
			URL = 'http://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id='
			rank = 0
			num = 25*(page-1)
			for hit in results:

				# DEBUGGING
				if debug==True:
					print hit.matched_terms()
					
				MAXRANK = resultALL.score(0)
				scoreRank = results.score(rank)
				Rate = int(5*scoreRank/MAXRANK)
				if Rate == 0:
					Rate = 1
				rank = rank + 1

				PhenOut[num]=[]
				# ----- Print rank score ------
				URL1 = URL + hit["path"].split('.')[0]

				# If title not contain search keywords
				if len(hit.highlights("title"))==0: 
					if format1=='html':
						try:
							print "<tr id='results_tablerow_" + str(num) + "'>"
							print "<td><input id='results_tablerow_" + str(num) + "'" + ' type="checkbox"' + ' name="tags[]"' + ' value="' + hit["path"] +'"/>'
							# Added on Apr 29, 2013
							id_temp1=hit["path"].strip().split('.')[0]
							AddSubstudy(id_temp1)
							print '</td>'
							# End Added
							print '<td class="title"> <a href="'+ URL1 +'" target="_blank">'+ hit["path"] +'<br>'+ html2text.html2text(hit["title"]) + '</a>' 
							if Qinput!='top':
								print ' </td>'

							temp1 = html2text.html2text(hit.highlights("desc")).lower().replace('*','')
							found =any(item in temp1 for item in hl2)
							if len(hit.highlights("desc"))>0 and found==True:
								print '<td class="highlight1" style="DISPLAY:none">' + HighlightX(hl2,temp1) + '</td>'
							else:
								print '<td class="highlight1" style="DISPLAY:none">' + ' '.join(hit["desc"].split()[:30]) + '</td>'				
						except:
							print "<tr id='results_tablerow_" + str(num) + "'>"
							print "<td><input id='results_tablerow_" + str(num) + "'" + ' type="checkbox"' + ' name="tags[]"' + ' value="' + hit["path"] +'"/>'
							# Added on Apr 29, 2013
							id_temp1=hit["path"].strip().split('.')[0]
							AddSubstudy(id_temp1)
							print '</td>'
							# End added
							print '<td class="title"> <a href="' + URL1 + '" target="_blank">'+ hit["path"] +'<br>' + hit["title"] + '</a>'
							if Qinput!='top':
								print ' </td>'

							temp1 = html2text.html2text(hit.highlights("desc")).lower().replace('*','')
							found =any(item in temp1 for item in hl2)
							if len(hit.highlights("desc"))>0 and found==True:
								print '<td class="highlight1" style="DISPLAY:none">' + HighlightX(hl2,temp1) + '</td>'
							else:
								print '<td class="highlight1" style="DISPLAY:none">' + ' '.join(hit["desc"].split()[:30]) + '</td>'	
							pass
				else:
					# If title contain terms then highlight title
					terms = [text for fieldname, text in query.existing_terms(ix.reader(), phrases=True, expand=True) if fieldname == "title"]  

					if format1=='html':
						#pass
						try:
							print "<tr id='results_tablerow_" + str(num) + "'>"
							print "<td><input id='results_tablerow_" + str(num) + "'" + ' type="checkbox"' + ' name="tags[]"' + ' value="' + hit["path"] +'"/>'
							# Added on Apr 29, 2013
							id_temp1=hit["path"].strip().split('.')[0]
							AddSubstudy(id_temp1)
							print '</td>'
							# End added
							
							# Note: Convert HTML into text then match into terms
							temp1 = html2text.html2text(hit.highlights("title")).lower().replace('*','')
							found =any(item in temp1 for item in hl2)
							if found==True:
								print '<td class="title"> <a href="' + URL1 + '" target="_blank">' + hit["path"] +'<br>'+ HighlightX(hl2,hit["title"]) +'</a>'
							else:
								print '<td class="title"> <a href="' + URL1 + '" target="_blank">' + hit["path"] +'<br>'+ hit["title"] +'</a>'			

							if Qinput!='top':
								print ' </td>'

							temp1 = html2text.html2text(hit.highlights("desc")).lower().replace('*','')
							found =any(item in temp1 for item in hl2)
							if len(hit.highlights("desc"))>0 and found==True:
								print '<td class="highlight1" style="DISPLAY:none">' + HighlightX(hl2,temp1) + '</td>'
							else:
								print '<td class="highlight1" style="DISPLAY:none">' + ' '.join(hit["desc"].split()[:30]) + '</td>'	


						except:
							print "<tr id='results_tablerow_" + str(num) + "'>"
							print "<td><input id='results_tablerow_" + str(num) + "'" + ' type="checkbox"' + ' name="tags[]"' + ' value="' + hit["path"] +'"/>'

							# Added on Apr 29, 2013
							id_temp1=hit["path"].strip().split('.')[0]
							AddSubstudy(id_temp1)
							print '</td>'
							# End added
							print '<td class="title"> <a href="' + URL1 + '" target="_blank">'+ hit["path"] +'<br>' + hit["title"] + '</a>'
							if Qinput!='top':
								#print '<div class="rating"> <div class="rank' + str(Rate) + '"> </div></div>'
								print ' </td>'

							#print len(hit.highlights("desc"))
							temp1 = html2text.html2text(hit.highlights("desc")).lower().replace('*','')
							found =any(item in temp1 for item in hl2)
							if len(hit.highlights("desc"))>0 and found==True:
								#print '<td class="highlight1" style="DISPLAY:none">' + hit.highlights("desc") + '</td>'
								print '<td class="highlight1" style="DISPLAY:none">' + HighlightX(hl2,temp1) + '</td>'
							else:
								print '<td class="highlight1" style="DISPLAY:none">' + ' '.join(hit["desc"].split()[:30]) + '</td>'	

							pass
				if format1=='html':
					# Print HTML Table here

					# Print Embargo Release
					studyid1 = hit["path"].split('.')[0]
					print "<td class=\"embargoRelease\">"
					print ReformatOther(Release1.getitem(studyid1)[0][1]) 
					print "</td>"

					# Print VDAS
					print """<td class='details'>
											<div class='detailsImg v on alignleft'>
											</div>
											<div class='detailsImg d off alignleft'>
											</div>
											<div class='detailsImg a off alignleft'>
											</div>
											<div class='detailsImg s off alignleft'>
											</div>
											<div style="clear: both;"></div>"""
					
					print '<td class="PhenNum" style="DISPLAY:none">' + str(records.phencount(hit["path"].split('.')[0])) + '</td>'						
					print"""					</td>"""
					# Print sample size
					print "<td class=\"sampleSize\">"
					print hit["cohort"]
					print "</td>"

					# Print Study type
					print "<td class=\"studyType\">"
					print ReformatOther(hit["Type"]) 
					print "</td>"

					# Print Platform
					platform = Study1.getPlatform(studyid1)
					print "<td class=\"platform\">"
					print platform
					print "</td>"
					
					# Print Links
					print "<td class=\"links\">"
					print "n/a"
					print "</td>"

					# Print Geography
                                        print "<td class=\"geography\">"
					studyid1 = hit["path"].split('.')[0]
					geo = Abstraction1.getGeoNew(studyid1)
					print geo.upper()
					print "</td>"

					# Print IRB
					print "	 <td class='irb'>"
					IRBStr = Abstraction1.getIRBNew(studyid1)
					print IRBStr
					print "</td>"

					# Print Consent Type
					print "	 <td class='consentType'>"
					ConsentText = Abstraction1.getConsentNew(studyid1)
					print ConsentText
					print "</td>"
					
					# Print Topic Disease
					print "	 <td class='topicDisease'>"
					Disease1 = Abstraction1.getDiseaseNew(studyid1)
					print ReformatOther1(Disease1)
					print "</td>"

					print "</tr>"

				PhenOut[num].append((hit["path"],hit["title"],URL1,hit["desc"],records.phencount(hit["path"].split('.')[0]),records.datasetcount(hit["path"]), hit["Type"],hit["cohort"]))

				num = num + 1

			# ========================================================
			# ============= PRINT PHENOTYPE VARIABLES ================
			# ========================================================

			# Print header
			print """
                                                        </tbody>
							</table>
                                          </div>"""
			if PhenTab==0:
				print """
					  <div id="tabs-2" class='wrapper2 hide'>
					"""
			else:
				print """
					  <div id="tabs-2" class='wrapper2'>
					"""

			print """
                        <div id="definitionTooltip" class='rounded shadow border'></div>"""

			# ========================================================
			# Find all ID variables

			#print AllStudy
			IDListQuery = ' '
			for key in AllStudy:
				IDListQuery+=key.split('.')[0] + '|'

			IDListQuery = IDListQuery.strip('|').strip('"').strip() 
			PhenQuery="'" + '|'.join(hl2[0:]).replace('(','').replace(')','').replace('"','') + "'"
			records = Table(db, "Phenotypes1")

			try:
				# Work with extended search - concept search
				PhenNum1 = records.countPhenLimit(PhenQuery,IDListQuery)
				PhenOutS1 = records.getPhenLimit(PhenQuery,IDListQuery,pagePhen)
			except:
				PhenNum1=0
				PhenOutS1 = ''

			if Qinput=='top':
				PhenNum1 = records.countPhenAll()
				PhenOutS1 = records.getPhenAll(pagePhen)

			# ===============================================================================
			# SHOWING THE PHENOTYPE RESULTS
			# ===============================================================================

			if PhenNum1==0:
				print "Your search return 0 variables"
			else:

				print	"""			<table id='variables_table' class='variables' >
								<thead>
									<th></th>
									<th class='study'>Study</th>
									<th class='name'>Variable ID/Name</th>
									<th class='description'>Description</th>
									<th class='category'>Category</th>
								</thead>

								<tbody> """

			pagePhenMax = PhenNum1/25 + 1
			startNum1 = 25*(pagePhen-1)+1
			if PhenNum1 > startNum1 + 25:
				endNum1 = startNum1 + 24
			else:
				endNum1 = PhenNum1

			if PhenNum1>0:
				print 'Displaying: ' + str(startNum1) + ' - ' +str(endNum1) +' of '+str(PhenNum1) + ' variables.'

				if pagePhen<=1:
					print  '<p class="alignright spaced"><a href="query.php?Fname=%s&Page=%s&PhenTab=1&phenPage=%s&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_stop_left.png" alt="help" height="16" width="16" border="0"></a> <a href="query.php?Fname=%s&Page=%s&PhenTab=1&phenPage=%s&LimitField=%s&search-checkbox=%s&PhenTab=1"><img src="./images/arrow_left.png" alt="help" height="16" width="16" border="0"></a>' %(Qinput,1,1,limit,check1,Qinput,1,1,limit,check1)
				else:
					print  '<p class="alignright spaced"><a href="query.php?Fname=%s&Page=%s&PhenTab=1&phenPage=%s&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_stop_left.png" alt="help" height="16" width="16" border="0"></a> <a href="query.php?Fname=%s&Page=%s&PhenTab=1&phenPage=%s&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_left.png" alt="help" height="16" width="16" border="0"></a>' %(Qinput,1,1,limit,check1,Qinput,1,pagePhen-1,limit,check1)
				
				print " 		Page " + str(pagePhen) +" of " + str(pagePhenMax)
				
				if pagePhen<=pagePhenMax-1:
					print '<a href="query.php?Fname=%s&submit=Search&Page=%s&PhenTab=1&phenPage=%s&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_right.png" alt="help" height="16" width="16" border="0"></a> <a href="query.php?Fname=%s&submit=Search&Page=%s&PhenTab=1&phenPage=%s&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_stop_right.png" alt="help" height="16" width="16" border="0"></a></p>' %(Qinput,1,pagePhen+1,limit,check1,Qinput,1,pagePhenMax,limit,check1)
				else:
					print '<a href="query.php?Fname=%s&submit=Search&Page=%s&PhenTab=1&phenPage=%d&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_right.png" alt="help" height="16" width="16" border="0"></a> <a href="query.php?Fname=%s&submit=Search&Page=%s&PhenTab=1&phenPage=%s&LimitField=%s&search-checkbox=%s"><img src="./images/arrow_stop_right.png" alt="help" height="16" width="16" border="0"></a></p>' %(Qinput,1,pagePhenMax,limit,check1,Qinput,1,pagePhenMax,limit,check1)

			# ===============================================================================

			numPhen = 0
			num1 = 0			
			# Print out the Table if only the number of PhenNum1>0
			if PhenNum1>0:
				# Print variables
				while num1<=min(24,len(PhenOutS1)-1):
					print "<tr id='variables_tablerow_" + str(num1) + "'>"

					StudyID1 = PhenOutS1[num1][1]
					
					# Print out for checked form
					temp1p = '","'.join(PhenOutS1[num1][0:]).replace('>',' ')
					print '<td><input id="variables_tablerow_' + str(num1) + '" type="checkbox" name="tags[]" value=\'"' + temp1p + '"\'/></td>'

					URL1 = 'http://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id='				       				     
					# Print study name and title
					print '<td class="study"> <a href="' + URL1 + StudyID1.split('.')[0] + '" target="_blank" >'
					print StudyID1
					print '<br>'
					print Study1.getTitle(StudyID1)
					print "</a></td>"
				
					# Print Variable ID
					print "<td class='name'> <div class='id'>"

					VarLink='http://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/variable.cgi?study_id=' + StudyID1 + '&phv=' + str(int(PhenOutS1[num1][0].split('.')[0].split('phv')[1]))
					print '<a href="' + VarLink + '">' + PhenOutS1[num1][0] + '</a>'
					print "</div>"
				
					# Print Variable Name
					print "<div class='var_name'>"
					print PhenOutS1[num1][4]
					print "</div>"
					PhenInfo=''
					for PhenX in PhenOutS1[num1]:
						PhenX = PhenX.replace(';',' | ') + ';'
						PhenInfo+=PhenX

					print '<td class="highlight2" style="DISPLAY:none">' + PhenInfo + '</td>'
				
					# Print Description
					print "<td class='description'>"

					print HighlightX(hl2,unicode(PhenOutS1[num1][5]))
					print "</td>"		
				
					# Print Category
					print "<td class='category'>"
					phenCat1 = PhenOutS1[num1][-1].split(';')
					if len(phenCat1)>0:
						for phen1 in phenCat1:
							print '<span>' + phen1 + '</span><br><br>'
					print "</td></tr>"

					num1+=1
					
			# End form for checkbox
			print '<noscript><input type="submit"></noscript>  '
			print '</form>'

			# ===============================================
			# Print Footer
			# ===============================================
			print """
								</tbody>
							</table>
					    </div>
					</div>
				</div>
			<div style="clear: both;"></div>
			</div>

                      <div id='main-footer' class='rounded shadow border'>

                               <h4 id="dbv">Database Version: Last update July 1, 2013. Next update September 1, 2013&nbsp;</h4>
                               <br>
                               <h5 style="font-size:x-small;font-weight:normal"> PhenDisco is based on a mix of computer- and human-curated data. For this reason, it is not 100% accurate. There may be cases in which relevant studies are missed, as well as cases in which irrelevant studies are ranked highly. We encourage users to contact us at email hyk038@ucsd.edu when they encounter these kinds of problems. This work was funded by grant UH2HL108785 from NHLBI, NIH. </h5>
                                <div style="clear: both;"></div>
                        </div>

		</div>
	</body>
</html>		
                                """

		# In case using JSON format
		if format1=='json':
			ToJSON = json.dumps(PhenOut)
			print ToJSON

		# Disconnect database
		db.close()

def main():

	version = '1.0'
	debug = False
	Qinput = ''
	Page = 1
	concept = False
	format1 = 'html'
	limit = ''
	# PhenTab: False-0, True-1. True then display Phen Tab
	PhenTab = 0
	pagePhen = 1

	try:
		options, remainder = getopt.getopt(sys.argv[1:], 'i:p:z:l:t:fhdcvt', ['input=','page=','pagePhen=','limit=','tab=','format','help','debug','concept','version'])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt, arg in options:
	    if opt in ('-h', '--help'):
		    usage()
		    sys.exit()
	    elif opt in ('-i', '--input'):
		    Qinput = arg
	    elif opt in ('-p', '--page'):
		    Page = arg
	    elif opt in ('-p', '--page'):
		    Page = arg
	    elif opt in ('-z', '--pagePhen'):
		    pagePhen = int(arg)
	    elif opt in ('-c', '--concept'):
		    #print "Search with concept extension"
		    concept = True
	    elif opt in ('-f', '--format'):
		    format1 = 'json'
	    elif opt in ('-d', '--debug'):
		    debug = True
	    elif opt in ('-v', '--version'):
		    version = '1.0'
	    elif opt in ('-l', '--limit'):
		    limit = arg
	    elif opt in ('-t', '--tab'):
		    PhenTab = int(arg)
	    
	Retrieval(Qinput,Page,concept,debug,format1,limit,PhenTab,pagePhen)

if __name__=="__main__":
	main()		


