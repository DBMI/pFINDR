#!/bin/sh

# Pipeline for phenotype standadization
# Example:
# sh Phenotype-pipeline.sh ../data/285phen.inp

### SCRIPTS program

Tagger='./pfindrIndex_SemType_v12.py'
Categorizer='./Phen-classify-revised-ALL_v3.py'
Cluster='./Similar_finding_v2.py'

# Example. 
# $1=../data/285phen.inp

#Input=$1

# *******************************************
# Step 1. Tagging
# *******************************************
# For raw input -- text only
python $Tagger -i $1 >$1_sem 

# For the whole pipeline -- Orig phenDesc in field #5, index start from 0 splitted by ':::'
#python $Tagger -d 5 -i $1 >$1_sem 

# For gold standard data -- Orig phenDesc in field #1, index start from 0 splitted by ':::'
#python $Tagger -d 1 -i $1 >$1_sem 

# *******************************************
# Step 2. Categorizing
# *******************************************
# For raw input -- text only
python $Categorizer -i $1_sem > $1_cat

# For the whole pipeline  -- Orig phenDesc in field #5, index start from 0 splitted by ':::'
#python $Categorizer -d 10 -i $1_sem > $1_cat

# For gold standard data  -- Orig phenDesc in field #1, normed phenDesc #2, index start from 0 splitted by ':::'
#python $Categorizer -d 2 -i $1_sem > $1_cat

# *******************************************
# Step 3. Clustering
# *******************************************
# For raw input -- text only
#python $Cluster -i "All" -d 1 -i $1_cat > $1_similar

# For gold standard data  -- Orig phenDesc in field #1, normed phenDesc #2, index start from 0 splitted by ':::'
#python $Cluster -o "All" -d 1 -i $1_cat > $1_similar

