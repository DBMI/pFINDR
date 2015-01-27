# This script is to map free text into MetaMap code
# and instantiate into semantic model
# Written by Son Doan, June 2012
# Input: MetaMap output file
# Output: A mapped semantic model

# Example: 
# Input is a text: "self reported description of ethnicity"
# Output of MetaMap:

import os,sys

Pheno = {}
PhenoTab = {}

def mapList(str, L):
	for iList in L:
		if str.find(iList)>=0:
			return 1
	return 0

def mapping(Text):
	''' 
	Input is text and MetaMap outputs
	Output is semantic mapping model
	The model include: Theme_PCN ,Theme_CUI, TOI_PCN, TOI_PCI, Event_PCN, Event_CUI, and LinkageConcept.
	PCN is for Preferred Concept Name.
	TOI is for Target of Information
	'''

	# List of keywords of semantic types
	RaceList = ['race','white','caucasian','asian','black','african','pacific','indian','american']
	EventList = ['dsyn','sosy','mobd','topp','diap','neop','cgab','anab','diap','hica','resa','inbe','phsf','orgf','hlca','neop','acty']
	LinkageList = ['note','diagnose','when','with','start','of ','at ','first']
	EthnicList = ['ethnic','hispanic']

	ModelMap = {}

	# Output of semantic model
	Theme = ''
	Theme_PCN = ''
	Theme_CUI = ''
	TOI_PCN = ''
	TOI_CUI = ''
	Event_PCN = ''
	Event_CUI = ''
	LinkageConcept = ''

	# Input for processing, i.e., MetaMap output

	Sents = Text.split('phrase')
	UttText = Sents[0].split('",')[0].split('\',')[1].strip('"')

	ModelMap[UttText,'Theme'] = 'NA'
	ModelMap[UttText,'Theme_PCN'] = ''
	ModelMap[UttText,'Theme_CUI'] = ''
	ModelMap[UttText,'TOI_PCN'] = ''
	ModelMap[UttText,'TOI_CUI'] =''
	ModelMap[UttText,'Event_PCN'] = ''
	ModelMap[UttText,'Event_CUI'] = ''
	ModelMap[UttText,'Linkage'] = ''

	#print "=================================================="
	#print "UttText: " + UttText
	for Sent1 in Sents[1:]:
		Phrase = Sent1.split('candidates')
		PhraseText = Phrase[0].split(',')[0].split('(')[1]
		#print "PhraseText : " + PhraseText
		for Sent2 in Phrase[1:]:
			Candidate = Sent2.split('mappings')
			CandidateString = Candidate[1].split('\n')[0]
			#print "CandidateString: " + CandidateString

			CandidateList = CandidateString.split('ev(')
			for item in CandidateList[1:]:
				#print "Candidate List: " + item
				CandidateCUI = item.split(',')[1]
				CandidateMatched = item.split(',')[2].lower()
				#CandidateMatched = item.split('\',')[1].split(',\'')[0]
				#CandidatePreferred = item.split(',')[3].lower()
				CandidatePreferred = item.split('\',[')[0].split('\'')[-1].lower()
				#CandidatePreferred = item.split('\',')[1].split(',\'')[0]
				SemType = item.split('[')[2].strip(',').strip(']')

				#print 'CandidateCUI : ' + CandidateCUI
				#print 'CandidateMatched : ' + CandidateMatched
				#print 'CandidatePreferred : ' + CandidatePreferred
				#print 'SemType : ' + SemType

				'''
				Now doing mapping into semantic model
				'''
				# ===================================
				# Mapping THEME
				# ===================================

				if mapList(CandidateMatched, RaceList)==1 and SemType.find('popg')>=0:
					Theme = 'Race'
					Theme_PCN = CandidatePreferred
					Theme_CUI = CandidateCUI
					ModelMap[(UttText,'Theme')] = Theme
					ModelMap[(UttText,'Theme_PCN')] = Theme_PCN			
					ModelMap[(UttText,'Theme_CUI')] = Theme_CUI
					#print " ============ MAPPING  ============"
					#print Theme
					#print Theme_PCN
					#print Theme_CUI
					
				elif CandidatePreferred.find('age')>=0 and SemType.find('orga')>=0 and ModelMap[(UttText,'Theme')] == 'NA':
					Theme='Age'
					Theme_PCN = CandidatePreferred
					Theme_CUI = CandidateCUI
					ModelMap[(UttText,'Theme')] = Theme
					ModelMap[(UttText,'Theme_PCN')] = Theme_PCN			
					ModelMap[(UttText,'Theme_CUI')] = Theme_CUI
					#print " ============ MAPPING  ============"
					#print Theme
					#print ModelMap[(UttText,'Theme')]
					#print Theme_PCN
					#print Theme_CUI

				elif (CandidatePreferred.find('gender')>=0 or CandidatePreferred.find('sex')>=0) and SemType.find('orga')>=0  and ModelMap[(UttText,'Theme')] == 'NA':
					Theme='Gender'
					Theme_PCN = CandidatePreferred
					Theme_CUI = CandidateCUI
					ModelMap[(UttText,'Theme')] = Theme
					ModelMap[(UttText,'Theme_PCN')] = Theme_PCN			
					ModelMap[(UttText,'Theme_CUI')] = Theme_CUI
					#print " ============ MAPPING  ============"
					#print Theme
					#print Theme_PCN
					#print Theme_CUI 

				elif mapList(CandidatePreferred, EthnicList)==1 and SemType.find('popg')>=0  and ModelMap[(UttText,'Theme')] == 'NA':
					Theme='Ethnicity'
					Theme_PCN = CandidatePreferred
					Theme_CUI = CandidateCUI
					ModelMap[(UttText,'Theme')] = Theme
					ModelMap[(UttText,'Theme_PCN')] = Theme_PCN			
					ModelMap[(UttText,'Theme_CUI')] = Theme_CUI
					#print " ============ MAPPING  ============"
					#print Theme
					#print Theme_PCN
					#print Theme_CUI 
				# ===================================
				# Mapping TOI (Target Of Information)
				# ===================================
				if (SemType.find('famg')>=0 or SemType.find('aggp')>=0):
					TOI_PCN = CandidatePreferred
					TOI_CUI = CandidateCUI
					ModelMap[UttText,'TOI_PCN'] = TOI_PCN
					ModelMap[UttText,'TOI_CUI'] = TOI_CUI
				# ===================================
				# Mapping EVENT
				# ===================================
				if mapList(SemType, EventList)==1:
					Event_PCN = CandidatePreferred
					Event_CUI = CandidateCUI
					ModelMap[UttText,'Event_PCN'] = Event_PCN
					ModelMap[UttText,'Event_CUI'] = Event_CUI
				# ===================================
				# Mapping Linkage
				# ===================================
				if mapList(CandidateMatched, LinkageList)==1:
					LinkageConcept = CandidateMatched
					ModelMap[UttText,'Linkage'] = LinkageConcept
	#print " ==== MAP === "
	if ModelMap[UttText,'TOI_PCN'] == '':
		ModelMap[UttText,'TOI_PCN'] = 'study subject'
		ModelMap[UttText,'TOI_CUI'] = 'C0681850'

	if ModelMap[UttText,'Theme'] == 'Gender':
		ModelMap[UttText,'Theme_PCN'] = 'gender'
		ModelMap[UttText,'Theme_CUI'] = 'C0079399'
				
	#for keys in ModelMap.keys():
	#	print ' '.join(keys[0:]) + ' : ' + ModelMap[keys]

	#print "FINAL PRINT"

	if ModelMap[UttText,'Theme']!='NA' and ModelMap[UttText,'Theme']!='' :
		#print "============= MAPPING RESULTS ==============="
		#print "<hr>"
		print '<table>'
		print '<tr>'
		#print "MAPPING RESULTS : "
		#print 'UttText : ' + UttText
		print '<td> <b> Theme </b> </td> <td> ' + ModelMap[UttText,'Theme'] + '</td>'
		print '</tr>'
		print '<tr>'
		print '<td> <b> Theme_PCN </b> </td> <td> ' + ModelMap[UttText,'Theme_PCN']+ '</td>'
		print '</tr>'
		print '<tr>'
		print '<td> <b> Theme_CUI </b> </td> <td>  ' + ModelMap[UttText,'Theme_CUI']+ '</td>'
		print '</tr>'
		print '<tr>'
		print '<td> <b> TOI_PCN </b> </td> <td>  ' + ModelMap[UttText,'TOI_PCN']+ '</td>'
		print '</tr>'
		print '<tr>'
		print '<td> <b> TOI_CUI </b> </td> <td>  ' + ModelMap[UttText,'TOI_CUI']+ '</td>'
		print '</tr>'
		print '<tr>'
		print '<td> <b> Event_PCN </b> </td> <td> ' + ModelMap[UttText,'Event_PCN']+ '</td>'
		print '</tr>'
		print '<tr>'
		print '<td> <b> Event_CUI </b> </td> <td>  ' + ModelMap[UttText,'Event_CUI']+ '</td>'
		print '</tr>'
		print '<tr>'
		print '<td> <b> Linkage </b> </td> <td> ' + ModelMap[UttText,'Linkage']+ '</td>'
		print '</table>'
		#print "============================================="
	else:
		print "Your input is not mapped into our demographic variables"

def readinput(input_file):
	fin = open(input_file,'r')
	text_file = fin.read()

	# Split into each input text
	items_utt = text_file.split('utterance')
	for item_utt in items_utt[1:]:
		mapping(item_utt)
	fin.close()

def main():
	readinput(sys.argv[1])

if __name__=="__main__":
	main()

