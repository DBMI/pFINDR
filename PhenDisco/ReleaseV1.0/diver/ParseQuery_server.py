'''
The program is to parse an input query from free text
and pass to mapping program to encode it to a semantic model

Input: A text file, program will process one sentence per line
Ouput: Normalized text before MetaMap processing

Written by Son Doan, June 2012
'''

import os,sys
import re

'''
Parse an input text and return to normalized string
Input: Text 
Output: Normalized text
Run: Customize comment to parse text from a text file or from stdin
python ParseQuery.py ./test/Dev_Dataset-2.inp |less
'''
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

    return Str1.strip() + '\n'

def parse_input(file):

    fin = open(file,'r')
    for lines in fin.readlines():
        line = lines.strip().strip('"')        
        Norm = parse_text(line)
        #print line + '::' + Norm
        print Norm

    fin.close()

def main():

    # If input is a text file
    #parse_input(sys.argv[1])

    # If input is a free text
    Norm = parse_text(sys.argv[1])
    print Norm

if __name__=="__main__":
    main()
