#!/bin/sh

PhenPATH='/home/sondoan/pfindr/Normalization/web1'

Tagger='/pfindrIndex_SemType_v12_web.py'
Categorizer='/Phen-classify-revised-ALL_v3.py'

# *******************************************
# Step 1. Tagging
# *******************************************

# For raw input -- text only
python $PhenPATH$Tagger -t "$1" > /tmp/tmp_sem 

# *******************************************
# Step 2. Categorizing
# *******************************************

# For raw input -- text only
python $PhenPATH$Categorizer -i /tmp/tmp_sem > /tmp/tmp_cat


