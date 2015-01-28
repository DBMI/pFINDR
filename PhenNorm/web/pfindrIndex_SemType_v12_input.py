# This script index free text and map into semantic model
# Written by Son Doan, Oct 2012
# Input: Phenotype dictionary, including studyID, dataset, analysis, etc.
# Output: A full mapped semantic model with associated studyID

# Example: 
# python pfindrIndex_v10.py  ./test/dbGaP.datOct2
# To avoid error of metamap, try:
# nohup python pfindrIndex_v10.py ../../data/new/dbGaP.datOct2 > ../../data/new/dbGaP.datOct2.map 2>/dev/null &

# CHANGES:
# April 09, 2013: Update new rules for demographics

import os,sys
import re
import subprocess as sub

Pheno = {}
def mapList(str, L):
	for iList in L:
		if str.find(iList)>=0:
			return 1
	return 0

def mapping(str1, Text):
	''' 
	Input is text and MetaMap outputs
	Output is semantic mapping model
	The model include: Theme_PCN,Theme_CUI,Event_PCN,Event_CUI,SOI_PCN,SOI_CUI
	PCN is for Preferred Concept Name.
	SOI is for Subject of Information
	'''

	# List of keywords of semantic types
	#RaceList = ['race','white','caucasian','asian','black','african','pacific','indian','american','french','british','italian','german']
	RaceList = ['race','white','caucasian','asian','black','african','pacific','indian','american','french','british','italian','german','african race','black african', 'black race', 'american indians', 'alaskan', 'ashkenazi jew', 'asians', 'african race', 'south asian', 'mexican','asian indian','caucasoid race', 'caucasians', 'chinese people', 'chinese','columbia race', 'miami race', 'european race', 'cuban', 'mexican', 'puerto ricans', 'central american', 'delaware indian', 'iowa indians', 'dominica islander race', 'german race','mediterranean','alaska native', 'anglos', 'samoan race', 'english race', 'american indians', 'alaska native', 'hawaiian population', 'other pacific islander', 'black race', 'african race', 'dominica islander race', 'arab race', 'mediterranean', 'puerto ricans', 'northern european', 'norwegians', 'russians', 'sephardic jew', 'other pacific islander', 'pacific islander americans', 'iowa indians', 'italians', 'japanese race', 'inca', 'circle indian', 'rampart indians', 'hawaiian population', 'filipino race', 'columbia race']
	EventList = ['dsyn','sosy','mobd','topp','diap','neop','cgab','anab','diap','hlca','resa','inbe','phsf','menp','orgf','neop','acab','biof','patf','clna','cgab','dora','inpo','fndg','qlco','lbpr','food','phsu','hops']
	EthnicList = ['ethnic','hispanic','not hispanic or latino', 'ethnic european','dominican - ethnicity','arab ethnic group','dominican - ethnicity']
	BirthList = ['date of birth','dob','birth year','year of birth']

	# Exclude list 
	ExList = ['white blood','white blood count']
	ExList1 = ['C1556084','C0596070','C0596227','C0687744','C1257890','C1705429','C0043210','C0086287','C0086582','C0683983','C0085756', 'C0687744','C1257890', 'C1705429', 'C0034510', 'C0019576', 'C0086528', 'C0086409', 'C0599755', 'C0015031','C0026193','C0239307','C1535514']
	ExList2 = ['marital', 'married', 'unmarried', 'single', 'separated', 'engaged', 'divorced', 'widowed', 'widow', 'widower', 'domestic partnership', 'partner', 'cohabit', 'civil union', 'sibling']
	ExCUIList2 = ['C0555047', 'C0087136', 'C1549113', 'C0682073', 'C0086170', 'C0206275', 'C0425152']
                   
	ModelMap = {}

	# Output of semantic model
	Theme = ''
	Theme_PCN = ''
	Theme_CUI = ''
	Event_PCN = ''
	Event_CUI = ''
	SOI_PCN = ''
	SOI_CUI = ''

	# Input for processing, i.e., MetaMap output

	Sents = Text.split('phrase')
	UttText = Sents[0].split('",')[0].split('\',')[1].strip('"')

	ModelMap[UttText,'Theme'] = []
	ModelMap[UttText,'Theme_PCN'] = []
	ModelMap[UttText,'Theme_CUI'] = []
	ModelMap[UttText,'Event_PCN'] = []
	ModelMap[UttText,'Event_CUI'] = []
	ModelMap[UttText,'SOI_PCN'] = []
	ModelMap[UttText,'SOI_CUI'] = []
	ModelMap[UttText,'SOI_SemType'] = []
	ModelMap[UttText,'Theme_SemType'] = []
	ModelMap[UttText,'Event_SemType'] = []

	#print "=================================================="
	#print "UttText: " + UttText
	for Sent1 in Sents[1:]:
		Phrase = Sent1.split('candidates')
		#print Phrase[0]
		#print Phrase[0].split(',')[0].split('(')[1]
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
				CandidateMatched = item.split(',')[2].lower().strip('\'')
				if item.find('\',[') >=0:
					CandidatePreferred = item.split('\',[')[0].split('\'')[-1].lower().strip('\'')
				else:
					CandidatePreferred = item.split(',')[3].lower()
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

				if mapList(CandidateMatched, RaceList)==1 and SemType.find('popg')>=0 and not mapList(Text.lower(), ExList):
					Theme = 'Race'
					if not Theme in ModelMap[(UttText,'Theme')]:
						ModelMap[(UttText,'Theme')].append(Theme)	

					#Theme_PCN = CandidatePreferred
					#Theme_CUI = CandidateCUI
					if not CandidatePreferred in ModelMap[(UttText,'Theme_PCN')]:
						ModelMap[(UttText,'Theme_PCN')].append(CandidatePreferred)			
						ModelMap[(UttText,'Theme_CUI')].append(CandidateCUI.strip('\''))
						ModelMap[(UttText,'Theme_SemType')].append(SemType.strip('\''))
								
				elif (mapList(CandidatePreferred, BirthList)==1) or (CandidatePreferred.find('age')>=0 and SemType.find('orga')>=0):
					Theme='Age'
					if not Theme in ModelMap[(UttText,'Theme')]:
						ModelMap[(UttText,'Theme')].append(Theme)	

					Theme_PCN = CandidatePreferred
					Theme_CUI = CandidateCUI
					if not Theme_PCN in ModelMap[(UttText,'Theme_PCN')]:
						ModelMap[(UttText,'Theme_PCN')].append(Theme_PCN)			
						ModelMap[(UttText,'Theme_CUI')].append(Theme_CUI.strip('\''))
						ModelMap[(UttText,'Theme_SemType')].append(SemType.strip('\''))

				elif (CandidatePreferred.find('gender')>=0 or CandidatePreferred.find('sex')>=0) and SemType.find('orga')>=0:
					Theme='Gender'
					if not Theme in ModelMap[(UttText,'Theme')]:
						ModelMap[(UttText,'Theme')].append(Theme)

					Theme_PCN = CandidatePreferred
					Theme_CUI = CandidateCUI
					if not Theme_PCN in ModelMap[(UttText,'Theme_PCN')]:
						ModelMap[(UttText,'Theme_PCN')].append(Theme_PCN)			
						ModelMap[(UttText,'Theme_CUI')].append(Theme_CUI.strip('\''))
						ModelMap[(UttText,'Theme_SemType')].append(SemType.strip('\''))

				elif mapList(CandidatePreferred, EthnicList)==1 and SemType.find('popg')>=0:
					Theme='Ethnicity'
					if not Theme in ModelMap[(UttText,'Theme')]:
						ModelMap[(UttText,'Theme')].append(Theme)

					Theme_PCN = CandidatePreferred
					Theme_CUI = CandidateCUI
					if not Theme_PCN in ModelMap[(UttText,'Theme_PCN')]:
						ModelMap[(UttText,'Theme_PCN')].append(Theme_PCN)
						ModelMap[(UttText,'Theme_CUI')].append(Theme_CUI.strip('\''))
						ModelMap[(UttText,'Theme_SemType')].append(SemType.strip('\''))

				# ==============================
				# Added new rules Apr 10, 2013
				# ==============================
                                elif mapList(CandidatePreferred, ExList2)==1 or mapList(CandidateCUI, ExCUIList2)==1:
					Theme = 'Marital Status'
					if not Theme in ModelMap[(UttText,'Theme')]:
						ModelMap[(UttText,'Theme')].append(Theme)

					Theme_PCN = CandidatePreferred
					Theme_CUI = CandidateCUI
					if not Theme_PCN in ModelMap[(UttText,'Theme_PCN')]:
						ModelMap[(UttText,'Theme_PCN')].append(Theme_PCN)
						ModelMap[(UttText,'Theme_CUI')].append(Theme_CUI.strip('\''))
						ModelMap[(UttText,'Theme_SemType')].append(SemType.strip('\''))

                               	elif mapList(CandidatePreferred, ['education','graduate'])==1 or mapList(CandidateCUI, ['C0682187', 'C0013658'])==1:
					Theme = 'Education Level'
					if not Theme in ModelMap[(UttText,'Theme')]:
						ModelMap[(UttText,'Theme')].append(Theme)

					Theme_PCN = CandidatePreferred
					Theme_CUI = CandidateCUI
					if not Theme_PCN in ModelMap[(UttText,'Theme_PCN')]:
						ModelMap[(UttText,'Theme_PCN')].append(Theme_PCN)
						ModelMap[(UttText,'Theme_CUI')].append(Theme_CUI.strip('\''))
						ModelMap[(UttText,'Theme_SemType')].append(SemType.strip('\''))

                               	elif mapList(CandidatePreferred, ['salary','income','wage'])==1:
					Theme = 'Income'
					if not Theme in ModelMap[(UttText,'Theme')]:
						ModelMap[(UttText,'Theme')].append(Theme)

					Theme_PCN = CandidatePreferred
					Theme_CUI = CandidateCUI
					if not Theme_PCN in ModelMap[(UttText,'Theme_PCN')]:
						ModelMap[(UttText,'Theme_PCN')].append(Theme_PCN)
						ModelMap[(UttText,'Theme_CUI')].append(Theme_CUI.strip('\''))
						ModelMap[(UttText,'Theme_SemType')].append(SemType.strip('\''))

				elif mapList(CandidatePreferred, ['working','employ','job','unemploy'])==1 or mapList(CandidateCUI, ["C0682295", "C0682294", "C2584322", "C2584323", "C0041674"])==1:
					Theme = 'Employment Status'
					if not Theme in ModelMap[(UttText,'Theme')]:
						ModelMap[(UttText,'Theme')].append(Theme)

					Theme_PCN = CandidatePreferred
					Theme_CUI = CandidateCUI
					if not Theme_PCN in ModelMap[(UttText,'Theme_PCN')]:
						ModelMap[(UttText,'Theme_PCN')].append(Theme_PCN)
						ModelMap[(UttText,'Theme_CUI')].append(Theme_CUI.strip('\''))
						ModelMap[(UttText,'Theme_SemType')].append(SemType.strip('\''))

					
				## ===================================
				# Mapping EVENT or topic
				# ===================================
				if mapList(SemType, EventList)==1:
					Event_PCN = CandidatePreferred
					Event_CUI = CandidateCUI
					# For multiple matches
					if not CandidatePreferred in ModelMap[UttText,'Event_PCN']:
						ModelMap[UttText,'Event_PCN'].append(CandidatePreferred)
						ModelMap[UttText,'Event_CUI'].append(CandidateCUI.strip('\''))
						ModelMap[(UttText,'Event_SemType')].append(SemType.strip('\''))
			
				# ===================================
				# Mapping SOI (Subject of Information)
				# ===================================                
	                        # Subject of Information
				if CandidateCUI.find('C0241889')>=0:
					ModelMap[UttText, 'SOI_PCN'].append('family')
					ModelMap[UttText, 'SOI_CUI'].append('C0015576')
					ModelMap[UttText, 'SOI_SemType'].append(SemType.strip('\''))
				elif (SemType.find('famg')>=0 or SemType.find('popg')>=0 or SemType.find('podg')>=0) and (mapList(CandidateCUI, ExList1)==0) and (mapList(CandidatePreferred,RaceList)==0) and (not CandidatePreferred in ModelMap[UttText,'SOI_PCN']):
						ModelMap[UttText, 'SOI_PCN'].append(CandidatePreferred)
						ModelMap[UttText, 'SOI_CUI'].append(CandidateCUI.strip('\''))
						ModelMap[(UttText,'SOI_SemType')].append(SemType.strip('\''))
	#print " ==== MAP === "
	if len(ModelMap[UttText, 'SOI_PCN']) == 0:
		ModelMap[UttText, 'SOI_PCN'] = ['study subject']
		ModelMap[UttText, 'SOI_CUI'] = ['C0681850']
		ModelMap[(UttText,'SOI_SemType')].append('grup')

	if mapList('Gender',ModelMap[UttText,'Theme'])==1:
		idx1 = ModelMap[UttText,'Theme'].index('Gender')
		ModelMap[UttText,'Theme_PCN'][idx1] = 'gender'
		ModelMap[UttText,'Theme_CUI'][idx1] = 'C0079399'
		ModelMap[(UttText,'Theme_SemType')].append('orga')

	if len(ModelMap[UttText,'Theme'])==0:
		ModelMap[UttText,'Theme'].append('NULL')
		ModelMap[UttText,'Theme_PCN'].append('NULL')
		ModelMap[UttText,'Theme_CUI'].append('NULL')
		ModelMap[(UttText,'Theme_SemType')].append('NULL')

	# Outputs for Excel file
	ModelTemplate = [UttText, ';'.join(ModelMap[UttText,'Theme'][0:]), ';'.join(ModelMap[UttText,'Theme_PCN'][0:]), ';'.join(ModelMap[UttText,'Theme_CUI'][0:]),';'.join(ModelMap[UttText,'Theme_SemType'][0:]), ';'.join(ModelMap[UttText,'Event_PCN']),';'.join(ModelMap[UttText,'Event_CUI']),';'.join(ModelMap[UttText,'Event_SemType']),';'.join(ModelMap[UttText,'SOI_PCN']),';'.join(ModelMap[UttText,'SOI_CUI']),';'.join(ModelMap[UttText,'SOI_SemType'])]

	mappings = ' ::: '.join(ModelTemplate[0:])
	#print str1.strip() + ' ::: ' + mappings
	showHTML(mappings)

"""
Show HTML for tables
"""
def showHTML(str1):

	#print "PhenID ::: StudyID ::: DATASETID ::: DATASET NAME ::: PHEN NAME ::: PHEN DESCRIPTION ::: PHEN TYPE ::: PHEN UNIT ::: PHEN MIN ::: PHEN MAX ::: NORMED ::: THEME ::: THEME PCN ::: THEME CUI ::: THEME STT ::: TOPIC PCN ::: TOPIC CUI ::: TOPIC SST ::: SOI PCN ::: SOI CUI ::: SOI SST"
	
	mappingsL = str1.split(' ::: ')

	#print mappingsL
	Desc = mappingsL[0]
	Theme = mappingsL[1]
	ThemePCN = mappingsL[2]
	ThemeCUI = mappingsL[3]
	ThemeSTT = mappingsL[4]
	TopicPCN = mappingsL[5]
	TopicCUI = mappingsL[6]
	TopicSTT = mappingsL[7]
	SOIPCN = mappingsL[8]
	SOICUI = mappingsL[9]
	SOISTT = mappingsL[10]

	# Show table
	print """

	<div class="body">

        <table id="results_table" class="results">
								<thead>
									<th class="title">Description</th>
<!--
									<th class="embargoRelease">Theme</th>
									<th class="details">Theme PCN </th>
									<th class="sampleSize">Theme CUI </th>
									<th class="studyType">Theme STT</th>
-->
									<th class="platform">Topic PCN </th>
									<th class="links">Topic CUI</th>
									<th class="geography">Topic STT</th>
									<th class="irb">SOI PCN</th>
									<th class="consentType">SOI CUI </th>
									<th class="topicDisease">SOI STT</th>
									<th class="topicDisease">Categories</th>
								</thead>
                                                                <tbody>

<tr id="results_tablerow_0">
<td class="title"> """
	print Desc
#	print """
#</td>
#
#<td class="embargoRelease"> """
#	print Theme
#	print """
#</td>
#<td class="details"> """

#	print ThemePCN
#	print """
#</td>
#<td class="PhenNum"> """
#	print ThemeCUI
#	print """
#</td>					
#<td class="sampleSize"> """
#	print ThemeSTT

	print """
</td>"""

	print """
<td class="studyType"> """

	if ThemePCN.find('NULL')>=0:
		print TopicPCN
	else:
		print ThemePCN + ';' +TopicPCN
	print """
</td>
<td class="platform">"""
	if ThemeCUI.find('NULL')>=0:
		print TopicCUI
	else:
		print ThemeCUI + ';'+ TopicCUI
	print """
</td>
<td class="links">"""
	if ThemeSTT.find('NULL')>=0:
		print TopicSTT
	else:
		print ThemeSTT + ';'+ TopicSTT
	print """
</td>
<td class="geography">"""
	print SOIPCN
	print """
</td>	 
<td class="irb">"""
	print SOICUI
	print """
</td>
<td class="consentType"> """

	print SOISTT
	print """
</td>
<td class="consentType"> """
	print ""
	print """</td>
</tr>
</tbody>
</table>
</div>
        """


def parse_text(TextInput):

    #Rule 0:  If a word has an uppercase letter occurring in it after a lowercase letter, split on that letter (e.g. "firstSecond" -> "first Second")        
    wordL = TextInput.split()
    Strx = ''
    for word in wordL:
        count = 0
        char1 = ''
        for c in word[1:]:
            if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                 count = count + 1
                 char1 = c
        if count==1 and not word[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            wordx=word.split(char1)
            wordi1=word.index(char1)
            word1 = word[0:wordi1]
            word2 = word[wordi1:len(word)]
            Strx = Strx + word1 + ' ' + word2
        else:
            Strx = Strx + ' ' + word
                        
    line1 = Strx.lower()
    # Rule 1: If string match 'mom'" then convert into 'mother' 
    if line1.find(' mom') >=0:
        line1 = line1.replace('mom','mother')

    # Rule 2: If string match 'dad'" then convert into 'father' 
    elif line1.find(' dad') >=0:
        line1 = line1.replace(' dad',' father')

    # Rule 3: If there are more than two letters before the hyphen, then split on the hyphen.  Otherwise, remove the hyphen (e.g. "X-Ray" -> XRay, "By-pass" -> bypass, "heart-attack" -> "heart attack", "First arm-other" ->  "First arm other"

    Str = ''
    wordL = line1.split()
    for word in wordL:
        #Str = Str + ' ' + word
        Hyphen = word.split('-')
        if len(Hyphen)==0:
            Str = Str + ' ' + word
        else:
            if len(Hyphen[0])<=2:
                Str = Str + ' ' + ''.join(Hyphen[0:])
            else:
                Str = Str + ' ' + ' '.join(Hyphen[0:])

    #print Str             
    # Rule 4: If a Word has a numeral in it, split at the last digit (e.g. Q13AGE -> Q13 AGE)
    line1 = Str
    wordL = line1.split()

    Str1 = ''
    for word in wordL:
        if re.match(r'\w+\d+\w+',word):
            #print "Matched"
            idx =0 
            #print word
            for i in range(len(word)-1,0,-1):
                if str(word[i]) in "0123456789":
                    idx = i
                    break
            word1 = word[0:idx+1]
            word2 = word[idx+1:len(word)]

            Str1 = Str1 + ' ' + word1 + ' ' + word2
        else:
            Str1 = Str1 + ' ' + word
    
    # Rule 5: If string match 'sex' then convert into 'gender' 
    if Str1.find('sex') >=0:
        Str1 = Str1.replace('sex','gender')

    # Rule 6: If string match 'male' and 'female' then convert into 'gender' 
    if Str1.find('sex [male or female]')>=0 :
        Str1 = Str1.replace('sex [male or female]','gender')

#    # Rule 7: If string match 'male' and 'gender' then convert into 'male gender' 
#    if Str1.find(' male ')>=0 and Str1.find('gender')>=0 and Str1.find(' female ')==-1:
#        Str1 = Str1.replace('male','')
#        Str1 = Str1.replace('female','')

   # Rule 8: If string match 'age parent' then convert into 'age of parent' 
    if Str1.find('age parent') >=0:
        Str1 = Str1.replace('age parent','age of parent')

   # Rule 9: If string match 'baby's sex' then convert into 'sex of baby' 
    if Str1.find('baby\'s sex') >=0:
        Str1 = Str1.replace('baby\'s sex','sex of baby')

   # Rule 10: If string match 'mother's age' then convert into 'age of mother' 
    if Str1.find('mother\'s age') >=0 :
        Str1 = Str1.replace('mother\'s age','age of mother')

   # Rule 10: If string match 'father's age' then convert into 'age of father' 
    if Str1.find('father\'s age') >=0 :
        Str1 = Str1.replace('father\'s age','age of father')

   # Rule 11: If string match 'onset' then convert into 'started' 
    if Str1.find('onset') >=0 :
        Str1 = Str1.replace('onset','started')


    # Remove '.','?'
    Str1 = Str1.replace('.',' ')
    Str1 = Str1.replace(';',' ')
    Str1 = Str1.replace('?',' ')
    Str1 = Str1.replace('!',' ')
    Str1 = Str1.replace('(',' ')
    Str1 = Str1.replace(')',' ')
    Str1 = Str1.replace(':',' ')
    Str1 = Str1.replace('#',' number ')
    Str1 = Str1.replace('/',' ')
    Str1 = Str1.replace('\'',' ')
    Str1 = Str1.replace('[',' ')
    Str1 = Str1.replace(']',' ')
    #Str1 = Str1.replace(',',' ')

    ## Correct some word
    #Str1 = Str1.replace('d eidentified','deidentified')
    #Str1 = Str1.replace('sub ject','subject')
    #Str1 = Str1.replace('s ubject','subject')
    #Str1 = Str1.replace('su bject','subject')
    #Str1 = Str1.replace('f ather','father')
    #Str1 = Str1.replace('fa ther','father')
    #Str1 = Str1.replace('fat her','father')
    #Str1 = Str1.replace('fath er','father')
    #Str1 = Str1.replace('fathe r','father')
    #Str1 = Str1.replace('mo ther','mother')
    #Str1 = Str1.replace('mot her','mother')
    #Str1 = Str1.replace('moth er','mother')
    #Str1 = Str1.replace('mothe r','mother')
    #Str1 = Str1.replace('g ender','gender')
    #Str1 = Str1.replace('ge nder','gender')
    #Str1 = Str1.replace('gen der','gender')
    #Str1 = Str1.replace('gend er','gender')
    #Str1 = Str1.replace('gende r','gender')
    #Str1 = Str1.replace('r ace','race')
    #Str1 = Str1.replace('ra ce','race')
    #Str1 = Str1.replace('rac e','race')
    #Str1 = Str1.replace('y ear','year')

    # Remove some words for MetaMap confusion
    Str1 = Str1.replace('utterance',' ')
    Str1 = Str1.replace('phrase',' ')
    Str1 = Str1.replace('candidates',' ')
    Str1 = Str1.replace('mappings',' ')

    # Include abbreviation
    Str1 = Str1 + ' '
    Str1 = Str1.replace(' mi ',' myocardial infarction ')
    Str1 = Str1.replace(' bp ',' blood pressure ')
    Str1 = Str1.replace(' bmi ',' body mass index ')
    Str1 = Str1.replace(' bpm ',' beats per minute ')
    Str1 = Str1.replace(' bw ', ' body weight')
    Str1 = Str1.replace(' dbp ', ' diastolic blood pressure')
    Str1 = Str1.replace(' hbp ', ' high blood pressure ')
    Str1 = Str1.replace(' htn ', ' hypertension ')
    Str1 = Str1.replace(' hr ', ' heart rate ')
    Str1 = Str1.replace(' ht ', ' height ')
    Str1 = Str1.replace(' lb ', ' pounds ')
    Str1 = Str1.replace(' rr ', ' respiration rate ')
    Str1 = Str1.replace(' sbp ', ' systolic blood pressure ')
    Str1 = Str1.replace(' temp ', ' temperature ')
    Str1 = Str1.replace(' tpr ', ' temperature, pulse, respiration ')
    Str1 = Str1.replace(' wt ', ' weight ')
    Str1 = Str1.replace(' yr ', ' year ')
    Str1 = Str1.replace(' vs ', ' vital signs ')
    Str1 = Str1.replace(' bmr ', ' basal metabolic rate ')
    Str1 = Str1.replace(' bg ', ' blood glucose ')
    Str1 = Str1.replace(' bgl ', ' blood glucose level ')
    Str1 = Str1.replace(' bld ', ' blood ')
    Str1 = Str1.replace(' bpm ', ' beats per minute ')
    Str1 = Str1.replace(' bs ', ' blood sugar ')
    Str1 = Str1.replace(' bsa ', ' body surface area ')
    Str1 = Str1.replace(' bsl ', ' blood sugar level ')
    Str1 = Str1.replace(' cbc ', ' complete blood count ')
    Str1 = Str1.replace(' cv ', ' cardiovascular ')
    Str1 = Str1.replace(' fbc ', ' full blood count ')
    Str1 = Str1.replace(' fbg ', ' fasting blood glucose ')
    Str1 = Str1.replace(' fbs ', ' fasting blood sugar ')
    Str1 = Str1.replace(' fhx ', ' family history ')
    Str1 = Str1.replace(' rbc ', ' red blood count ')
    Str1 = Str1.replace(' wbc ', ' white blood count ')

    return Str1.strip() + '\n'

def readinput(str1, input_file):
	fin = open(input_file,'r')
	text_file = fin.read()

	# Split into each input text
	items_utt = text_file.split('utterance')
	for item_utt in items_utt[1:]:
		mapping(str1, item_utt)
	fin.close()

def readinput2(input_text):

	#print input_text

	input_text2 = input_text.split('\n')

	for items in input_text2:
 
		# === Run with sanitized data
		item = items.split(':::')
		phenDesc = parse_text(item[0]).strip()

		# Need to remove all non-ascii chracter before go through MetaMap
		# Trick: First encode in unicode, then concert into in ascii 
		# Put it here

		cmd='echo "' + phenDesc + '"|/data/resources/MetaMap/public_mm/bin/metamap11v2 -q > /tmp/PhenNorm_tmp123'
		os.system(cmd)

		# === Run with whole data
		text1 = ' ::: '.join(item[0:]).strip()
	
		#  === Run with sanitized data
		#text1 = item[1]

		readinput(text1, '/tmp/PhenNorm_tmp123')		

def main():

	# print header 
	#print "PhenID ::: StudyID ::: DATASETID ::: DATASET NAME ::: PHEN NAME ::: PHEN DESCRIPTION ::: PHEN TYPE ::: PHEN UNIT ::: PHEN MIN ::: PHEN MAX ::: NORMED ::: THEME ::: THEME PCN ::: THEME CUI ::: THEME STT ::: TOPIC PCN ::: TOPIC CUI ::: TOPIC SST ::: SOI PCN ::: SOI CUI ::: SOI SST"

	readinput2(sys.argv[1])
if __name__=="__main__":
	main()

