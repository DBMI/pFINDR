# This script cluster similar variables
# Written by Son Doan, January 2014
# Version 2.0 March 2014
# RUN:
# Example 
# python Similar_finding_v2.py -d 1 -o "LabTest" -i ../data/200test/500LabTests_random_KWL.txt2_cat

"""
RULE SETS:

1. Medical History
Type=Medical History
AND
SOI= {Study Subject, Participant, Patient}={C0030705, C0679646,   
AND
Topic_CUI (Var1) = Topic_CUI (Var2), where topic_CUIs in {dsyn, neop, sosy, acab, anab, biof, cgab, inpo, orgf, patf, phsf, mobd}
	
2. Demographics
Type=Demographics
AND
SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850
AND
Topic_CUI (Var1) = Topic_CUI (Var2)

3. Lab Test
Type= Lab Test
AND
SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850
AND
Topic_CUI (Var1) = Topic_CUI (Var2), where topic_CUIs in {lbpr}

Remove every remaining topics

4. Medication
Type= Medication
AND
SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
AND 
(Topic_CUI (Var1) = Topi_CUI (Var2), where topic CUI in {phsu}
OR
Keyword (Var1)=Keyword (Var2) = "medication")

5. Smoking History
Type= Smoking History
AND
SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
AND 
Keyword (Var1) & Keyword (Var2) are in {smoke, smoking, smoker, tobacco, cigarette, pipe, cigar, nicotine}

6. Healthcare Activity Finding
Prerequisite
	Type= Healthcare Activity Finding	
SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
Then compare keyword if has keyword in {medical care}
Keyword 1=Keyword 2
Then compare topic CUI in {hlca}
Var 1 CUI=Var2 CUI

7. Diagnostic Procedure
Prerequisite       
Type= Diagnostic Procedure	
SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
Then compare keyword  if has keyword in {ECG, electrocardiogram, t-wave, wave feature, QRS, RR interval, R wave, P wave, Q duration, S wave}
Keyword 1=Keyword 2
Then compare topic CUI in {diap}
Var 1 CUI=Var2 CUI

8. Therapeutic or Preventative Procedure
Prerequisite	
Type= Therapeutic or Preventative Procedure	
SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
Then compare topic CUI in {topp}
Var 1 CUI=Var2 CUI

"""

import os,sys
import getopt
import re

#  ==================================
# Global variables
#  ==================================

Group = {}

Group['Medical History']=[]
Group['Demographics']=[]
Group['Lab Tests']=[]
Group['Medication']=[]
Group['Smoking History']=[]
Group['Mental or Emotional Finding']=[]
Group['Drinking History']=[]
Group['Diagnostic Procedure']=[]
Group['Research Attributes']=[]
Group['Clinical Attributes']=[]
Group['Eating or Nutritional Finding']=[]
Group['Healthcare Activity Finding']=[]
Group['Daily or Recreational Activity']=[]
Group['Self-care Status']=[]
Group['Therapeutic or Preventive Procedure']=[]
Group['Substance Use History']=[]
Group['Healthcare Encounter']=[]

def readinput2(input_file, DescIdx, Select):

	Phen1 = {}
	PhenGroup = {}
	IDList = []
	CheckDup = {}

	#Select = 'All' # DEFAULT

	#Default DescIdx = 0, indicating the original PhenDesc is in field #0
	# DescIdx = 0

	fin = open(input_file,'r')
	for items in fin.readlines():
		#item = items.split(':::')		
		item = items.split('\t')

		# Add ID for each variable
		ID = item[0].strip()
		#print ID

		if not ID in IDList:
			IDList.append(ID)
			CheckDup[ID]=0
		else:
			CheckDup[ID]=1
		
		# Original PhenDesc
		PhenDesc = item[DescIdx].strip()
		
		# Normalized PhenDesc
		PhenText = item[DescIdx+1].strip()
		
		Theme = item[DescIdx + 2].strip()
		ThemePCN = item[DescIdx + 3]
		ThemeCUI = item[DescIdx + 4]
		ThemeSem = item[DescIdx + 5]
		
		TopicPCN = item[DescIdx + 6]
		TopicCUI = item[DescIdx + 7]
		TopicSem = item[DescIdx + 8]

		#print PhenDesc
		#print TopicCUI
		#print TopicSem	

		TopicCUI1 = TopicCUI.split(';')
		TopicSem1 = TopicSem.split(';')

		TopicCUI2 = []
		TopicSem2 = []
		for item1 in TopicSem1:
			if item1.find('lbpr')>=0:
				TopicSem2.append(item1)
				TopicCUI2.append(TopicCUI1[TopicSem1.index(item1)].strip())

		SOIPCN = item[DescIdx + 9]
		SOICUI = item[DescIdx + 10]
		SOISem = item[DescIdx + 11]

		#print SOICUI
		#print SOISem

		Category = item[-1].strip().split(';')
		#print item[0]
		#print Category

		TopicCUIL = sorted(TopicCUI2)
		SOI_Topic = SOICUI + ':' +'-'.join(TopicCUIL[0:])

		if len(Category[0])>0:
			for iCat in Category:
				#print iCat
				iCat = iCat.replace('Family','').strip()
				iCat = iCat.replace('Patient','').strip()
				if not Group.has_key(iCat):
					Group[iCat] = [item]
				else:
					if not item in Group[iCat] and CheckDup[ID]==0:
							Group[iCat].append(item)

	fin.close()

	#### GLOBAL VARIABLES ####

	##################################
	##### RULE FOR Medical History ###
	##################################
	"""
	1. Medical History
	Type=Medical History
	AND
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850)  
	AND
	Topic_CUI (Var1) = Topic_CUI (Var2), where topic_CUIs in {dsyn, neop, sosy, acab, anab, biof, cgab, inpo, orgf, patf, phsf, mobd, fndg}
	"""

	if Select == "MedHist" or Select=="All":
		print "MEDICAL HISTORY CLUSTERS"
		Group1 = Group['Medical History']
		List1 = ['dsyn', 'neop', 'sosy', 'acab', 'anab', 'biof', 'cgab', 'inpo', 'orgf', 'patf', 'phsf', 'mobd', 'fndg'] 
		cluster1(DescIdx,Group1,List1)

	##################################
	##### RULE FOR DEMOGRAPHICS ######
	##################################
	"""
	Demographics
	Type=Demographics
	AND
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
	AND
	Topic_CUI (Var1) = Topic_CUI (Var2)
	"""

	if Select == "Demo" or Select=="All":
		print "DEMOGRAPHICS CLUSTERS"
		Group1 = Group['Demographics']
		cluster(DescIdx,Group1)

	##################################
	##### RULE FOR LAB TESTS ######
	##################################
	"""
	3. Lab Test
	Type= Lab Test
	AND
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
	AND
	Topic_CUI (Var1) = Topic_CUI (Var2), where topic_CUIs in {lbpr}

	Remove every remaining topics

	"""

	if Select == "LabTest" or Select=="All":
		print "LAB TESTS CLUSTERS"
		Group1 = Group['Lab Tests']
		List1 = ['lbpr']
		cluster1(DescIdx,Group1,List1)

	##################################
	##### RULE FOR MEDICATIONS ######
	##################################
	"""
	4. Medication
	Type= Medication
	AND
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
	AND 
	(Topic_CUI (Var1) = Topi_CUI (Var2), where topic CUI in {phsu}
	OR
	Keyword (Var1)=Keyword (Var2) = "medication")
	"""

	if Select == "Med" or Select=="All":
		print "MEDICATION CLUSTERS"
		Group1 = Group['Medication']
		List1 = ['phsu']
		cluster1(DescIdx,Group1,List1)

	##################################
	##### RULE FOR Smoking History ###
	##################################
	"""
	Prerequisite
		Type= Smoking History
		SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850
	Then 
	Compare keyword if has keyword in {start*, onset, first, 1st}
	These variables are in the same cluster "Start"
	OR
	Compare keyword if has keyword in {stop*, last, quit*, end*, recency}
	These variables are in the same cluster "Last use"
	OR
	Compare keyword if has keyword in {amount, AMT, pack, /day, per day, per week, /week, /wk, per month, /month, how many, how much, pack-year, chain smoke, # of, number of, NO of, regularly, daily, regular, how often, days, times, TMS, frequency, duration, how long, years, # years, once a,}
	These variables are in the same cluster "Amount"
	OR
	Compare keyword if has keyword in {W/D, withdrawal}
	These variables are in the same cluster "Withdrawal"
	"""

	if Select == "Smoking" or Select=="All":
		print "SMOKING CLUSTERS"
		Group1 = Group['Smoking History']

		#print Group1

		Keywords = ['start', 'onset', 'first', '1st']
		cluster_synonyms(DescIdx,Group1,Keywords)

		Keywords1 = ['stop', 'last', 'quit', 'end', 'recency']
		cluster_synonyms(DescIdx,Group1,Keywords1)
		
		Keywords2 = ['amount', 'amt', 'pack', '/day', 'per day', 'days', 'per week', '/week', '/wk', 'per month', '/month', 'how many', 'how much', 'pack-year', 'pack year', 'chain smoke', '# of', 'number of', 'no of', 'regularly', 'daily', 'regular', 'how often', 'days', 'times', 'tms', 'frequency', 'duration', 'how long', 'year', 'years', '# years', 'once a']
		cluster_synonyms(DescIdx,Group1,Keywords2)
		
		Keywords3 = ['w/d', 'withdrawal']
		cluster_synonyms(DescIdx,Group1,Keywords3)

	###############################################
	###### RULE FOR Mental or Emotional Finding ###
	##############################################
	"""
	6. Mental or Emotional Finding
	Type= Mental or Emotional Finding
	AND
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
	AND 
	Topic_CUI (Var1) = Topic_CUI (Var2), where topic_CUIs in {menp}
	"""
	if Select == "MentalHealth" or Select=="All":
		print "Mental or Emotional Finding CLUSTERS"
		Group1 = Group['Mental or Emotional Finding']

		List1 = ['menp']
		ExCUIs = ['C1527305', 'C0013987', 'C0039869', 'C0596545', 'C0237607', 'C2911692']
		
		cluster1_exclude_CUIs(DescIdx,Group1,List1,ExCUIs)
	

	##############################################
	##### RULE FOR Heathcare Activity Finding ####
	##############################################
	"""
	Prerequisite
	Type= Healthcare Activity Finding	
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850
	Then compare keyword if has keyword in {'medical care', 'hospital', 'appointment', 'follow up','f/u', 'follow-up','visit', 'encounter', 'service'}
	Keyword 1=Keyword 2
	Then compare topic CUI in {hlca}
	Var 1 CUI=Var2 CUI
	"""

	if Select == "Activ" or Select=="All":
		print "HEALTHCARE ACTIVITIES FINDING CLUSTERS"
		Group1 = Group['Healthcare Activity Finding']

		Keywords = ['medical care','hospital', 'appointment', 'follow up','f/u', 'follow-up','visit', 'encounter', 'service']
		cluster_keywords(DescIdx,Group1,Keywords)

		List1 = ['hlca']
		cluster1(DescIdx,Group1,List1)


	#############################################
	##### RULE FOR Dignostic Procedure    #######
	#############################################
	"""
	Prerequisite
	Type= Diagnostic Procedure	
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850
	Then compare keyword  if has keyword in {ECG, electrocardiogram, t-wave, wave feature, QRS, RR interval, R wave, P wave, Q duration, S wave}
	Keyword 1=Keyword 2
	Then compare topic CUI in {diap}
	Var 1 CUI=Var2 CUI
	"""

	if Select == "Diag" or Select=="All":
		print "DIAGNOSTICS CLUSTERS"
		Group1 = Group['Diagnostic Procedure']

		Keywords = ['ecg', 'ekg' ,'electrocardiogram', 't-wave', 'wave feature', 'qrs', 'rr interval', 'r wave', 'p wave', 'q duration', 's wave', 'q wave', 't wave']
		#cluster_keywords(DescIdx,Group1,Keywords)
		cluster_synonyms(DescIdx,Group1,Keywords)

		List1 = ['diap']
		cluster1(DescIdx,Group1,List1)

	##############################################################
	##### RULE FOR Therapeutic or Preventative Procedure   #######
	##############################################################
	"""
	Prerequisite
	Type= Therapeutic or Preventative Procedure	
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850
	Then compare topic CUI in {topp}
	Var 1 CUI=Var2 CUI
	"""

	if Select == "Thera" or Select=="All":
		print " Therapeutic or Preventative Procedure CLUSTERS"
		Group1 = Group['Therapeutic or Preventive Procedure']

		List1 = ['topp']
		cluster1(DescIdx,Group1,List1)

	##############################################
	###### RULE FOR Drinking History       #######
	##############################################
	"""
	Prerequisite
		Type= Drinking History
		SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
	Then 
	Compare keyword if has keyword in {start*, onset, first, 1st}
	These variables are in the same cluster "Start"
	
	OR
	
	Compare keyword if has keyword in {stop*, last, quit*, end*, recency}
	These variables are in the same cluster "Last use"
	
	OR
	
	Compare keyword if has keyword in {amount, AMT, glass, bottle, can, /day, per day, per week, /week, /wk, per month, /month, how many, how much, # of, number of, NO of,  regularly, daily, regular, how often, days, times, TMS, frequency, duration, how long, years, # years, once a, FFQ}
	These variables are in the same cluster "Amount"
	OR
	
	Compare keyword if has keyword in {W/D, withdrawal}
	These variables are in the same cluster " Withdrawal"
	"""

	if Select == "Drinking" or Select=="All":
		print "DRINKING HISTORY CLUSTERS"
		Group1 = Group['Drinking History']

		Keywords = ['start', 'onset', 'first', '1st']
		cluster_synonyms(DescIdx,Group1,Keywords)

		Keywords1 = ['stop', 'last', 'quit', 'end', 'recency', 'stopped']
		cluster_synonyms(DescIdx,Group1,Keywords1)

		Keywords2 = ['amount', 'amt', 'glass', 'bottle', 'can', '/day', 'per day', 'per week', '/week', '/wk', 'per month', '/month', 'how many', 'how much', '# of', 'number of', 'no of', 'regularly', 'daily', 'regular', 'how often', 'days', 'times', 'tms', 'frequency', 'duration', 'how long', 'years', '# years', 'once a','ffq','ordinarily']
		cluster_synonyms(DescIdx,Group1,Keywords2)

		Keywords3 = ['w/d', 'withdrawal']
		cluster_synonyms(DescIdx,Group1,Keywords3)

	##############################################
	###### RULE FOR Substance Use History   #######
	##############################################
	"""
	Prerequisite
	Type= Substance Use History	
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850
	Then compare keyword if has keyword in {cocaine, opiate, stimulant, marijuana, pot, cannabis}
               Keyword 1 = Keyword 2
	Then compare topic CUI in {hops}
	       Var 1 CUI=Var2 CUI
	"""
	if Select == "Substance" or Select=="All":
		print "Substance Use History CLUSTERS"
		Group1 = Group['Substance Use History']


		# Rule for group 1
		Keywords = ['cocaine', 'opiate', 'opioid', 'heroin' , 'stimulant', 'marijuana', 'pot', 'cannabis']
		cluster_keywords(DescIdx,Group1,Keywords)

		Group2 = []
		for item in Group1:
			if not Match(Keywords,item[2]):
				Group2.append(item)

		List1 = ['hops']
		cluster1(DescIdx,Group2,List1)

		# Rule for group 2
		Keywords = ['start', 'onset', 'first', '1st']
		cluster_synonyms(DescIdx,Group1,Keywords)

		Keywords1 = ['stop', 'last', 'quit', 'end', 'recency']
		cluster_synonyms(DescIdx,Group1,Keywords1)

		Keywords2 = ['amount', 'amt', '/day', 'per day', 'per week', '/week', '/wk', 'per month', '/month', 'how many', 'how much', '# of', 'number of', 'no of', 'regularly', 'daily', 'regular', 'how often', 'days', 'times', 'tms', 'frequency', 'duration', 'how long', 'years', '# years', 'once a']
		cluster_synonyms(DescIdx,Group1,Keywords2)

		Keywords3 = ['w/d', 'withdrawal']
		cluster_synonyms(DescIdx,Group1,Keywords3)

	########################################################
	###### RULE FOR Daily or Recreational Activity   #######
	########################################################
	"""
	Prerequisite
	Type= Daily or Recreational Activity	
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850
	Then compare keyword if has keyword in {gait, walking, exercise, sports, workout, gambling, sleep, toilet, chore, stand, eat out}
        	Keyword 1=Keyword 2
	Then compare topic CUI in {dora}
	        Var 1 CUI=Var2 CUI
	"""
	if Select == "DailyActivity" or Select=="All":
		print "Daily or Recreational Activity CLUSTERS"
		Group1 = Group['Daily or Recreational Activity']

		#Keywords = ['gait', 'walking', 'exercise', 'sports', 'workout', 'gambling', 'sleep','toilet', 'chore', 'stand', 'eat out']
		#Keywords = ['walk', 'exercis', 'sport', 'workout', 'gambl', 'chore', 'eat out', 'gait', 'stand', 'sit', 'rest']
		#Keywords = ['walk', 'exercis', 'sport', 'workout', 'gambl', 'chore', 'eat out', 'gait', 'stand', 'rest', 'sleep']
		
		# Modified on July 14
		Keywords = ['gait', 'walk', 'exercis', 'sport', 'workout', 'gambl', 'sleep','chore', 'stand', 'eat out', 'eatout']

		cluster_keywords(DescIdx,Group1,Keywords)

		Keywords2 = ['sit', 'sits', 'sitted','sat', 'sitten', 'sitting']
		cluster_synonyms_exact(DescIdx,Group1,Keywords2)

		Group2 = []
		for item in Group1:
			if not Match(Keywords,item[2]):
				Group2.append(item)

		List1 = ['dora']
		cluster1(DescIdx,Group1,List1)

		#cluster1(DescIdx,Group2,List1)

	########################################################
	###### RULE FOR Eating or Nutritional Finding  #######
	########################################################
	"""
	Prerequisite
	Type= Eating or Nutritional Finding	
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850
	Then compare keyword if has keyword in {food, vitamin, nutrition, water}
	       Keyword 1=Keyword 2
	Then compare topic CUI in {food}
	       Var 1 CUI=Var2 CUI
	"""
	if Select == "Eating" or Select=="All":
		print "Eating or Nutritional Finding CLUSTERS"
		Group1 = Group['Eating or Nutritional Finding']

		Keywords = ['food', 'vitamin', 'nutrition', 'water']
		cluster_keywords(DescIdx,Group1,Keywords)

		List1 = ['food']
		cluster1(DescIdx,Group1,List1)

	########################################################
	###### RULE FOR Self-Care Status                   #####
	########################################################
	"""
	Prerequisite
	Type= Self-care Status	
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
	Then
	Compare keyword if has keywords in {bath, bathing}
	These variables are in the same cluster	
	OR	
	Compare keyword if has keyword in {self-care, dress*, groom*, bathing, eating, toilet*, hygiene}
	Keyword 1=Keyword 2	
	
	Note: Remove 'bathroom'

	"""
	if Select == "SelfCare" or Select=="All":
		print "SelfCare CLUSTERS"
		Group1 = Group['Self-care Status']

		Keywords1 = ['bath','bathing']
		cluster_synonyms_exact(DescIdx,Group1,Keywords1)

		Keywords2 = ['eating', 'eat', 'eats', 'ate', 'eaten']
		cluster_synonyms_exact(DescIdx,Group1,Keywords2)

		Keywords = ['self-care', 'dress', 'groom', 'toilet', 'hygiene']
		cluster_keywords(DescIdx,Group1,Keywords)

	########################################################
	###### RULE FOR Research Attribute                 #####
	########################################################
	"""
	Prerequisite
	Type=Research Attribute	
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
	Then
	Compare keyword if has keyword in {control group, control status, case, case control }
	These variables are in the same cluster
	
	Then
	Compare keyword if has keyword in {protocol}
	Keyword 1=Keyword 2
	
	Then else (for the remaining variable)
	Compare Topic_CUI in {resa}
	Var 1 CUI=Var 2 CUI
	"""
	if Select == "Research" or Select=="All":
		print "Research Attribute CLUSTERS"
		Group1 = Group['Research Attributes']

		Keywords = ['control group', 'control status', 'case', 'case control']
		cluster_synonyms(DescIdx,Group1,Keywords)

		Keywords2 = ['protocol']
		cluster_keywords(DescIdx,Group1,Keywords2)

		
		WordList1 = ['control group', 'control status', 'case', 'case control', 'protocol']

		Group2 = []
		for item in Group1:
			if not Match(WordList1,item[2]):
				Group2.append(item)

		List1 = ['resa']
		cluster1(DescIdx,Group2,List1)

	########################################################
	###### RULE FOR  Clinical Attribute                ####
	########################################################
	"""
	Prerequisite
	Type= Clinical Attribute	
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
	Then

	Compare keyword if has keyword in {heartbeat, heart rate, pulse, pulse deficit, pulse rate, vital sign}
	These variables are in the same cluster
	
	Then
	Compare keyword if has keyword in {blood pressure, diastolic blood pressure, diastolic pressure, resting pressure, systolic blood pressure, systolic pressure, vital sign}
	These variables are in the same cluster
	
	Then
	Compare keyword if has keyword in {body mass index, body weight, weight, body surface area, birth weight}
	These variables are in the same cluster
	
	Then
	Compare keyword if has keyword in {body temperature, temperature, vital sign}
	These variables are in the same cluster
	
	Then
	Compare keyword if has keyword in {pupil equality, pupil reactivity to light, pupil size}
	These variables are in the same cluster
	
	Then
	Compare keyword if has keyword in {respiration, respiration rate, respiration depth}
	These variables are in the same cluster
	
	Then
	Compare keyword if has keyword in {pulse oximetry, oxygen saturation}
	These variables are in the same cluster
	
	Then
	Compare keyword if has keyword in {adiposity, basal metabolic rate, body fat distribution. chest circumference, diameter, head circumference, height, pain, perimeter,  waist circumference, waist-hip ratio, gestational age} 
	Keyword 1=Keyword 2

	"""
	if Select == "Clinical" or Select=="All":
		print "Clinical Attribute CLUSTERS"
		Group1 = Group['Clinical Attributes']

		Keywords = ['heartbeat', 'heart rate', 'pulse', 'pulse deficit', 'pulse rate', 'vital sign']
		cluster_synonyms(DescIdx,Group1,Keywords)

		Keywords2 = ['blood pressure', 'bp' ,'diastolic blood pressure', 'diastolic pressure', 'diastolic', 'resting pressure', 'systolic blood pressure', 'systolic pressure', 'systolic', 'vital sign']
		cluster_synonyms(DescIdx,Group1,Keywords2)

		Keywords3 = ['body mass index','bmi', 'body weight', 'weight', 'body surface area', 'birth weight']
		cluster_synonyms(DescIdx,Group1,Keywords3)

		Keywords4=['pupil equality', 'pupil reactivity to light', 'pupil size']
		cluster_synonyms(DescIdx,Group1,Keywords4)

		Keywords5=['respiration', 'respiration rate', 'respiration depth']
		cluster_synonyms(DescIdx,Group1,Keywords5)

		Keywords6=['pulse oximetry', 'oxygen saturation']
		cluster_synonyms(DescIdx,Group1,Keywords6)

		Keywords7=['adiposity', 'basal metabolic rate', 'body fat distribution', 'chest circumference', 'diameter', 'head circumference', 'height', 'pain', 'perimeter',  'waist circumference', 'waist-hip ratio', 'gestational age','visual acuity']
		cluster_keywords(DescIdx,Group1,Keywords7)


	########################################################
	###### RULE FOR Healthcare Encounter               #####
	########################################################
	"""
	Healthcare Encounter
	Prerequisite
		Type= Healthcare Encounter	
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850
	Then	
	Compare keyword if has keyword in {ER visit, E.R. visit, emergency room, emergency department},
	These variables are in same group "ER visit"	
	OR	
	Compare keyword if has keyword in {hospital*, rehabilitation}
	Keyword 1=Keyword 2
	
	"""

	if Select == "Healthcare Encounter" or Select=="All":
		print "Healthcare Encounter CLUSTERS"
		Group1 = Group['Healthcare Encounter']

		Keywords = ['er visit', 'e.r. visit', 'emergency room', 'emergency department']
		cluster_synonyms(DescIdx,Group1,Keywords)

		Keywords2 = ['rehabilitation','hospital']
		cluster_keywords(DescIdx,Group1,Keywords2)

		#Keywords3 = ['hospital']
		#cluster_keywords(DescIdx,Group1,Keywords3)
		
"""
Check if Str1 contain a word in the wordlist
"""
def Match(WordList,Str1):
	for item in WordList:
		if Str1.lower().find(item.lower())>=0:
			return 1
	return 0

"""
Check if Str1 contain a word in the wordlist - tokenized by space
Cannot match first word since the case of "CIGS/day" where '/day' is a keyword matched
"""
def Match2(WordList,Str1):
	Str1List = Str1.split()
	for item1 in Str1List:
		for item in WordList:	
			if item1.lower().find(item.lower())>=0:
				return 1
	return 0

"""
Check if Str1 contain a word in the wordlist - tokenized by space
"""
def MatchStrict(WordList,Str1):

	#print "**********"
	#print WordList
	#print Str1
	#print "========="

	Str1List = Str1.lower().split()

	Str1List2 = []
	for xitem in Str1List:
		# Tokenize item
		if xitem.find('/')>=0:
			item1 = xitem.split('/')
		elif xitem.find('-')>=0:
			item1 = xitem.split('-')
		else:
			item1 = xitem.split()

		for item2 in item1:
			item3 = item2.strip().strip('?').strip('!').strip(',').strip('.').strip(';').strip('-').strip(':')
			Str1List2.append(item3)
	#print Str1
	#print Str1List2

	for item in WordList:			
		if item in Str1List2: 
			return 1
	return 0

"""
Cluster algorithms -- for other except Demographics: first compare STT, then compare CUI
"""

def cluster1(DescIdx,Group1,List1):

	Cluster = {}
	for i in range(0,len(Group1)):
		for j in range(i+1,len(Group1)):
			SOICUI = Group1[i][DescIdx + 10]
			#if SOICUI.find('C0681850')>=0 or SOICUI.find('C0030705')>=0 or SOICUI.find('C0679646')>=0:
			if 2>1:
				"""
				If the same STT - DescIdx + 8
				"""
				# =================================
				# Firstly, check Semantic
				# =================================
		
				# Check the case of multiple categories
				tempL1 = Group1[i][DescIdx + 8].strip().replace(',',';').split(';')
				tempL2 = Group1[j][DescIdx + 8].strip().replace(',',';').split(';')

				TopicSTT1 = set(tempL1)
				TopicSTT2 = set(tempL2)
				
				InterTopicSTT = list(TopicSTT1&TopicSTT2)

				#print InterTopicSTT

				JoinListL = list(set(InterTopicSTT)&set(List1))
				JoinList = set(InterTopicSTT)&set(List1)
				JoinListStr = ':'.join(list(set(InterTopicSTT)&set(List1))[0:])

				#print JoinList
				
				if len(JoinList)>0:

					# =================================
					# Secondly, check CUI
					# =================================

					##### CONVERT ITEM 1
					TopicCUI1L = Group1[i][DescIdx + 7].strip().split(';')
					TopicSTT1L = Group1[i][DescIdx + 8].strip().split(';')

					temp1=[]
					temp2=[]
					for item in TopicCUI1L:
						idx = TopicCUI1L.index(item)

						#print JoinListL
						#print TopicSTT1L[idx]
						
						if checkItem(TopicSTT1L[idx],JoinListL):
							temp1.append(item)
							temp2.append(JoinListL[0])
							
					TopicCUI1L = temp1
					TopicSTT1L = temp2
					
					#print "SECOND PHASE"
					#print TopicCUI1L
					#print TopicSTT1L

					##### CONVERT ITEM 2
					TopicCUI2L = Group1[j][DescIdx + 7].strip().split(';')
					TopicSTT2L = Group1[j][DescIdx + 8].strip().split(';')

					temp1=[]
					temp2=[]
					for item in TopicCUI2L:
						idx = TopicCUI2L.index(item)
						if checkItem(TopicSTT2L[idx],JoinListL):
							temp1.append(item)
							temp2.append(JoinListL[0])
							
					TopicCUI2L = temp1
					TopicSTT2L = temp2

					#print TopicCUI2L
					#print TopicSTT2L

					### DO JOINING

					InterTopicCUI = list(set(TopicCUI1L)&set(TopicCUI2L))
					InterTopicCUI1 =':'.join(InterTopicCUI[0:])

					#print InterTopicCUI

					if len(InterTopicCUI)>0:
						if not Cluster.has_key(InterTopicCUI1):
							Cluster[InterTopicCUI1]=[Group1[i],Group1[j]]
						else:
							if not Group1[i] in Cluster[InterTopicCUI1]:
								Cluster[InterTopicCUI1].append(Group1[i])
							if not Group1[j] in Cluster[InterTopicCUI1]:
								Cluster[InterTopicCUI1].append(Group1[j])

	for key in Cluster.keys():
		print key 
		for item in Cluster[key]:
			#print item[0] + '\t' + item[DescIdx]  + '\t' + item[DescIdx + 7] + '\t' + item[DescIdx + 8] 
			print '\t' + item[0] + '\t' + item[DescIdx]  + '\t' + item[DescIdx + 7] + '\t' + item[DescIdx + 8] 
		print "==============="


"""
Cluster algorithms -- for other except Demographics: first compare STT, then compare CUI
Exclude several CUIs
1 cluster is 1 CUIs, remove combination
"""

def cluster1_exclude_CUIs(DescIdx,Group1,List1,ExCUIs):

	Cluster = {}
	for i in range(0,len(Group1)):
		for j in range(i+1,len(Group1)):
			SOICUI = Group1[i][DescIdx + 10]
			#if SOICUI.find('C0681850')>=0 or SOICUI.find('C0030705')>=0 or SOICUI.find('C0679646')>=0:
			if 2>1:
				"""
				If the same STT - DescIdx + 8
				"""
				# =================================
				# Firstly, check Semantic
				# =================================
		
				# Check the case of multiple categories
				tempL1 = Group1[i][DescIdx + 8].strip().replace(',',';').split(';')
				tempL2 = Group1[j][DescIdx + 8].strip().replace(',',';').split(';')

				TopicSTT1 = set(tempL1)
				TopicSTT2 = set(tempL2)
				
				InterTopicSTT = list(TopicSTT1&TopicSTT2)

				#print InterTopicSTT

				JoinListL = list(set(InterTopicSTT)&set(List1))
				JoinList = set(InterTopicSTT)&set(List1)
				JoinListStr = ':'.join(list(set(InterTopicSTT)&set(List1))[0:])

				#print JoinList
				
				if len(JoinList)>0:

					# =================================
					# Secondly, check CUI
					# =================================

					##### CONVERT ITEM 1
					TopicCUI1L = Group1[i][DescIdx + 7].strip().split(';')
					TopicSTT1L = Group1[i][DescIdx + 8].strip().split(';')

					temp1=[]
					temp2=[]
					for item in TopicCUI1L:
						idx = TopicCUI1L.index(item)

						#print JoinListL
						#print TopicSTT1L[idx]
						
						if checkItem(TopicSTT1L[idx],JoinListL):
							temp1.append(item)
							temp2.append(JoinListL[0])
							
					TopicCUI1L = temp1
					TopicSTT1L = temp2
					
					#print "SECOND PHASE"
					#print TopicCUI1L
					#print TopicSTT1L

					##### CONVERT ITEM 2
					TopicCUI2L = Group1[j][DescIdx + 7].strip().split(';')
					TopicSTT2L = Group1[j][DescIdx + 8].strip().split(';')

					temp1=[]
					temp2=[]
					for item in TopicCUI2L:
						idx = TopicCUI2L.index(item)
						if checkItem(TopicSTT2L[idx],JoinListL):
							temp1.append(item)
							temp2.append(JoinListL[0])
							
					TopicCUI2L = temp1
					TopicSTT2L = temp2

					#print TopicCUI2L
					#print TopicSTT2L

					### DO JOINING

					InterTopicCUI = list(set(TopicCUI1L)&set(TopicCUI2L))
					InterTopicCUI1 =':'.join(InterTopicCUI[0:])

					#print "************"
					#print TopicCUI1L
					#print TopicCUI2L
					#print InterTopicCUI
					#print "************"
									       	
					if len(InterTopicCUI)>0:
						for xtem in InterTopicCUI:
							if not xtem in ExCUIs:
								if not Cluster.has_key(xtem):
									Cluster[xtem]=[Group1[i],Group1[j]]
								else:
									if not Group1[i] in Cluster[xtem]:
										Cluster[xtem].append(Group1[i])
									if not Group1[j] in Cluster[xtem]:
										Cluster[xtem].append(Group1[j])

	for key in Cluster.keys():
		print key 
		for item in Cluster[key]:
			#print item[0] + '\t' + item[DescIdx]  + '\t' + item[DescIdx + 7] + '\t' + item[DescIdx + 8] 
			print '\t' + item[0] + '\t' + item[DescIdx]  + '\t' + item[DescIdx + 7] + '\t' + item[DescIdx + 8] 
		print "==============="


"""
Check item in list or not
"""
def checkItem(Str1, List):
	
	for item in List:
		if Str1.find(item)>=0:
			return 1
	return 0

"""
Cluster algorithms -- for demographics
"""
def cluster(DescIdx,Group1):

	##################################
	##### RULE FOR DEMOGRAPHICS ######
	##################################
	"""
	Demographics
	Type=Demographics
	AND
	SOI= {Study Subject, Participant, Patient}={C0030705, C0679646, C0681850}
	AND
	Topic_CUI (Var1) = Topic_CUI (Var2)
	"""

	#Group1 = Group['Demographics']

	Cluster = {}

	for i in range(0,len(Group1)):
		for j in range(i+1,len(Group1)):
			SOICUI = Group1[i][DescIdx + 10]
			if SOICUI.find('C0681850')>=0 or SOICUI.find('C0030705')>=0 or SOICUI.find('C0679646')>=0:
				"""
				If the same Theme - DescIdx + 3
				"""
				
				Theme1 = set(Group1[i][DescIdx + 3].strip().split(';'))
				Theme2 = set(Group1[j][DescIdx + 3].strip().split(';'))
				
				InterTheme = list(Theme1&Theme2)
				InterTheme1 =':'.join(InterTheme[0:])
				
				if len(InterTheme)>0:
					if not Cluster.has_key(InterTheme1):
						Cluster[InterTheme1]=[Group1[i],Group1[j]]
					else:
						if not Group1[i] in Cluster[InterTheme1]:
							Cluster[InterTheme1].append(Group1[i])
						if not Group1[j] in Cluster[InterTheme1]:
							Cluster[InterTheme1].append(Group1[j])
	for key in Cluster.keys():
		print key
		for item in Cluster[key]:
			print '\t' + item[0] + '\t' + item[DescIdx] + '\t' + item[DescIdx + 3] 
		print "==============="

"""
Cluster algorithms -- for comparison of keywords instead
"""
def cluster_keywords(DescIdx,Group1,WordList):

	Cluster = {}

	for i in range(0,len(Group1)):
		SOICUI = Group1[i][DescIdx + 10]
		#if SOICUI.find('C0681850')>=0 or SOICUI.find('C0030705')>=0 or SOICUI.find('C0679646')>=0:
		if 2>1:
			"""
			Check keywords
			"""
			Desc = Group1[i][DescIdx]
			DescNorm = Group1[i][DescIdx + 1]
			for item in WordList:
				if DescNorm.find(item)>=0:
					if not Cluster.has_key(item):
						Cluster[item] = [Group1[i]]
					else:
						if not Group1[i] in Cluster[item]: 
							Cluster[item].append(Group1[i])

	for key in Cluster.keys():
		if len(Cluster[key])>1:
			print key
			for item in Cluster[key]:
				#print "\t" + item[DescIdx] 
				print "\t" + item[0] + '\t' + item[DescIdx] 
		print "==============="

"""
Synonym cluster algorithms 
"""
def cluster_synonyms(DescIdx,Group1,SynonymList):

	Cluster = {}
	KeySyn = SynonymList[0]

	for i in range(0,len(Group1)):
		SOICUI = Group1[i][DescIdx + 10]
		#if SOICUI.find('C0681850')>=0 or SOICUI.find('C0030705')>=0 or SOICUI.find('C0679646')>=0:
		# Change SOI check 
		if 2>1:
			"""
			Check synonyms
			"""
			Desc = Group1[i][DescIdx]
			DescNorm = Group1[i][DescIdx + 1]

			# Change back to DescNorm, change back on July 19 2014
			DescNorm = DescNorm.lower()

			# Deal with exception cases: "end*"
			DescNorm1 = DescNorm.split()
			EndList = ['end', 'ends', 'ending', 'ended','quit','quits','quitted','quitting','recency','stop','stops','stopped','stopping']
			LastList = ['last','lasts','lasted', 'lasting']

			# Changed in July 19, 2014
			# For class "stop"
			if 'stop' in SynonymList:

				# CHECK ENDLIST first
				if len(set(EndList).intersection(DescNorm1))>0:

					KeySyn='stop'
					if not Cluster.has_key(KeySyn):
						Cluster[KeySyn] = [Group1[i]]
					else:	
						if not Group1[i] in Cluster[KeySyn]: 
							Cluster[KeySyn].append(Group1[i])

				# Deal with exception cases: "last year/hour/month etc"
				# RULE:
                        	# except last {year, week, hour, number +hr, number+days, number +weeks, number +years, exam, night, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday}

				# Changed on July 19 2014
				# If contain term "last"
				elif len(set(LastList).intersection(DescNorm1))>0: 

					# case of last + time
					DescNorm1 = DescNorm.split()
					Lidx = DescNorm1.index('last')
					Next = ''
					if len(DescNorm1)>Lidx+2:
						Next = DescNorm1[Lidx+2]

					ExList = ['last year','last week','last hour','last exam', 'last night', 'last monday', 'last tuesday', 'last wednesday', 'last thursday', 'last friday', 'last saturday', 'last sunday']

					ExList2 = ['hr','hours','days','weeks','years']

					#print DescNorm
					#print Next
					#print Match(ExList, DescNorm)
					#print Match(ExList2, Next)

					# RULE: Exclude "last" + {years,month, number + days}
					# Ex. IF NOT "last year" AND NOT "last 30 days"
					if Match(ExList, DescNorm)==0 and Match(ExList2, Next)==0 :
						KeySyn='stop'
						if not Cluster.has_key(KeySyn):
							Cluster[KeySyn] = [Group1[i]]
						else:	
							if not Group1[i] in Cluster[KeySyn]: 
								Cluster[KeySyn].append(Group1[i])

			# For the remaining cases -- not "stop"
			else:
				KeySyn = SynonymList[0]
				ItemList = SynonymList
				DescNorm1 = DescNorm.split()

				#print DescNorm1
				#print ItemList
				#print set(ItemList).intersection(DescNorm1)

				for item in SynonymList:
					if DescNorm.find(item)>=0:
					#if len(set(ItemList).intersection(DescNorm1))>0:
						if not Cluster.has_key(KeySyn):
							Cluster[KeySyn] = [Group1[i]]
						else:
							if not Group1[i] in Cluster[KeySyn]: 
								#print Group1[i]
								Cluster[KeySyn].append(Group1[i])
	#print Cluster
	for key in Cluster.keys():
		if len(Cluster[key])>1:
			print key
			for item in Cluster[key]:
				#print "\t" + item[DescIdx] 
				print "\t" + item[0] + '\t' + item[DescIdx] 
		print "==============="

"""
Synonym cluster algorithms -- cluster with exact keyword matching 
"""
def cluster_synonyms_exact(DescIdx,Group1,SynonymList):

	Cluster = {}
	KeySyn = SynonymList[0]

	for i in range(0,len(Group1)):
		SOICUI = Group1[i][DescIdx + 10]
		#if SOICUI.find('C0681850')>=0 or SOICUI.find('C0030705')>=0 or SOICUI.find('C0679646')>=0:
		if 2>1:
			"""
			Check synonyms
			"""
			Desc = Group1[i][DescIdx]
			DescNorm = Group1[i][DescIdx + 1]

			## Match only with Desc, not DescNorm
			#DescNorm = Desc.lower()

			# Change back to DescNorm - noted on July 19, 2014
			DescNorm = DescNorm.lower()

			if MatchStrict(SynonymList, DescNorm):
				if not Cluster.has_key(KeySyn):
					Cluster[KeySyn] = [Group1[i]]
				else:
					if not Group1[i] in Cluster[KeySyn]: 
						Cluster[KeySyn].append(Group1[i])


	for key in Cluster.keys():
		if len(Cluster[key])>1:
			print key
			for item in Cluster[key]:
				#print "\t" + item[DescIdx] 
				print "\t" + item[0] + '\t' + item[DescIdx] 
		print "==============="


"""
Usage function
"""
def usage():
        print """"python [prog] -i <file> -d <number> -t <text> -o <selection>
where input can be one of those:
-i : input file
-d : deliminator number, e.g., 0, 5, 6. Default is 0, means no meta-data
OR 
-t : text input

-o : select which types to display

All - Display all
MedHist - Medical History
Demo  - Demographics 
LabTest - Lab Test
Med - Medication 
DrHist - Drinking History 
Smoking - Smoking History 
Mental - Mental or Emotional Finding
Activ - Healthcare Activity Finding
Diag - Diagnostic Procedure
Thera - Theurapeutic or Preventive Procedure
MentalHealth - Mental or Emotional Finding
SelfCare - Self-Care Status
Research - Research Attribute
Clinical - Clinical Attribute

        """

def main():

        try:
                options,remainder = getopt.getopt(sys.argv[1:], 'i:d:t:o:hdv', ['input=','deliminator=','text=','option=','help','debug','version'])

        except getopt.GetoptError:
                usage()
                sys.exit(2)
                
        delim = 0 # Default vallue, mean original PhenDesc start from number 0
        text_inp = ''
	select = 'All'

        for opt,arg in options:
                if opt in ('-h', '--help'):
                        usage()
                        sys.exit()
                elif opt in ('-i', '--input'):
                        Qinput = arg
                elif opt in ('-d', '--deliminator'):
                        delim = int(arg)
                elif opt in ('-t', '--text'):
                        text_inp = arg
                elif opt in ('-o', '--option'):
                        select = arg

	readinput2(Qinput,delim,select)

if __name__=="__main__":
	main()

