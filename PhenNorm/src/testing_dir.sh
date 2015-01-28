#!/bin/sh
# Run pipeline in testing data set
# RUN:
# nohup sh testing_dir.sh ../data/testing_new

for i in `ls $1/*.txt2`
do
	#echo $i
	sh ./Phenotype-pipeline.sh $i
done

