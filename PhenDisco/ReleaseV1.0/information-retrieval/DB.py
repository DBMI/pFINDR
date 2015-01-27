# The script pull out data from database
# Written by Son Doan, Oct 2012

import MySQLdb
import sys,re

class Table:
	''' This class is for retrieve data from dbGaP database '''

	def __init__(self, db, name):
		self.db = db
		self.name = name
		self.dbc = self.db.cursor()

	# Get an item by index of record
	def __getitem__(self, item):
		self.dbc.execute("select * from %s limit %s, 1" %(self.name, item))
		return self.dbc.fetchone()

	def __len__(self):
		self.dbc.execute("select count(*) from %s" % (self.name))
		l = int(self.dbc.fetchone()[0])
		return l

	# Count number of phenotypes in a study
	def phencount(self, item):
		#cmd = "select count(PhenID) from Phenotypes WHERE StudyID LIKE \"%" + item + "%\""
		cmd = "select count(PhenID) from " + self.name + " WHERE StudyID LIKE \"%" + item + "%\""
		self.dbc.execute(cmd)
		num = int(self.dbc.fetchone()[0])
		return num

	# Count number of datasets in a study
	def datasetcount(self, item):
		#cmd = "select count(distinct(DatasetID)) from Phenotypes WHERE StudyID LIKE \"%" + item + "%\""
		cmd = "select count(distinct(DatasetID)) from " + self.name + " WHERE StudyID LIKE \"%" + item + "%\""
		self.dbc.execute(cmd)
		num = int(self.dbc.fetchone()[0])
		return num

	# Get an item by StudyID of record
	def getitem(self, item):
		#cmd = "select * from Phenotypes WHERE StudyID LIKE \"%" + item +"%\""
		cmd = "select * from " + self.name + " WHERE StudyID LIKE \"%" + item +"%\""
		self.dbc.execute(cmd)
		return self.dbc.fetchall()

	# Get Platform from Table Study
	def getPlatform(self, item):
		plat = self.getitem(item)[0][7]
		Platform = plat.replace(';','<br>')
		return Platform

	# Get Title from Table Study
	def getTitle(self, item):
		item1 = item.split('.')[0]
		title = self.getitem(item1)[0][1]
		return title

	# =======================================
	# Get info from table StudyAbstraction
	# Get geo
	def getGeo(self, item):
		geo = 'n/a'
		try:
			geo = self.getitem(item)[0][5]
		except:
			geo='n/a'
		return geo.lower()

	# Get topic disease
	def getDisease(self, item):
		disease = 'n/a'
		try:
			disease = self.getitem(item)[0][2]
		except:
			disease='n/a'
		return disease.lower()

	# Get IRB
	def getIRB(self, item):
		IRB1 = 'n/a'
		try:
			IRB = self.getitem(item)[0][11]
			if IRB==1:
				IRB1 = 'Required'
			elif IRB==0:
				IRB1 = 'Not required'
		except:
			IRB1='n/a'
		return IRB1

	# Get Consent Type
	def getConsent(self, item):
		consent1 = 'n/a'
		try:
			consent = self.getitem(item)[0][12]
			if consent==0:
				consent1 = 'Unrestricted'
			elif consent==1:
				consent1 = 'Restricted'
			elif consent==2:
				consent1 = 'Unspecified'
		except:
			consent1='n/a'
		return consent1

	# =======================================
	# Get info from table StudyAbstractionNew
	# Get geo
	def getGeoNew(self, item):
		geo = 'n/a'
		try:
			geo = self.getitem(item)[0][4]
		except:
			geo='n/a'
		return geo.lower()

	# Get topic disease
	def getDiseaseNew(self, item):
		disease = 'n/a'
		try:
			disease = self.getitem(item)[0][1]
		except:
			disease='n/a'
		return disease.lower()

	# Get IRB
	def getIRBNew(self, item):
		IRB1 = 'n/a'
		try:
			IRB = self.getitem(item)[0][2]
			if IRB==1:
				IRB1 = 'Required'
			elif IRB==0:
				IRB1 = 'Not required'
		except:
			IRB1='n/a'
		return IRB1

	# Get Consent Type
	def getConsentNew(self, item):
		consent1 = 'n/a'
		try:
			consent = self.getitem(item)[0][3]
			if consent==0:
				consent1 = 'Unrestricted'
			elif consent==1:
				consent1 = 'Restricted'
			elif consent==2:
				consent1 = 'Unspecified'
		except:
			consent1='n/a'
		return consent1

	# ==============================================
	# Get concept
	def getConcept(self,keywords):
		cmd = "select DISTINCT AUI2_PreferedName from " + self.name + " WHERE AUI1_PreferedName=\"" + keywords +"\" OR CUI1_PreferedName=\"" + keywords + "\""
		print cmd
		self.dbc.execute(cmd)
		return self.dbc.fetchall()

	# Count number of phenotype query
	def countPhen(self, query):
		cmd = "select count(*) from " + self.name + " WHERE PhenDescription REGEXP " + query 
		self.dbc.execute(cmd)
		num = int(self.dbc.fetchone()[0])
		return num

	# Get phenotype descriptions
	def getPhen(self, query):
		#cmd1 = "select DISTINCT PhenDescription from " + self.name + " WHERE PhenDescription LIKE \"%" + query +"%\" LIMIT 0,20"
		cmd1 = "select * from " + self.name + " WHERE PhenDescription REGEXP " + query + " LIMIT 0,25"
		self.dbc.execute(cmd1)
		return self.dbc.fetchall()

	# Count all the number of phenotype 
	def countPhenAll(self):
		cmd = "select count(*) from " + self.name 
		self.dbc.execute(cmd)
		num = int(self.dbc.fetchone()[0])
		return num

	# Get all phenotype descriptions
	def getPhenAll(self, Page):
		cmd1 = "select * from " + self.name + " LIMIT " + str((Page-1)*25) + ',' + str((Page-1)*25 + 25)
		self.dbc.execute(cmd1)
		return self.dbc.fetchall()

	# ========================================================
	# ------ LIMIT FOR PhenDescription only
	# Count number of phenotype query with ID List
	def countPhenLimit(self, query, IDList):
		cmd = "select count(*) from " + self.name + " WHERE PhenDescription REGEXP " + query + " AND StudyID REGEXP '^(" + IDList.strip('"') + ")'"
		#print cmd
		self.dbc.execute(cmd)
		num = int(self.dbc.fetchone()[0])
		return num

	# Get phenotype descriptions with ID List
	def getPhenLimit(self, query, IDList, Page):
		cmd1 = "select * from " + self.name + " WHERE PhenDescription REGEXP " + query + " AND StudyID REGEXP '^(" + IDList.strip('"') + ")' LIMIT " + str((Page-1)*25) + ',' + str((Page-1)*25 + 25)
		#print cmd1
		self.dbc.execute(cmd1)
		return self.dbc.fetchall()

	# ========================================================
	# ------ LIMIT FOR PhenDescription/Theme/Topic/Category
	# Count number of phenotype query with ID List
	def countPhenLimit1(self, query, IDList):
		cmd = "select count(*) from " + self.name + " WHERE (Category REGEXP " + query +  ' OR Theme REGEXP ' + query  + ' OR ThemePCN REGEXP ' + query + ' OR TopicPCN REGEXP '  + query + ' OR SOIPCN REGEXP ' + query + ' OR Category REGEXP ' +query+ ") AND StudyID REGEXP '^(" + IDList.strip('"') + ")'"
		#print cmd
		self.dbc.execute(cmd)
		num = int(self.dbc.fetchone()[0])
		return num

	# Get phenotype descriptions with ID List
	def getPhenLimit1(self, query, IDList, Page):
		cmd1 = "select * from " + self.name + " WHERE (Category REGEXP " + query +  ' OR Theme REGEXP ' + query  + ' OR ThemePCN REGEXP ' + query + ' OR TopicPCN REGEXP '  + query + ' OR SOIPCN REGEXP ' + query + ' OR PhenDescription REGEXP ' +query+ ") AND StudyID REGEXP '^(" + IDList.strip('"') + ")'"  + " LIMIT " + str((Page-1)*25) + ',' + str((Page-1)*25 + 25)
		#print cmd1
		self.dbc.execute(cmd1)
		return self.dbc.fetchall()


