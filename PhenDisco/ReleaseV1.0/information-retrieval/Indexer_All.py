# Index for all dbGaP data, including studies and phenotypes
# ****** CAREFUL WHENEVER RUN AGAIN, IT WILL **** WRITE **** INTO CURRENT INDEX FOLDER 
# Written by Son Doan, Aug 2012

import os,sys
import html2text
from whoosh.index import create_in
from whoosh.fields import *
from decimal import *

# ================================================================
#  MAIN SCHEMA 
# ================================================================

schema = Schema(IDName=TEXT(stored=True),path=ID(stored=True), title=TEXT(stored=True), desc=TEXT(stored=True), Type=TEXT(stored=True), cohort=NUMERIC(stored=True), inexclude=TEXT(stored=True),  platform=TEXT(stored=True), MESHterm=TEXT(stored=True), history=TEXT(stored=True), attributes=TEXT(stored=True), topic=TEXT(stored=True),disease=TEXT(stored=True),measurement=TEXT(stored=True),demographics=TEXT(stored=True),geography=TEXT(stored=True),age=TEXT(stored=True),gender=TEXT(stored=True),category=TEXT(stored=True),IRB=TEXT(stored=True),ConsentType=TEXT(stored=True),phen=TEXT(stored=True),phenID=TEXT(stored=True),phenDesc=TEXT(stored=True),phenName=TEXT(stored=True),phenCUI=TEXT(stored=True),phenMap=TEXT(stored=True), AgeMin=NUMERIC(stored=True), AgeMax=NUMERIC(stored=True), MaleNum=NUMERIC(stored=True), FemaleNum=NUMERIC(stored=True), OtherGenderNum=NUMERIC(stored=True), UnknownGenderNum=NUMERIC(stored=True), Demographics=TEXT(stored=True), phenType=TEXT(stored=True))

# ****** CAREFUL WHENEVER RUN AGAIN, IT WILL **** WRITE **** INTO CURRENT INDEX FOLDER 
# Comment it when do experimental

ix = create_in("PhD",schema)
writer = ix.writer()

Dict = {}

##### GLOBAL VARIABLES #######

# Replace the folder containing meta-data (study abstraction and phenotype) here
DataPATH = '../database/'

# =================================================================
# Combine abtraction from studies
# =================================================================

StudyData = DataPATH + '/studyAbstraction/dbGaP-all-html.datJan10'
fin = open(StudyData,'r')

for lines in fin.readlines():
	line = lines.split(':::')
	ID1 = line[0]
	ID2 = ID1.split('.')[0].strip()
	title1 = line[1]
	desc1 = line[2]
	type1 = line[3]
	cohort1 = line[4].strip()

	if len(cohort1)==0:
		cohort1 = 0

	inexclude1 = line[6]
	platform1 = line[7]
	MESHterm1 = line[8]
	history1 = line[9]
	attributes1 = line[10]

	Dict[ID2]=[ID1,title1,desc1,type1,cohort1,inexclude1,platform1,MESHterm1,history1,attributes1]

fin.close()

# =================================================================
# Combine abtraction from curation studies
# =================================================================
StudyData3 = DataPATH + '/studyAbstraction/StudyAbstraction.txt_ascii'

fin = open(StudyData3,'r')

tempDict={}

for lines in fin.readlines():
	line = lines.split('\t')
	ID1 = line[0]
	ID2 = ID1.split('.')[0].strip()
	disease = line[1]
	geography = line[4]
	IRB = line[2]

	if IRB.strip()=='1':
		IRB = 'Required'
	elif IRB.strip()=='0':
		IRB = 'No'
	else:
		IRB = 'Unspecified'

	ConsentType=line[3]
	if ConsentType.strip()=='1':
		ConsentType = 'Restricted'
	elif ConsentType.strip()=='0':
		ConsentType = 'No'
	else:
		ConsentType = 'Unspecified'
	
	# Temporary variables
	tempDict[(ID2,'disease')] = disease
	tempDict[(ID2,'geography')] = geography
	tempDict[(ID2, 'IRB')] = IRB
	tempDict[(ID2,'ConsentType')] = ConsentType	

fin.close()

# Change to newly update file from abstraction - Mindy dir
StudyData2 = DataPATH + '/studyAbstraction/mindy_abstracting-22.txt'

fin = open(StudyData2,'r')

for lines in fin.readlines():
	line = lines.split(':::')
	ID1 = line[0]
	ID2 = ID1.split('.')[0]
	topic = line[1]
	#disease = line[2]
	disease = tempDict[(ID2,'disease')]
	measurement = line[3]
	demographics = line[4]
	#geography = line[5]
	geography = tempDict[(ID2,'geography')]
	age = line[6]
	gender = line[7]
	cat = line[8]

	IRB=tempDict[(ID2,'IRB')]
	ConsentType=tempDict[(ID2,'ConsentType')]

	if Dict.has_key(ID2):
		Dict[ID2].append((topic,disease,measurement,demographics,geography,age,gender,cat,IRB,ConsentType))

fin.close()

# ===============================================
# Fill out empty fields if not has an abstraction
for keys in Dict.keys():
	if len(Dict[keys])<=10:
		#print keys 	
		Dict[keys].append(('','','','','','','','','',''))

# =================================================================
# Combine abtraction from phenotypes
# =================================================================
PhenData = DataPATH + '/phenotype/dbGaP.datJuly1_2013'

fin = open(PhenData,'r')

for lines in fin.readlines():
	line = lines.split(':::')
	phenID1 = line[0].split('.')[0]
	studyID1 = line[1].split('.')[0]
	dataset1 = line[2].split('.')[0]
	dataname1 = line[3]
	phenName1 = line[4]
	phenDesc1 = line[5]

	phenStr = ' '.join(line[0:6])
	if Dict.has_key(studyID1):
		Dict[studyID1].append(phenStr)

fin.close()

# =================================================================
# Add mapped phenotypes into search
# =================================================================
PhenMapData = DataPATH + '/phenotype/dbGaP.datJuly1_2013.map'

fin = open(PhenMapData,'r')

for lines in fin.readlines():
	line = lines.split(' ::: ')
	# If mapped
	if len(line)==22:
		studyID1 = line[1].split('.')[0]
		phenID1 = line[0].split('.')[0]
		phenName1 = line[4]
		phenDesc1 = line[5]
		theme = line[11]
		themePCN = line[12]
		themeCUI = line[13].strip().split(';')
		topicPCN = line[15]
		topicCUI = line[16].strip().split(';')
		SOI_PCN = line[18]
		SOI_CUI = line[19].strip().split(';')

		#print SOI_CUI
		# Added on Apr 24, 2012
		phenType = line[-1].strip()
		#print phenType

		phenMap1 = theme + ' ' + themePCN + ' ' + topicPCN + ' ' + SOI_PCN
		phenCUI1 = list(set(topicCUI + SOI_CUI))

		# Add phenID
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'phenID1')):
				Dict[(studyID1,'phenID1')] = [phenID1]
			else:
				if not phenID1 in Dict[(studyID1,'phenID1')]:
					Dict[(studyID1,'phenID1')].append(phenID1)
		# Add phenName
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'phenName1')):
				Dict[(studyID1,'phenName1')] = [phenName1]
			else:
				if not phenName1 in Dict[(studyID1,'phenName1')]:
					Dict[(studyID1,'phenName1')].append(phenName1)
		# Add phenDesc
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'phenDesc1')):
				Dict[(studyID1,'phenDesc1')] = [phenDesc1]
			else:
				if not phenDesc1 in Dict[(studyID1,'phenDesc1')]:
					Dict[(studyID1,'phenDesc1')].append(phenDesc1)
		# Add phenMap
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'phenMap1')):
				Dict[(studyID1,'phenMap1')] = [phenMap1]
			else:
				if not phenMap1 in Dict[(studyID1,'phenMap1')]:
					Dict[(studyID1,'phenMap1')].append(phenMap1)
		# Add phenCUI
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'phenCUI1')):
				Dict[(studyID1,'phenCUI1')] = phenCUI1
			else:
				Dict[(studyID1,'phenCUI1')] = list(set(Dict[(studyID1,'phenCUI1')] + phenCUI1))
		# Add phenType
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'phenType1')):
				Dict[(studyID1,'phenType1')] = [phenType]
			else:
				if not phenType in Dict[(studyID1,'phenType1')]:
					Dict[(studyID1,'phenType1')].append(phenType)

fin.close()

### Added new data summary statistics

DemographicsData = DataPATH + '/studyAbstraction/SummaryStat_Apr2013.txt'
fin1 = open(DemographicsData,'r')

Demographics = ["StudyID","Age-Min","Age-Max","Male Gender","Female Gender","Unknown Gender","Other Gender","White Caucasian","European","Asian Korean","Asian","Black African","Black or African American","African","African Barbedian","Indian Native American","Native Hawaiian or Pacific Islander","American Indian or Alaska Native","Multiple Races","Hispanic","NonLatino","Other Unknown Race","Missing Race","Ashkenazi Jewish","French Canadian","Polish","Italian","England,Ireland ","Ireland","Lebanese","Irish Italian","Germany [non Ashkenazi jewish],England ,Ireland","Han Chinese","Puerto Rican","Hawaiian","Mexican","British","Swiss","Spaniard","Portugese","French","Finnish","German","Russian","Ukrainian","Romanian","Hungarian","Czehs","Jewish","Israeli","Canadian","Dutch Canadian","American USA United States ","European American","Mexican American","Peruvian","Venezuelan","Cuban","Indian","Japanese","Chinese","Filipino","Middle Eastern","Arabic","Omani Arabic","Pakistani","Turkish","Amhara","Hamer"]

count = 0
for lines in fin1.readlines():
	count+=1
	if count >1:
		line = lines.split('\t')
		studyID1 = line[0].split('.')[0].strip()
		
		# Debuging

		AgeMin = line[1].strip()
		if len(AgeMin)==0:
			AgeMin = 0
		else:
			AgeMin = int(float(AgeMin))
		
		AgeMax = line[2].strip()
		if len(AgeMax)==0:
			AgeMax = 100
		else:
			AgeMax = int(float(AgeMax))

		
		MaleNum = line[3].strip('"').split(',')[0].strip()
		if len(MaleNum) ==0:
			MaleNum = 0
		else:
			MaleNum=int(MaleNum)
			
		FemaleNum = line[4].strip('"').split(',')[0].strip()
		if len(FemaleNum) ==0:
			FemaleNum = 0
		else:
			FemaleNum = int(FemaleNum)
		
		OtherGenderNum = line[5].strip('"').split(',')[0].strip()
		if len(OtherGenderNum) ==0:
			OtherGenderNum = 0
		else:
			OtherGenderNum = int(OtherGenderNum)
		
		UnknownGenderNum = line[6].strip('"').split(',')[0].strip()
		if len(UnknownGenderNum) ==0:
			UnknownGenderNum = 0
		else:
			UnknownGenderNum = int(UnknownGenderNum)
		
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'AgeMin')):
				Dict[(studyID1,'AgeMin')] = AgeMin
		else:
			Dict[(studyID1,'AgeMin')] = AgeMin
			
		
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'AgeMax')):
				Dict[(studyID1,'AgeMax')] = AgeMax
		else:
			Dict[(studyID1,'AgeMax')] = AgeMax
		
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'MaleNum')):
				Dict[(studyID1,'MaleNum')] = MaleNum
		else:
			Dict[(studyID1,'MaleNum')] = MaleNum
		
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'FemaleNum')):
				Dict[(studyID1,'FemaleNum')] = FemaleNum
		else:
			Dict[(studyID1,'FemaleNum')] = FemaleNum
		
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'OtherGenderNum')):
				Dict[(studyID1,'OtherGenderNum')] = OtherGenderNum
		else:
			Dict[(studyID1,'OtherGenderNum')] = OtherGenderNum
		
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'UnknownGenderNum')):
				Dict[(studyID1,'UnknownGenderNum')] = UnknownGenderNum
		else:
			Dict[(studyID1,'UnknownGenderNum')] = UnknownGenderNum
		
		DemStr= ''	
		if MaleNum>0:
			DemStr=' Male Man Gender Sex '
		if FemaleNum>0:			
			DemStr+=' Female Woman Gender Sex '
		if OtherGenderNum>0:			
			DemStr+=' Other Gender Sex '
		if UnknownGenderNum>0:			
			DemStr+=' Unknown Gender Sex '

		for i in range(7,len(line)):
			if len(line[i].strip()):
				if int(line[i].strip())>0:
					DemStr+= Demographics[i].strip() + ' ; '
		if Dict.has_key(studyID1):
			if not Dict.has_key((studyID1,'Demographics')):
				Dict[(studyID1,'Demographics')] = DemStr

		else:
			Dict[(studyID1,'Demographics')] = DemStr
fin1.close()

# Fill out empty fields
for keys in Dict.keys():

	if isinstance(keys,str):
		if len(Dict[keys])<=11:
			Dict[keys].append('')
	if not Dict.has_key((keys,'phenID1')):
		Dict[(keys,'phenID1')]=['']
	if not Dict.has_key((keys,'phenName1')):
		Dict[(keys,'phenName1')]=['']
	if not Dict.has_key((keys,'phenDesc1')):
		Dict[(keys,'phenDesc1')]=['']
	if not Dict.has_key((keys,'phenMap1')):
		Dict[(keys,'phenMap1')]=['']
	if not Dict.has_key((keys,'phenCUI1')):
		Dict[(keys,'phenCUI1')]=['']
	if not Dict.has_key((keys,'AgeMin')):
		Dict[(keys,'AgeMin')]=0
	if not Dict.has_key((keys,'AgeMax')):
		Dict[(keys,'AgeMax')]=100
	if not Dict.has_key((keys,'MaleNum')):
		Dict[(keys,'MaleNum')]=0
	if not Dict.has_key((keys,'FemaleNum')):
		Dict[(keys,'FemaleNum')]=0
	if not Dict.has_key((keys,'OtherGenderNum')):
		Dict[(keys,'OtherGenderNum')]=0
	if not Dict.has_key((keys,'UnknownGenderNum')):
		Dict[(keys,'UnknownGenderNum')]=0
	if not Dict.has_key((keys,'Demographics')):
		Dict[(keys,'Demographics')]=''
	if not Dict.has_key((keys,'phenType1')):
		Dict[(keys,'phenType1')]=''

### INDEXING

print "Start indexing ....."

for keys in Dict.keys():

	if isinstance(keys,str):
		if keys.find('phs')>=0 or keys.lower().find('egas')>=0:
			IDName1 = keys
			path1 = Dict[keys][0]
			title1 = Dict[keys][1]
			desc1 = Dict[keys][2]
			type1 = Dict[keys][3]
			cohort1 = Dict[keys][4]
			inexclude1 = Dict[keys][5]
			platform1 = Dict[keys][6]
			MESHterm1 = Dict[keys][7]
			history1 = Dict[keys][8]
			attributes1 = Dict[keys][9]
			topic1 = Dict[keys][10][0]
			measurement1 = Dict[keys][10][2]
			demographics1 = Dict[keys][10][3]
			age1 = Dict[keys][10][5]
			gender1 = Dict[keys][10][6]
			cat1 = Dict[keys][10][7]

			disease1 = tempDict[keys,'disease']
			geography1 = tempDict[keys,'geography']
			IRB1 = tempDict[keys,'IRB']
			ConsentType1 = tempDict[keys,'ConsentType']

			phen1 = ' '.join(Dict[keys][11:])
			phenID1S = ' '.join(Dict[keys,'phenID1'][0:])
			phenName1S = ' '.join(Dict[keys,'phenName1'][0:])
			phenDesc1S = ' '.join(Dict[keys,'phenDesc1'][0:])
			phenMap1S = ' '.join(Dict[keys,'phenMap1'][0:])
			phenCUI1S = ' '.join(Dict[keys,'phenCUI1'][0:])
			# Added phenType
			phenType1S = ' '.join(Dict[keys,'phenType1'][0:])
			
			ageMin1 = Dict[keys,'AgeMin']
			ageMax1 = Dict[keys,'AgeMax']
			MaleNum1 = Dict[keys,'MaleNum']
			FemaleNum1 = Dict[keys,'FemaleNum']
			OtherGenderNum1 = Dict[keys,'OtherGenderNum']
			UnknownGenderNum1 = Dict[keys,'UnknownGenderNum']
			Demographics1 = Dict[keys,'Demographics']
			
			# Comment it when do experimental
			writer.add_document(IDName=unicode(IDName1),path=unicode(path1),title=unicode(title1), desc=unicode(desc1),Type=unicode(type1),cohort=cohort1, inexclude=unicode(inexclude1), platform=unicode(platform1),MESHterm=unicode(MESHterm1),history=unicode(history1),attributes=unicode(attributes1),topic=unicode(topic1),disease=unicode(disease1),measurement=unicode(measurement1),demographics=unicode(demographics1),geography=unicode(geography1),age=unicode(age1),gender=unicode(gender1),category=unicode(cat1),IRB=unicode(IRB1),ConsentType=unicode(ConsentType1),phen=unicode(phen1),phenID=unicode(phenID1S),phenDesc=unicode(phenDesc1S),phenName=unicode(phenName1S),phenCUI=unicode(phenCUI1S),phenMap=unicode(phenMap1S),AgeMin=ageMin1,AgeMax=ageMax1,MaleNum=MaleNum1,FemaleNum=FemaleNum1,OtherGenderNum=OtherGenderNum1,UnknownGenderNum=UnknownGenderNum1,Demographics=unicode(Demographics1),phenType=unicode(phenType1S))

writer.commit()

print "Indexing done!!!"
