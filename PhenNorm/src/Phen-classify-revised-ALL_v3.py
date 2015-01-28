# This script classify free text into pre-defined classess
# Written by Son Doan, Feb 2013
# Modified on Jan 2014
# RUN:
# python [prog] -i <input file> 
# Example,
# python [prog] -i ./test1.out

import os,sys
import getopt
import re
import html2text

#  ==================================
# Global variables
#  ==================================

def mapList(str, L):
	for iList in L:
		if str.find(iList)>=0:
			return 1
	return 0

def mapLOINC(str1):
	if str1.find('^')>=0:
		return 1
	else:
		return 0

def readinput2(input_file,DescIdx):

	# Demographic keywords
	Demographics = ["marital","married","unmarried", "single", "separated", "engaged","divorced","widowed","widow","widower","domestic partnership","unmarried partner","cohabiting","civil union","education","graduate","occupation","birthplace","salary","relationship"]

	DemographicsIS = ["single","separated"]

	# Keep SNOMED-CT CUI finding codes
	SNOMED  = {}
	#SNOMED_source = '/home/sondoan/pfindr/VariableStandadization/phen-classification/data/MRCONSO_SNOMEDCT_finding_unique.ID'
	SNOMED_source = '/home/sodoan/pfindr/Normalization/Abbreviation/MRCONSO_SNOMEDCT_finding_unique.ID'
	f1 = open(SNOMED_source,'r')
	for item1 in f1.readlines():
		if len(item1.strip())>0:
			SNOMED[item1.strip()] = 1	
	f1.close()
	
	fin = open(input_file,'r')
	for items in fin.readlines():
		item = items.split(':::')
		
		#PhenDesc = item[0].strip()
	
		# Default DescIdx is 1, is the index of phenotype description 
		# DescIdx = 1
		PhenDesc = item[DescIdx].strip()
		if PhenDesc.find('<a href>')>=0:
			PhenDesc = html2text.html2text(PhenDesc)
		
		Theme = item[DescIdx + 1].strip()
		ThemePCN = item[DescIdx + 2]
		ThemeCUI = item[DescIdx + 3]
		ThemeSem = item[DescIdx + 4]
		
		TopicPCN = item[DescIdx + 5]
		TopicCUI = item[DescIdx + 6]
		TopicSem = item[DescIdx + 7]

		SOIPCN = item[DescIdx + 8]
		SOICUI = item[DescIdx + 9]
		SOISem = item[DescIdx + 10]
		
		# ==========================================
		# Remove LOINC code from TopicPCN
		TopicPCNL1 = TopicPCN.split(';')
		TopicCUIL1 = TopicCUI.split(';')	
		TopicSemL1 = TopicSem.split(';')

		tempPCN =''
		tempCUI=''
		tempSem =''
		iPCN = 0

		for iTopic in TopicPCNL1:
			#print iPCN
			#print len(iTopic.strip())
			if not mapLOINC(iTopic) and len(iTopic.strip())>0:
				tempPCN+= iTopic + ';'
				tempCUI+= TopicCUIL1[iPCN] + ';'
				tempSem+= TopicSemL1[iPCN] + ';'
				#print tempPCN
				#print tempCUI
			iPCN+=1

		TopicPCN = tempPCN.strip(';')
		TopicCUI = tempCUI.strip(';')
		TopicSem = tempSem.strip(';')

		# ==========================================
		# Remove Excluded CUIs 
		CUIEx = ["C0555047", "C0087136", "C1549113", "C0682073", "C0086170", "C0206275", "C0425152", "C0425164", "C0682187", "C0013658", "C0337664", "C0337676", "C0337677", "C0337679", "C0560184", "C2699517", "C1558950", "C0579133", "C0750479", "C0238884", "C1550043", "C0449255", "C2053594", "C0011900", "C1299586", "C1704632", "C0518459", "C0013798", "C0849912", "C0476610", "C1287845", "C2825142", "C1832071", "C0016928", "C0518461", "C1832073", "C2004062", "C1444656", "C0496675", "C0262926", "C1657765", "C0240320", "C2970713", "C1820407", "C1444648", "C1955473", "C1509143", "C0516977", "C1514241", "C0848632", "C1705236", "C1705179", "C2826292", "C2826292", "C0871269", "C0518462", "C0449416", "C1301826", "C0429103", "C0427693", "C1363945", "C0040210", "C1299582", "C1273517", "C0439540", "C1444647", "C0234766","C2926735","C0682295"]		

		# List of PRODUCT names
		CUIEx1 = ['C2926735','C0308903','C0308902','C0310197','C0722923','C2348077']

		TopicPCNL1 = TopicPCN.split(';')
		TopicCUIL1 = TopicCUI.split(';')	
		TopicSemL1 = TopicSem.split(';')

		iPCN = 0		
		for iCUI in TopicCUIL1:
			
			if mapList(iCUI, CUIEx1):
				TopicPCNL1.remove(TopicPCNL1[iPCN])
				TopicCUIL1.remove(iCUI)
				TopicSemL1.remove(TopicSemL1[iPCN])
				
			iPCN+=1

		TopicPCN = ';'.join(TopicPCNL1[0:]).strip()
		TopicCUI = ';'.join(TopicCUIL1[0:]).strip()
		TopicSem = ';'.join(TopicSemL1[0:]).strip()

		# ==========================================
		# Keep SNOMED-CT finding only  -- Filter by SNOMED CT, just keep finding in SNOMED-CT from UMLS findings
		
		# Keep Topic
		
		TopicPCNL1 = TopicPCN.split(';')
		TopicCUIL1 = TopicCUI.split(';')	
		TopicSemL1 = TopicSem.split(';')

		iPCN = 0		
		for iCUI in TopicSemL1:
			if iCUI.find('fndg')>=0:
			# Check if it exists in SNOMED List
				if not SNOMED.has_key(TopicCUIL1[iPCN].strip()):
					# Remove item from the list
					TopicSemL1.remove(iCUI)
					TopicCUIL1.remove(TopicCUIL1[iPCN])
					TopicPCNL1.remove(TopicPCNL1[iPCN])
			iPCN+=1

		TopicPCN = ';'.join(TopicPCNL1[0:]).strip()
		TopicCUI = ';'.join(TopicCUIL1[0:]).strip()
		TopicSem = ';'.join(TopicSemL1[0:]).strip()

		# ----------------------------
		phenCategory = []

		# RULE STARTING

		### Type: Demographic
		#if mapList(PhenDesc.lower(),Demographics) or len(Theme)>0:
		#if Theme!='NULL' and len(ThemePCN)>0:
		#	if not 'Demographics' in phenCategory:
		#		phenCategory.append('Demographics')

		# Modified on July 11, 2014
		Patient = ['C0030705', 'C0679646', 'C0681850']
		if Theme!='NULL' and len(ThemePCN)>0:
			if mapList(SOICUI,Patient):
				phenCategory.append('Demographics Patient')
			else:
				phenCategory.append('Demographics Family')			

		### Type: Medication
		MedPatient = ['C0030705', 'C0679646', 'C0681850']
		if mapList(SOICUI,MedPatient) and (mapList(TopicSem,['phsu']) or PhenDesc.lower().find('medication')>=0):
			if not 'Medication Patient' in phenCategory:
				phenCategory.append('Medication Patient')

		if not mapList(SOICUI,MedPatient) and (mapList(TopicSem,['phsu']) or PhenDesc.lower().find('medication')>=0):
			if not 'Medication Family' in phenCategory:
				phenCategory.append('Medication Family')

		### Type: Lab Test
		LabTest = ['C0030705', 'C0679646', 'C0681850']
		if mapList(SOICUI,LabTest) and mapList(TopicSem,['lbpr']):
			if not 'Lab Tests Patient' in phenCategory:
				phenCategory.append('Lab Tests Patient')

		if not mapList(SOICUI,LabTest) and mapList(TopicSem,['lbpr']):
			if not 'Lab Tests Family' in phenCategory:
				phenCategory.append('Lab Tests Family')

		### Type: Mental or Emotional Finding
		MentalFinding = ['menp']
		if mapList(SOICUI,LabTest) and mapList(TopicSem,MentalFinding):
			if not 'Mental or Emotional Finding' in phenCategory:
				phenCategory.append('Mental or Emotional Finding')

		if not mapList(SOICUI,LabTest) and mapList(TopicSem,MentalFinding):
			if not 'Mental or Emotional Finding Family' in phenCategory:
				phenCategory.append('Mental or Emotional Finding Family')

		### Type: Smoking History
		SmokingHistory = ["smoke",
			"smoking",
			"smoker",
			"tobacco",
			"cigarette",
			"pipe",
			"cigar",
			"nicotine"]

		if mapList(SOICUI,LabTest) and mapList(PhenDesc.lower(),SmokingHistory):
			if not 'Smoking History' in phenCategory:
				phenCategory.append('Smoking History')	

		if not mapList(SOICUI,LabTest) and mapList(PhenDesc.lower(),SmokingHistory):
			if not 'Smoking History Family' in phenCategory:
				phenCategory.append('Smoking History Family')	

		### Type: Drinking History
		DrinkingEx = ["C0337676", "C0337677", "C0337679"]
		DrinkingHistory = ["drink",
			"drinker",
			"alcohol",
			"liquor",
			"drunk",
			"beer",
			"wine",
			"drinking"]

		if mapList(SOICUI,LabTest) and PhenDesc.lower().find('drinking function')==-1:
			if  mapList(PhenDesc.lower(),DrinkingHistory) and not mapList(TopicCUI,DrinkingEx):
				if not 'Drinking History' in phenCategory:
					phenCategory.append('Drinking History')	

		if not mapList(SOICUI,LabTest) and PhenDesc.lower().find('drinking function')==-1 :
			if  mapList(PhenDesc.lower(),DrinkingHistory) and not mapList(TopicCUI,DrinkingEx):
				if not 'Drinking History Family' in phenCategory:
					phenCategory.append('Drinking History Family')	

		### Type: Substance Use History
		SubstanceUseHistory = ["cocaine",
			"opiate",
			"stimulant",
			"marijuana",
			"pot",
			"cannabis"]

		ExSubstance = ['smoke', 'smoking','smoker','tobacco','cigarette','pipe','cigar', 'nicotine']

		if mapList(SOICUI,LabTest):
			if  mapList(PhenDesc.lower(),SubstanceUseHistory) or mapList(TopicSem,['hops']):
				if not mapList(PhenDesc,ExSubstance):			
					if not 'Substance Use History' in phenCategory:
						phenCategory.append('Substance Use History')	

		if not mapList(SOICUI,LabTest):
			if  mapList(PhenDesc.lower(),SubstanceUseHistory) or mapList(TopicSem,['hops']):
				if not mapList(PhenDesc,ExSubstance):			
					if not 'Substance Use History Family' in phenCategory:
						phenCategory.append('Substance Use History Family')		

		### Type: Eating or Nutritional Finding 
		Eating = ["food",
			"vitamin",
			"nutrition",
			"water"]

		if mapList(SOICUI,LabTest):
			if mapList(TopicSem,['food']) or mapList(PhenDesc.lower(),Eating):
				if not 'Eating or Nutritional Finding' in phenCategory:
					phenCategory.append('Eating or Nutritional Finding')	

		if not mapList(SOICUI,LabTest):
			if mapList(TopicSem,['food']) or mapList(PhenDesc.lower(),Eating):
				if not 'Eating or Nutritional Finding Family' in phenCategory:
					phenCategory.append('Eating or Nutritional Finding Family')

		### Type: Self-care Status  
		Selfcare = ["selfcare",
			    "self care",
			    "self-care",
			    "dressing",
			    "grooming",
			    "bathing",
			    "eating",
			    "toileting",
			    "hygiene"]

		if mapList(SOICUI,LabTest):
			if mapList(PhenDesc.lower(),Selfcare):
				if not 'Self-care Status' in phenCategory:
					phenCategory.append('Self-care Status')	

		if not mapList(SOICUI,LabTest):
			if  mapList(PhenDesc.lower(),Selfcare):
				if not 'Self-care Status' in phenCategory:
					phenCategory.append('Self-care Status Family')


		### Type: Healthcare Activity Finding
		Healthcare =   ["medical care",
			        "hospital",
			        "appointment",
			        "follow up",
				"f/u",
				"follow-up",
				"visit",
				"encounter",
				"service"
				]

		#if mapList(SOICUI,LabTest):
		#	if mapList(TopicSem,['hlca']) or mapList(PhenDesc.lower(),Healthcare):
		#		if not 'Healthcare Activity Finding' in phenCategory:
		#			phenCategory.append('Healthcare Activity Finding')	

		#if not mapList(SOICUI,LabTest):
		#	if mapList(TopicSem,['hlca']) or  mapList(PhenDesc.lower(),Healthcare):
		#		if not 'Healthcare Activity Finding Family' in phenCategory:
		#			phenCategory.append('Healthcare Activity Finding Family')

		if mapList(PhenDesc.lower(),Healthcare):
			if not 'Healthcare Encounter' in phenCategory:
				phenCategory.append('Healthcare Encounter')	


		## Type: Therapeutic or Preventive Procedure
		if mapList(SOICUI,LabTest) and mapList(TopicSem,['topp']):
			if not 'Therapeutic or Preventive Procedure' in phenCategory:
				phenCategory.append('Therapeutic or Preventive Procedure')
		
		if not mapList(SOICUI,LabTest) and mapList(TopicSem,['topp']):
			if not 'Therapeutic or Preventive Procedure Family' in phenCategory:
				phenCategory.append('Therapeutic or Preventive Procedure Family')

		### Type: Clinical Attributes

		ClinicalAttL = ["gestational age",
			"basal metabolic rate",
			"body surface area",
			"blood pressure",
			"body mass index",
			"body weight",
			"diastolic blood pressure",
			"heart rate",
			"height",
			"respiration rate",
			"systolic blood pressure",
			"temperature",
			"temperature, pulse, respiration",
			"weight",
			"vital sign",
			"body temperature",
			"pulse rate",
			"systolic pressure",
			"diastolic pressure",
			"resting pressure",
			"pulse pressure",
			"heartbeat",
			"birth weight",
			"body fat distribution",
			"adiposity",
			"waist circumference",
			"waist-hip ratio",
			"head circumference",
			"chest circumference",
			"pulse",
			"respiratory depth",
			"pulse deficit",
			"pain",
			"oxygen saturation",
			"pupil size",
			"pupil equality",
			"pupil reactivity to light",
			"pulse oximetry",
			"diameter",
			"perimeter",
			"systolic",
			"diastolic",
			"visual acuity"]
		
		if mapList(SOICUI,LabTest):
			if mapList(PhenDesc.lower(),ClinicalAttL) and not mapList(PhenDesc.lower(),['weighting','weighted']):
				if not 'Clinical Attributes' in phenCategory:
					phenCategory.append('Clinical Attributes')
	
		if not mapList(SOICUI,LabTest):
			if mapList(PhenDesc.lower(),ClinicalAttL):
				if not 'Clinical Attributes Family' in phenCategory and not mapList(PhenDesc.lower(),['weighting','weighted']):
					phenCategory.append('Clinical Attributes Family')

		### Type: Research Attributes
		ResearchTerms = ["control group",
				"control status",
				"case",
				"case control",
				"case-control",
				"protocol"
			]
		
		if mapList(SOICUI,LabTest):
			if  mapList(PhenDesc.lower(),ResearchTerms) or mapList(TopicSem,['resa']):
				if not 'Research Attributes' in phenCategory:
					phenCategory.append('Research Attributes')

		if not mapList(SOICUI,LabTest):
			if  mapList(PhenDesc.lower(),ResearchTerms) or mapList(TopicSem,['resa']):
				if not 'Research Attributes Family' in phenCategory:
					phenCategory.append('Research Attributes Family')


		## REMOVE CO-OCCURENCE Types, e.g., Daily or Recreation Activity doesnot occurs with Clinical Attributes, Lab Test, Diagnostic Procedure

		# If Diagnostic Procedure co-occurs with Clinical Attribute, then ignore.
		### Type: Diagnostic Procedure
		Diagnosis = ['ecg',
			     'electrocardiogram',
			     't wave',
			     't-wave',
			     'wave feature',
			     'qrs',
			     'rr interval',
			     'r wave',
			     'p wave',
			     'q duration',
			     's wave'
			     ]
		if mapList(SOICUI,LabTest):
			if mapList(TopicSem,['diap']) or mapList(PhenDesc.lower(),Diagnosis):
				if not 'Clinical Attributes' in phenCategory and not 'Clinical Attributes Family' in phenCategory:
					if not 'Diagnostic Procedure' in phenCategory:
						phenCategory.append('Diagnostic Procedure')

		if not mapList(SOICUI,LabTest):
			if mapList(TopicSem,['diap']) or mapList(PhenDesc.lower(),Diagnosis):
				if not 'Clinical Attributes' in phenCategory and not 'Clinical Attributes Family' in phenCategory:
					if not 'Diagnostic Procedure Family' in phenCategory:
						phenCategory.append('Diagnostic Procedure Family')

		### Type: Daily or Recreational Activity
		Activity = ["gait",
			"walking",
			"exercise",
			"sport",
			"workout",
			"gambling",
			"sleep",
			"toilet",
			"chore",
			"stand",
			"eat out"]

		if mapList(SOICUI,LabTest):
			if  mapList(PhenDesc.lower(),Activity) or mapList(TopicSem,['dora']):
				if not 'Clinical Attributes' in phenCategory and not 'Clinical Attributes Family' in phenCategory and not 'Lab Test' in phenCategory and not 'Lab Test Family' in phenCategory and not 'Diagnostic Procedure' in phenCategory and not 'Diagnostic Procedure Family' in phenCategory:
					if not 'Daily or Recreational Activity' in phenCategory:	
						phenCategory.append('Daily or Recreational Activity')	

		if not mapList(SOICUI,LabTest):
			if  mapList(PhenDesc.lower(),Activity) or mapList(TopicSem,['dora']):
				if not 'Clinical Attributes' in phenCategory and not 'Clinical Attributes Family' in phenCategory and not 'Lab Test' in phenCategory and not 'Lab Test Family' in phenCategory and not 'Diagnostic Procedure' in phenCategory and not 'Diagnostic Procedure Family' in phenCategory:
					if not 'Daily or Recreational Activity Family' in phenCategory:
						phenCategory.append('Daily or Recreational Activity Family')

		# IF Medical History co-occurs with any of (Daily or Recreational Activity, Eating or Nutritional Finding, Drinking History) then ignore (i.e., drop Medical History from the assigned types).

		### Type: Medical History
		MedHist = ['dsyn','neop','sosy','acab','anab','biof','cgab','fndg','inpo','orgf','patf','phsf','mobd']

		TopicL1 = TopicCUI.split(';')
		TopicS1 = TopicSem.split(';')
		idx1 = 0
	
		#print TopicS1
	
		for iTopic in TopicL1:
			if mapList(SOICUI,LabTest) and mapList(TopicS1[idx1],MedHist):
				if not 'Daily or Recreational Activity' in phenCategory and not 'Daily or Recreational Activity Family' in phenCategory and not 'Eating or Nutritional Finding' in phenCategory and not 'Eating or Nutritional Finding Family' in phenCategory and not 'Drinking History' in phenCategory and not 'Drinking History Family' in phenCategory:
					if not 'Medical History' in phenCategory:
						phenCategory.append('Medical History')

			if not mapList(SOICUI,LabTest) and mapList(TopicS1[idx1],MedHist):
				if not 'Daily or Recreational Activity' in phenCategory and not 'Daily or Recreational Activity Family' in phenCategory and not 'Eating or Nutritional Finding' in phenCategory and not 'Eating or Nutritional Finding Family' in phenCategory and not 'Drinking History' in phenCategory and not 'Drinking History Family' in phenCategory:
					if not 'Medical History Family' in phenCategory:
						phenCategory.append('Medical History Family')
			idx1+=1

		# End the rules
		# =========================================================================

		# PRINT OUT THE MAPPING

		phenCatStr = ';'.join(phenCategory[0:])
		#print item
		#print "======="
		#print phenCatStr
		#print "======="
		
		# Print to Excel file
		ExcelOut = '\t'.join(item[0:]).strip() + '\t' + phenCatStr

		# Print to text file
		#ExcelOut = ':::'.join(item[0:]).strip() + ':::' + TopicPCN + ':::' + TopicCUI + ':::' + TopicSem + ':::' +  phenCatStr

		print ExcelOut

	fin.close()


def usage():
	print """"python [prog] -i <file> -d <number> 
where input can be one of those:
-i : input file
-d : deliminator number of phenotype description, default is 1.
        """

def main():

	try:
		options,remainder = getopt.getopt(sys.argv[1:], 'i:d:hdv', ['input=','deliminator=','help','debug','version'])

	except getopt.GetoptError:
                usage()
                sys.exit(2)
		
	delim = 1 # Default vallue index of Phenotype description

	for opt,arg in options:
		if opt in ('-h', '--help'):
			usage()
			sys.exit()
		elif opt in ('-i', '--input'):
			Qinput = arg
		elif opt in ('-d', '--deliminator'):
			delim = int(arg)

	readinput2(Qinput,delim)

if __name__=="__main__":
	main()

