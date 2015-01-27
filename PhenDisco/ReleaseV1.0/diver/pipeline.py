# Pipeline for demographic mapping tools
# Input is free text input
# Output is demographic mapping 
# This is run in server side
# Input : Free text
# Output: Mapping model at ./model.html
# Run:
# python ./pipeline.py 'age first started smoking cigars'

import os,sys

# ==========================================================
# Put the current directory here
CurrentDir = '.'
OutputDir = '.'
MetaMap = '/data/resources/MetaMap/public_mm/bin/metamap11v2' 

# ==========================================================
# Step 1: Normalize the free text
# ==========================================================

InputStr = '"' + sys.argv[1] + '"'
NormCmd = 'python ' + CurrentDir + '/ParseQuery_server.py ' + InputStr
NormText = os.popen(NormCmd).read().strip() 

# ==========================================================
# Step 2: Running MetaMap
# ==========================================================
pid = os.getpid()
MetaMapCmd = 'echo "' + NormText + '"|' + MetaMap + ' -q > ' + OutputDir + '/metamap.out'
os.system(MetaMapCmd)

# ==========================================================
# Step 3: Mapping into a semantic model
# ==========================================================
SemMapCmd = 'python ' + CurrentDir + '/MetaMapEncoding_server_v1.py ' + OutputDir + '/metamap.out > '  + OutputDir + '/model.html' 
os.system(SemMapCmd)

