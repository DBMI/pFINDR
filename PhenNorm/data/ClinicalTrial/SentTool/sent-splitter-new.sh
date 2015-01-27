#!/bin/sh

# Script to do sentence splitter
# Input:
# $1: Folder containing original text
# $2: Target folder containing sentence splitted text
# RUN:
# sh sent-splitter.sh 2014orig 2014sent

for i in `ls $1`
do
	# Sentence splitter for an input file

	# remove multiple new lines
	sed /^$/d $1/$i > $1/$i.tmp

	echo $1/$i	

	# Run sentence splitter
	perl ./Sent1.pl $1/$i > $2/$i.sent
	
	# Remove temp file
	rm $1/$i.tmp
done
