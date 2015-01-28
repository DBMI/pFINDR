# 	$Id$	
# This class is for processing query to map into concept
# Task:
# 1) Normalize text
# 2) Map into UMLS concept

import re
from pyparsing import *

class QueryNorm:
    ''' This class is for normalizing text 
    '''

    def __init__(self, text):
        self.data = text

    def __repr__(self):
        return "%s" % (self.data)

    def norm(self):

    	#Rule 0:  If a word has an uppercase letter occurring in it after a lowercase letter, split on that letter (e.g. "firstSecond" -> "first Second")
    	wordL = self.data.split()
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
    	
    	# Rule 3: If there are more than two letters before the hyphen, then split on the hyphen.  Otherwise, remove the hyphen (e.g. "X-Ray" -> XRay, "By-pass" -> bypass, "heart-attack" -> heart attack.)
    	
    	Str = ''
    	wordL = line1.split()
    	for word in wordL:
    	    #Str = Str + ' ' + word
    	    Hyphen = word.split('-')
    	    #print Hyphen
    	    if len(Hyphen)==0:
    	        Str = Str + ' ' + word
    	    else:
    	        if len(Hyphen[0])<=2:
    	            Str = Str + ' ' + ''.join(Hyphen[0:])
    	        else:
    	            Str = Str + ' ' + ' '.join(Hyphen[0:])
        # Rule 4: If a Word has a numeral in it, split  at the last digit (e.g. Q13AGE -> Q13 AGE)
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
    	
#   	 # Rule 7: If string match 'male' and 'gender' then convert into 'male gender' 
#   	 if Str1.find(' male ')>=0 and Str1.find('gender')>=0 and Str1.find(' female ')==-1:
#   	     Str1 = Str1.replace('male','')
#   	     Str1 = Str1.replace('female','')
    	
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
    	
    	# Remove some words for MetaMap confusion
    	Str1 = Str1.replace('utterance',' ')
    	Str1 = Str1.replace('phrase',' ')
    	Str1 = Str1.replace('candidates',' ')
    	Str1 = Str1.replace('mappings',' ')

        Str1 = Str1.replace('\"','')
    	
    	return Str1.strip()

class QueryMap:
    ''' This class is to map free text into MetaMap
    '''

    def __init__(self,text):
        self.data = text
	
    def wrapper(self):
        ''' Wrapper for MetaMap, called MetaMap from shell
            Input is self.data
	'''
	
        from subprocess import Popen, PIPE
        #p1 = Popen(["echo", text], stdout=PIPE)
        
        # self.data should be converted into string 
        p1 = Popen(["echo", str(self.data)], stdout=PIPE)
        p2 = Popen(["/data/resources/MetaMap/public_mm/bin/metamap11v2", "-q", "--silent"], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()
        result = p2.communicate()[0]
        p1.wait()
        return result
	
    def getMapping(self, Text):
        ''' Get mapped terms from MetaMap.
        '''
        #Text = str(self.data)
        QueryStr = []

    	## For debugging
    	#print Text
    	TermList = {}
    	Sents = Text.split('phrase')
    	UttText = Sents[0].split('",')[0].split('\',')[1].strip('"').lower()
    	
        # Only get mapping string !
        for Sent1 in Sents[1:]:
            Phrase = Sent1.split('candidates')
            PhraseText = Phrase[0].split(',')[0].split('(')[1].lower().strip('\'')

            ## For debugging
            #print "Start to print ========"
            #print Phrase
            #print "PHRASE: " + PhraseText
                    
            for Sent2 in Phrase[1:]:
                Candidate = Sent2.split('mappings')
                CandidateString = Candidate[1].split('\n')[0]

                # Access Mapping
                MappedString = Candidate[1].split('\n')[1]
                CandidateList = CandidateString.split('ev(')
                    
                if len(CandidateList)>=2:

                    Candidate_temp = []
                    for item in CandidateList[1:]:
                        CandidateCUI = item.split(',')[1]
                        CandidateMatched = item.split(',')[2].lower().strip('\'')
                        if item.find('\',[') >=0:
                            CandidatePreferred = item.split('\',[')[0].split('\'')[-1].lower().strip('\'')
                        else:
                            CandidatePreferred = item.split(',')[3].lower()
                        SemType = item.split('[')[2].strip(',').strip(']')
                    	                    	        
                        ## For debugging
                        #print item
                        #print "MATCHED : " + CandidateMatched
                        #print "PREFERRED : " + CandidatePreferred

		    	# =======================================
		    	# REMOVE LOINC code and SNOMED CT, added on Apr 26, 2013
		    	# =======================================
                        if CandidatePreferred.find('^')==-1 and CandidatePreferred.find('-')==-1:
                            Candidate_temp.append((CandidateMatched,CandidatePreferred))

                    QueryStr.append((PhraseText,Candidate_temp))
                else:
                    ## For debugging
                    #print "PREFERRED : "
                    QueryStr.append((PhraseText,'',''))

        OrigQuery = ''
        for item in QueryStr:
            	OrigQuery += ' ' + item[0]	

        ## For debugging        
        #print "==================================="
        #print "Orig Query: "
        #print OrigQuery.strip()

        #print "Extended Query: "
        # --------------------------------
        # Adding original query into query 
        ExtendedQuery = ' '
        #ExtendedQuery = self.data + ' OR '
        for item in QueryStr:
            # MOST IMPORTANT FOR DEBUGGING
            #print "======"
            #print item

            if len(item[0].strip())>0:
                temp1 = '("' + item[0].strip('"') + '"'
            else:
                #print item[1][0][1]
                #temp1 = ''
                # Note: Error of MetaMap when parsing phrase such as "(copd and child)"
		if len(item[1])>=0 and len(item[1][0])>0:
               		temp1 ='("' + item[1][0][1] + '"' 
		else:
			temp1=''

            #print temp1

            # If there is mapping terms
            if len(item[1])>0:
                for item1 in item[1]:
                    # if preferred terms is not matched phrase
                    #if len(temp1)>0 and item1[1].strip('"') !=item[0].strip('"'):
                    if len(temp1)>0 and item1[1].strip('"') !=item[0].strip('"') and item1[1]!=item1[0]:
                        temp1=temp1 + ' OR "' + item1[1].strip('"') + '"'

                    #if len(temp1)>0 and item1[1].strip('"') !=item[0].strip('"') and item1[1].strip('"') !=item[1][0][1].strip('"'):
                    #    temp1=temp1 + ' OR "' + item1[1].strip('"') + '"'

                    #if len(temp1)>0 and item1[1].strip('"') !=item[0].strip('"') and item1[1].strip('"') ==item[1][0][1].strip('"'):
                    #    temp1=temp1 + ' OR ("' + item1[1].strip('"') + '"'

                ExtendedQuery+= ' ' + temp1 
                ExtendedQuery +=')'

            # Add AND or OR or NOT operators
            else:
                # If parse into individual AND,OR,NOT
                if item[0].find('and')==0 or item[0].find('or')==0 or item[0].find('not')==0:
                	ExtendedQuery+=' ' + item[0].upper() 
                # If not 
                #else:
                    #ExtendedQuery+=' "' + item[0].upper() + '"'
                    #ExtendedQuery+= item[0].upper()
        
        #print ExtendedQuery.strip()
        return ExtendedQuery.strip()

    def getMappingNew(self,Text):
        ''' Get mapped terms from MetaMap.
        '''
        #Text = str(self.data)
        QueryStr = []

    	## For debugging
    	#print Text
    	TermList = {}
    	Sents = Text.split('phrase')
    	UttText = Sents[0].split('",')[0].split('\',')[1].strip('"').lower()
    	
        # Only get mapping string !
        for Sent1 in Sents[1:]:
            Phrase = Sent1.split('candidates')
            PhraseText = Phrase[0].split(',')[0].split('(')[1].lower().strip('\'')

            ## For debugging
            #print "Start to print ========"
            #print Phrase
            #print "PHRASE: " + PhraseText
                    
            for Sent2 in Phrase[1:]:
                Candidate = Sent2.split('mappings')
                CandidateString = Candidate[1].split('\n')[0]

                # Access Mapping
                MappedString = Candidate[1].split('\n')[1]
                CandidateList = CandidateString.split('ev(')
                    
                if len(CandidateList)>=2:

                    Candidate_temp = []
                    for item in CandidateList[1:]:
                        CandidateCUI = item.split(',')[1]
                        CandidateMatched = item.split(',')[2].lower().strip('\'')
                        if item.find('\',[') >=0:
                            CandidatePreferred = item.split('\',[')[0].split('\'')[-1].lower().strip('\'')
                        else:
                            CandidatePreferred = item.split(',')[3].lower()
                        SemType = item.split('[')[2].strip(',').strip(']')
                    	                    	        
                        ## For debugging
                        #print item
                        #print "MATCHED : " + CandidateMatched
                        #print "PREFERRED : " + CandidatePreferred
                        Candidate_temp.append((CandidateMatched,CandidatePreferred))

                    QueryStr.append((PhraseText,Candidate_temp))
                else:
                    ## For debugging
                    #print "PREFERRED : "
                    QueryStr.append((PhraseText,'',''))
        OrigQuery = ''
        for item in QueryStr:
            OrigQuery += ' ' + item[0]

        ## For debugging        
        #print "==================================="
        #print "Orig Query: "
        #print OrigQuery.strip()

        #print "Extended Query: "
        # --------------------------------
        # Adding original query into query 
        ExtendedQuery = ' '
        #ExtendedQuery = self.data + ' OR '
        for item in QueryStr:
            # MOST IMPORTANT FOR DEBUGGING
            #print "==== ITEM =="
            #print item

            if len(item[0].strip())>0:
                temp1 = '("' + item[0].strip('"') + '"'
            else:
                #print item[1]
                #print len(item[1])
                #print item[1][0]
                #print item[1][0][1]
                #temp1 = ''
                # Note: Error of MetaMap when parsing phrase such as "(copd and child)"
		if len(item[1])>=0 and len(item[1][0])>0:
               		temp1 ='("' + item[1][0][1] + '"' 
		else:
			temp1=''

            #print temp1

            # If there is mapping terms
            if len(item[1])>0:
                for item1 in item[1]:
                    #print "DEBUGGING ...."
                    # if preferred terms is not matched phrase
                    #if len(temp1)>0 and item1[1].strip('"') !=item[0].strip('"'):
                    #    temp1=temp1 + ' OR "' + item1[1].strip('"') + '"'

                    if len(temp1)>0 and item1[1].strip('"') !=item[0].strip('"') and item1[1]!=item1[0]:
                        temp1=temp1 + ' OR "' + item1[1].strip('"') + '"'

                    #if len(temp1)>0 and item1[1].strip('"') !=item[0].strip('"') and item1[1].strip('"') !=item[1][0][1].strip('"'):
                    #    temp1=temp1 + ' OR "' + item1[1].strip('"') + '"'

                    #if len(temp1)>0 and item1[1].strip('"') !=item[0].strip('"') and item1[1].strip('"') ==item[1][0][1].strip('"'):
                    #    temp1=temp1 + ' OR ("' + item1[1].strip('"') + '"'

                ExtendedQuery+= ' ' + temp1 
                ExtendedQuery +=')'

            # Add AND or OR or NOT operators
            else:
                # If parse into individual AND,OR,NOT
                if item[0].find('and')==0 or item[0].find('or')==0 or item[0].find('not')==0:
                	ExtendedQuery+=' ' + item[0].upper() 
                # If not 
                #else:
                    #ExtendedQuery+=' "' + item[0].upper() + '"'
                    #ExtendedQuery+= item[0].upper()
        
        #print ExtendedQuery.strip()
        #return ExtendedQuery.strip()
        try:
            return  ExtendedQuery.strip()
        #    if len(result)>0:
        #        finalS = resultS
        except:
            return ''

## Try to map using MetaMap
#def getMappingStr(Text):
#    Str1 = Text.split(' ')
#    print Str1
#    
#    Str2 = ''
#    for item in Str1:
#        Str2 += item + ' '
#        if Str2.lower()=='and' or Str2.lower()=='or' or Str2.lower()=='not':
#            print Str2
#            a=QueryMap(Str2)
#            metamap1=a.wrapper()
#            map1 = a.getMappingNew(metamap1)
#            print map1
#            Str2 = ''

# This class is in experimental - not finished yet!
class QueryParse:
    '''
    Parsing class for query
    Using pyparsing package to parse free text
    '''

    def __init__(self,text):
        self.text = text

    def Parse(self):        
	and_ = CaselessLiteral("and")
	or_  = CaselessLiteral("or")
	not_ = CaselessLiteral("not")
	searchTerm = Word(alphanums) | quotedString.setParseAction( removeQuotes )
	searchExpr = operatorPrecedence( searchTerm,
	       [
	       (not_, 1, opAssoc.RIGHT),
	       (and_, 2, opAssoc.LEFT),
	       (or_, 2, opAssoc.LEFT),
	       ])

	#tests = """\
	#    wood and blue or red
	#    wood and (blue or red)
	#    (steel or iron) and "lime green"
	#    not steel or iron and "lime green"
	#    not(steel or iron) and "lime green""" .splitlines()
        #
	#for t in tests:
	#    print t.strip()
	#    print searchExpr.parseString(t)[0]
        #
        #print searchExpr.parseString(self.text)[0]

        a = searchExpr.parseString(self.text)[0]
        #print a
        query = ''
        for item in a:
            # If item is string then run MetaMap and include into Query
            if isinstance(item,str):
            	b = QueryMap(item)
                #print item
            	MetaMap =  b.wrapper()
                try:
                    b_out= b.getMapping(MetaMap)
                except:
                    b_out = item                    
                # Check if MetaMap return nothing
                if b_out == '':
                    b_out = '"' + item + '"'
            	query+= b_out + ' ' 
            else:
                query+='('
        	for item1 in item:
        	    if isinstance(item1,str):
        	    	b = QueryMap(item1)
                        #print item1
        	    	MetaMap =  b.wrapper()
        	    	try:
                            b_out1 = b.getMapping(MetaMap)                            
                        except:
                            b_out1 = item1
                        # Check if MetaMap return nothing
                        if b_out1.strip()=='':
                            b_out1 = '"' + item1 + '"'
        	    	query+= b_out1 + ' ' 
                    else:
                        #print item1
                        query+='('
                        # Add here
        		for item2 in item1:
        		    if isinstance(item2,str):
        		    	b2 = QueryMap(item2)
                	        #print item2
        		    	MetaMap2 =  b2.wrapper()
        		    	try:
                	            b_out2 = b2.getMapping(MetaMap2)                            
                	        except:
                	            b_out2 = item2                	
                	        # Check if MetaMap return nothing
                	        if b_out2.strip()=='':
                	            b_out2 = '"' + item2 + '"'
        		    	query+= b_out2 + ' ' 
                        # End add
                        query+=') '
                query+=') '
        #print query
        return query
			
def _demo():

    import sys, subprocess

    # =======================
    # TESTING QueryNorm class
    # =======================
    #a = QueryNorm(sys.argv[1])
    #print a
    #print a.norm()

    # =======================
    # TESTING QueryMap class
    # =======================
    #b = QueryMap(a.norm())
    b = QueryMap(sys.argv[1])
    MetaMap =  b.wrapper()
    print MetaMap
    b_out= b.getMappingNew(MetaMap)
    print b_out
    
if __name__ == "__main__":

    _demo()
