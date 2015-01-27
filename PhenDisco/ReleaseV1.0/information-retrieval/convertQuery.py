# 	$Id$	
# This is to convert query from Advanced Search form into basic form
# Written by Son Doan, May 2013

import os,sys
import getopt
from whoosh import index, store, fields
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from pyparsing import *
from TextMap import *

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
				#print ExtendedQ.getMapping(MetaMap)
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

# The purpose is to map text into query format from Whoosh
def Map(Qinput,concept):

	# Check if not correct syntax
	# IF THERE ARE NOT FIELDS
	if Qinput.find('[')==-1 or Qinput.find(']')==-1:
		return ('top',['top'])
	# ==========

	# Replace 'and','or'
	Qinput=Qinput.replace(' and',' ')
	Qinput=Qinput.replace(' or',' ')

	# Replace 'AND', 'OR'
	if Qinput.strip().split()[-1]=='AND' or Qinput.strip().split()[-1]=='OR':
		Qinput = ' '.join(Qinput.strip().split()[0:-1])
		
	#print Qinput

	map1 = Qinput
	map1 = map1.replace('[','|')
	map1 = map1.replace(']','|')
	map2 = map1.split('|')

	#print map2
	#print len(map2)

	terms=[]
	fields=[]
	conj = []

	for index1 in range(0,len(map2),2):
		if len(map2[index1].strip())>0:

			text = map2[index1]
			if text.find('AND')>=0:
				conj.append('AND')
				text_str = text.replace('AND','')
			elif text.find('OR')>=0:
				conj.append('OR')		
				text_str = text.replace('OR','')	
			else:
				text_str = text
	
			terms.append(text_str.strip())
			
			if index1+1<len(map2):
				fields.append(map2[index1+1])  						
						
	#print terms
	#print fields
	#print conj

	# Fix parenthesis, first remove all parenthesis
	for i in range(0,len(terms)):
		terms[i]=terms[i].replace("(",'').strip()
		terms[i]=terms[i].replace(")",'').strip()
	
	if terms[-1]=='':
		terms=terms[0:-1]

	#print "=========="	
	#print terms
	#print fields
	#print conj	

	# ==============================================
	# Convert to Whoosh query
	# ==============================================

	schema = Schema(IDName=TEXT(stored=True),path=ID(stored=True), title=TEXT(stored=True), desc=TEXT(stored=True), Type=TEXT(stored=True), cohort=NUMERIC(stored=True), inexclude=TEXT(stored=True),  platform=TEXT(stored=True), MESHterm=TEXT(stored=True), history=TEXT(stored=True), attributes=TEXT(stored=True), topic=TEXT(stored=True),disease=TEXT(stored=True),measurement=TEXT(stored=True),demographics=TEXT(stored=True),geography=TEXT(stored=True),age=TEXT(stored=True),gender=TEXT(stored=True),category=TEXT(stored=True),IRB=TEXT(stored=True),ConsentType=TEXT(stored=True),phen=TEXT(stored=True),phenID=TEXT(stored=True),phenDesc=TEXT(stored=True),phenName=TEXT(stored=True),phenCUI=TEXT(stored=True),phenMap=TEXT(stored=True), AgeMin=NUMERIC(stored=True), AgeMax=NUMERIC(stored=True), MaleNum=NUMERIC(stored=True), FemaleNum=NUMERIC(stored=True), OtherGenderNum=NUMERIC(stored=True), UnknownGenderNum=NUMERIC(stored=True), Demographics=TEXT(stored=True), phenType=TEXT(stored=True))

	## Convert into Advanced Search
	MainQuery=''
	count = 0
	for iQuery in terms:

		# Default MParser
		mparser = MultifieldParser(["IDName","path","title","desc","Type","cohort","platform","topic","disease","measurement","demographics","geography","age","gender","category","phenID","phenName","phenDesc","phenCUI","phenMap","Demographics","phenType"], schema)

		# Work with SampleSize
		if fields[count].find('SampleSize')>=0:
			MinSize = terms[count].split(',')[0].strip('(')
			MaxSize = terms[count].split(',')[1].strip(')')

			if MinSize.find('*')>=0:
				MinSizeN=0
			else:
				MinSizeN=int(MinSize) 
				
			if MaxSize.find('*')>=0:
				MaxSizeN=100000
			else:
				MaxSizeN=int(MaxSize)

			if count<len(terms)-1:
				MainQuery+= 'cohort:' + '[' + str(MinSizeN) + ' to ' + str(MaxSizeN) + '] ' + conj[count] + ' '
			else:
				MainQuery+= 'cohort:' + '[' + str(MinSizeN) + ' to ' + str(MaxSizeN) + ']'

		# Work with Age
		if fields[count]=='Age':
			#print terms
			MinAge = terms[count].strip().split(',')[0].strip('(')
			MaxAge = terms[count].strip().split(',')[1].strip(')')

			if MinAge.find('*')>=0:
				MinAgeN=0
			else:
				MinAgeN=int(MinAge) 
				
			if MaxAge.find('*')>=0:
				MaxAgeN=150
			else:
				MaxAgeN=int(MaxAge)

			if count<len(terms)-1:
				MainQuery+= 'AgeMin:' + '[' + str(MinAgeN) + ' to 150] ' + ' AND AgeMax:' + '[0 to ' + str(MaxAgeN) + '] ' + conj[count] + ' '
			else:
				MainQuery+= 'AgeMin:' + '[' + str(MinAgeN) + ' to 150] ' + ' AND AgeMax:' + '[0 to ' + str(MaxAgeN) + ']'
				
		# Work with StudySubject
		if fields[count].find('StudySubject')>=0:

			if count<=len(terms)-2:
				if fields[count]==fields[count+1]:
					if fields[count-1]!=fields[count]:
						MainQuery+= ' (Type:' + terms[count].strip() + ' ' +conj[count]
					else:
						MainQuery+=' Type:' + terms[count].strip() + ' ' +conj[count]
				else:
					MainQuery+=' Type:' + terms[count].strip() + ') ' +conj[count]
			else:
				if fields[count]==fields[count-1]:
					MainQuery+= ' Type:' + terms[count].strip() + ') '
				else:
					MainQuery+=' Type:' + terms[count].strip() + ' '

		# Work with Ethnicity
		if fields[count].find('Ethnicity')>=0:

			#print terms[count]
			if terms[count].find('Hispanic')==0:
				terms[count]='Hispanic'
			elif terms[count].find('Not Hispanic')==0:
				terms[count]='NonLatino'	
			else:
				terms[count]='Hispanic OR Demographics:NonLatino'

			if count<=len(terms)-2:
				if fields[count]==fields[count+1]:
					if fields[count-1]!=fields[count]:
						MainQuery+= ' (Demographics:' + terms[count].strip() + ' ' +conj[count]
					else:
						MainQuery+=' Demographics:' + terms[count].strip() + ' ' +conj[count]
				else:
					MainQuery+=' Demographics:' + terms[count].strip() + ') ' +conj[count]
			else:
				if fields[count]==fields[count-1]:
					MainQuery+= ' Demographics:' + terms[count].strip() + ') '
				else:
					MainQuery+=' Demographics:' + terms[count].strip() + ' '

		# Work with Platform
		if fields[count].find('Platform')>=0:
			if count<=len(terms)-2:
				if fields[count]==fields[count+1]:
					if fields[count-1]!=fields[count]:
						MainQuery+= ' (platform:"' + terms[count].strip() + '" ' +conj[count]
					else:
						MainQuery+=' platform:"' + terms[count].strip() + '" ' +conj[count]
				else:
					MainQuery+=' platform:"' + terms[count].strip() + '") ' +conj[count]
			else:
				if fields[count]==fields[count-1]:
					MainQuery+= ' platform:"' + terms[count].strip() + '") '
				else:
					MainQuery+=' platform:"' + terms[count].strip() + '" '

		# Work with DataAnalysisMethod
		if fields[count].find('DataAnalysisMethod')>=0:

			if count<=len(terms)-2:
				if fields[count]==fields[count+1]:
					if fields[count-1]!=fields[count]:
						MainQuery+= ' (platform:"' + terms[count].strip() + '" ' +conj[count]
					else:
						MainQuery+=' platform:"' + terms[count].strip() + '" ' +conj[count]
				else:
					MainQuery+=' platform:"' + terms[count].strip() + '") ' +conj[count]
			else:
				if fields[count]==fields[count-1]:
					MainQuery+= ' platform:"' + terms[count].strip() + '") '
				else:
					MainQuery+=' platform:"' + terms[count].strip() + '" '

		# Work with Machine
		if fields[count].find('Machine')>=0:

			if count<=len(terms)-2:
				if fields[count]==fields[count+1]:
					if fields[count-1]!=fields[count]:
						MainQuery+= ' (platform:"' + terms[count].strip() + '" ' +conj[count]
					else:
						MainQuery+=' platform:"' + terms[count].strip() + '" ' +conj[count]
				else:
					MainQuery+=' platform:"' + terms[count].strip() + '") ' +conj[count]
			else:
				if fields[count]==fields[count-1]:
					MainQuery+= ' platform:"' + terms[count].strip() + '") '
				else:
					MainQuery+=' platform:"' + terms[count].strip() + '" '

		# Work with SenquencingTechnique
		if fields[count].find('SequencingTechnique')>=0:

			if count<=len(terms)-2:
				if fields[count]==fields[count+1]:
					if fields[count-1]!=fields[count]:
						MainQuery+= ' (platform:"' + terms[count].strip() + '" ' +conj[count]
					else:
						MainQuery+=' platform:"' + terms[count].strip() + '" ' +conj[count]
				else:
					MainQuery+=' platform:"' + terms[count].strip() + '") ' +conj[count]
			else:
				if fields[count]==fields[count-1]:
					MainQuery+= ' platform:"' + terms[count].strip() + '") '
				else:
					MainQuery+=' platform:"' + terms[count].strip() + '" '

		# Work with IRB
		if fields[count].find('IRB')>=0:
			if terms[count]=='Not Required':
				terms[count]='No'
			if count<len(terms)-1:
				if fields[count]==fields[count+1]:
					if fields[count-1]!=fields[count]:
						MainQuery+=  '(IRB:' + terms[count].strip() + ' ' +conj[count]
					else:
						MainQuery+=  ' IRB:' + terms[count].strip() + ' ' +conj[count]
				else:
					MainQuery+= ' IRB:' + terms[count].strip() + ') ' +conj[count]
			else:
				if fields[count]==fields[count-1]:
					MainQuery+=  ' IRB:' + terms[count].strip() + ') '
				else:
					MainQuery+= ' IRB:' + terms[count].strip() + ' '

		# Work with Consent Type
		if fields[count].find('Consent')>=0:
			#print terms
			if terms[count]=='Unrestricted':
				terms[count]='No'
			if terms[count]=='Restricted':
				terms[count]='Restricted'
			if terms[count]=='Unspecified':
				terms[count]='Unspecified'

			if count<=len(terms)-2:
				if fields[count]==fields[count+1]:
					if fields[count-1]!=fields[count]:
						MainQuery+= ' (ConsentType:' + terms[count].strip() + ' ' +conj[count]
					else:
						MainQuery+=' ConsentType:' + terms[count].strip() + ' ' +conj[count]
				else:
					MainQuery+=' ConsentType:' + terms[count].strip() + ') ' +conj[count]
			else:
				if fields[count]==fields[count-1]:
					MainQuery+= ' ConsentType:' + terms[count].strip() + ') '
				else:
					MainQuery+=' ConsentType:' + terms[count].strip() + ' '

			#if count<len(terms)-1:
			#	MainQuery+= ' ConsentType:' + terms[count].strip() + ' ' +conj[count]
			#else:
			#	MainQuery+= ' ConsentType:' + terms[count].strip()

		# Work with Nationality
		if fields[count].find('Nationality')>=0:
			mparser = MultifieldParser(["Demographics","demographics"], schema)
			query= mparser.parse(unicode(iQuery))
			
			# Combine all queries together
			#if count<=len(terms)-2:
			#	MainQuery+=str(query) + ' ' +conj[count] + ' '
			#else:
			#	MainQuery+=str(query) 

			if count<=len(terms)-2:
				if fields[count]==fields[count+1]:
					if fields[count-1]!=fields[count]:
						MainQuery+= ' ( ' + str(query) + ' ' +conj[count]
					else:
						MainQuery+= ' ' + str(query) + ' ' +conj[count]
				else:
					MainQuery+=' ' + str(query) + ') ' +conj[count] 
			else:
				if fields[count]==fields[count-1]:
					MainQuery+= ' ' + str(query) + ') '
				else:
					MainQuery+=' ' + str(query) + ' '

		# Work with Gender
		if fields[count].find('Sex')>=0:
			if terms[count]=='Male':
				#if count<len(terms)-1:
				#	MainQuery+= ' MaleNum:[1 to] ' +conj[count]
				#else:
				#	MainQuery+= ' MaleNum:[1 to] '

				if count<=len(terms)-2:
					if fields[count]==fields[count+1]:
						if fields[count-1]!=fields[count]:
							MainQuery+=' (MaleNum:[1 to] ' +conj[count]
						else:
							MainQuery+=' MaleNum:[1 to] ' +conj[count]
					else:
						MainQuery+=' MaleNum:[1 to]) ' +conj[count]
				else:
					if fields[count]==fields[count-1]:
						MainQuery+=' MaleNum:[1 to]) ' 
					else:
						MainQuery+=' MaleNum:[1 to] '


			if terms[count]=='Female':
				#if count<len(terms)-1:
				#	MainQuery+= ' FemaleNum:[1 to] ' +conj[count]
				#else:
				#	MainQuery+= ' FemaleNum:[1 to] '

				if count<=len(terms)-2:
					if fields[count]==fields[count+1]:
						if fields[count-1]!=fields[count]:
							MainQuery+=' (FemaleNum:[1 to] ' +conj[count]
						else:
							MainQuery+=' FemaleNum:[1 to] ' +conj[count]
					else:
						MainQuery+=' FemaleNum:[1 to]) ' +conj[count]
				else:
					if fields[count]==fields[count-1]:
						MainQuery+=' FemaleNum:[1 to]) '
					else:
						MainQuery+=' FemaleNum:[1 to] '

			if terms[count]=='Both':
				#if count<len(terms)-1:
				#	MainQuery+= ' MaleNum:[1 to] AND FemaleNum:[1 to] ' +conj[count]
				#else:
				#	MainQuery+= ' MaleNum:[1 to] AND FemaleNum:[1 to] '

				if count<=len(terms)-2:
					if fields[count]==fields[count+1]:
						if fields[count-1]!=fields[count]:
							MainQuery+=' (MaleNum:[1 to] AND FemaleNum:[1 to] ' +conj[count]
						else:
							MainQuery+=' MaleNum:[1 to] AND FemaleNum:[1 to] ' +conj[count]
					else:
						MainQuery+=' MaleNum:[1 to] AND FemaleNum:[1 to]) ' +conj[count]
				else:
					if fields[count]==fields[count-1]:
						MainQuery+=' MaleNum:[1 to] AND FemaleNum:[1 to]) '
					else:
						MainQuery+=' MaleNum:[1 to] AND FemaleNum:[1 to] '


			if terms[count]=='Either':
				#if count<len(terms)-1:
				#	MainQuery+= ' MaleNum:[1 to] OR FemaleNum:[1 to] ' +conj[count]
				#else:
				#	MainQuery+= ' MaleNum:[1 to] OR FemaleNum:[1 to] '

				if count<=len(terms)-2:
					if fields[count]==fields[count+1]:
						if fields[count-1]!=fields[count]:
							MainQuery+=' (MaleNum:[1 to] OR FemaleNum:[1 to] ' +conj[count]
						else:
							MainQuery+=' MaleNum:[1 to] OR FemaleNum:[1 to] ' +conj[count]
					else:
						MainQuery+=' MaleNum:[1 to] OR FemaleNum:[1 to]) ' +conj[count]
				else:
					if fields[count]==fields[count-1]:
						MainQuery+=' MaleNum:[1 to] OR FemaleNum:[1 to]) '
					else:
						MainQuery+=' MaleNum:[1 to] OR FemaleNum:[1 to] '

		# Work with Study Design
		if fields[count].find('StudyDesign')>=0:
			
			if terms[count].find('Genome Wide Association Study')>=0:
				terms[count]= 'gwas'

			if terms[count]=='Case-Control Study':
				terms[count]= 'Case-Control'

			if terms[count]=='Cross Sectional Study':
				terms[count]= 'Cross Sectional'

			if terms[count]=='Double Blind Study':
				terms[count]= 'Double Blind'

			if terms[count]=='Interventional Studies':
				terms[count]='Interventional'

			if terms[count]=='Longitudinal Cohort Study':
				terms[count]='Longitudinal'

			if terms[count]=='Mendelian Randomized':
				terms[count]='Mendelian'

			if terms[count]=='Multicenter Study':
				terms[count]='Multicenter'

			if terms[count]=='Nested Case Control Study':
				terms[count]='Nested Case Control'

			if terms[count]=='Observational Studies':
				terms[count]='Observational'

			if terms[count]=='Partial Factorial Randomized Trial':
				terms[count]='Partial Factorial Randomized'

			if terms[count]=='Placebo Controlled Study':
				terms[count]='Placebo Controlled'

			if terms[count]=='Population Based Study':
				terms[count]='Population Based Control'

			if terms[count]=='Prospective Cohort Study':
				terms[count]='Prospective'

			if terms[count]=='Quantitative Cross Sectional Study':
				terms[count]='Quantitative Cross Sectional'

			if terms[count]=='Randomized Trial':
				terms[count]='Randomized'

			if terms[count]=='Phase 1':
				terms[count]='Phase1'
					
			if terms[count]=='Phase 2':
				terms[count]='Phase2'

			if terms[count]=='Phase 3':
				terms[count]='Phase3'

			if count<=len(terms)-2:
				#MainQuery+= ' Type:' + terms[count].strip() + ' ' +conj[count]
				if fields[count]==fields[count+1]:
					if fields[count-1]!=fields[count]:
						MainQuery+= ' (Type:' + terms[count].strip() + ' ' +conj[count]
					else:
						MainQuery+=' Type:' + terms[count].strip() + ' ' +conj[count]
				else:
					MainQuery+=' Type:' + terms[count].strip() + ') ' +conj[count]
			else:
				#MainQuery+= ' Type:' + terms[count].strip() + ' '
				if fields[count]==fields[count-1]:
					MainQuery+= ' Type:' + terms[count].strip() + ') '
				else:
					MainQuery+=' Type:' + terms[count].strip() + ' '
		#print MainQuery

		# Work with Race
		if fields[count].find('Race')>=0:

			#if terms[count]=='White':
			#	terms[count]='white OR Demographics:cacausian '

			if terms[count]=='Mixed Race':
				terms[count]='Multiple'

                        # Combine all queries together
                        if count<=len(terms)-2:
				#MainQuery+= ' Demographics:' + terms[count].strip() + ' ' +conj[count]
				if fields[count]==fields[count+1]:
					if fields[count-1]!=fields[count]:
						MainQuery+= ' (Demographics:' + terms[count].strip() + ' ' +conj[count]
					else:
						MainQuery+=' Demographics:' + terms[count].strip() + ' ' +conj[count]
				else:
					MainQuery+='Demographics:' + terms[count].strip() + ') ' +conj[count]
			else:
				if fields[count]==fields[count-1]:
					MainQuery+= ' Demographics:' + terms[count].strip() + ') '
				else:
					MainQuery+=' Demographics:' + terms[count].strip() + ' '

                        #else:
			#	MainQuery+= ' Demographics:' + terms[count].strip()

			#print MainQuery

		# ======================================
		# Work with Study
		if fields[count].strip()=='Study':

			mparser = MultifieldParser(["IDName","path","title","desc"], schema)
			query= mparser.parse(unicode(iQuery)) 

			# Combine all queries together
			if count<=len(terms)-2:
				MainQuery+=str(query) + ' ' +conj[count] + ' '
			else:
				MainQuery+=str(query) 

		# Work with Study Name
		if fields[count].find('Study Name')>=0:

			mparser = MultifieldParser(["title"], schema)
			query= mparser.parse(unicode(iQuery)) 

			# Combine all queries together
			if count<=len(terms)-2:
				MainQuery+=str(query) + ' ' +conj[count] + ' '
			else:
				MainQuery+=str(query) 

		# Work with Study ID
		if fields[count].find('Study ID')>=0:

			mparser = MultifieldParser(["IDName"], schema)
			query= mparser.parse(unicode(iQuery)) 

			# Combine all queries together
			if count<=len(terms)-2:
				MainQuery+=str(query) + ' ' +conj[count] + ' '
			else:
				MainQuery+=str(query) 

		# ======================================
		# Work with Variable
		if fields[count]=='Variable':
			mparser = MultifieldParser(["phenID","phenName","phenType","phenDesc"], schema)
			query= mparser.parse(unicode(iQuery))
 
			if count<len(terms)-1:
				MainQuery+= str(query) + ' ' +conj[count] + ' '
			else:
				MainQuery+= str(query)

		# Work with Variable Description
		if fields[count].find('Variable Desc')>=0:

			mparser = MultifieldParser(["phenDesc"], schema)
			query= mparser.parse(unicode(iQuery)) 

			# Combine all queries together
			if count<=len(terms)-2:
				MainQuery+=str(query) + ' ' +conj[count] + ' '
			else:
				MainQuery+=str(query) 

		# Work with Variable Name
		if fields[count].find('Variable Name')>=0:
			mparser = MultifieldParser(["phenName"], schema)
			query= mparser.parse(unicode(iQuery)) 

			# Combine all queries together
			if count<=len(terms)-2:
				MainQuery+=str(query) + ' ' +conj[count] + ' '
			else:
				MainQuery+=str(query) 

		# Work with Variable ID
		if fields[count].find('Variable ID')>=0:

			mparser = MultifieldParser(["phenID"], schema)
			query= mparser.parse(unicode(iQuery)) 

			# Combine all queries together
			if count<=len(terms)-2:
				MainQuery+=str(query) + ' ' +conj[count] + ' '
			else:
				MainQuery+=str(query) 					
		# ======================================
		# Work with All Fields
		if fields[count].find('All Fields')>=0:			
			# Added on May 21, 2013
			query = iQuery

			if concept==True:
				query_temp = QueryAnalys(query, concept)
			else:
				query_temp = query

			# Combine all queries together
			#if count<=len(terms)-2:
			#	MainQuery+=str(query) + ' ' +conj[count] + ' '
			#else:
			#	MainQuery+=str(query) 

			if count<=len(terms)-2:
				MainQuery+=query_temp + ' ' + conj[count] + ' '
			else:
				MainQuery+=query_temp + ' '

		count+=1

	return (MainQuery,terms)

def main():

	Qinput = ''
	concept=False

	try:
                options, remainder = getopt.getopt(sys.argv[1:], 'i:c', ['input=','concept'])
        except getopt.GetoptError:
                sys.exit(2)

	for opt, arg in options:
	       if opt in ('-i', '--input'):
                    Qinput = arg
	       elif opt in ('-c', '--concept'):
                    concept = True       

	print Map(Qinput,concept)[0]

if __name__=="__main__":
	main()		


