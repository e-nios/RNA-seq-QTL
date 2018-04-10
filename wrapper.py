#!usr/bin/env python

import sys
import json
import subprocess
import core

# Input parameters
parameters = None
path = sys.argv[1]
fileFormat = sys.argv[2]

# JSON input
try:
	parameters = json.load(open(path + sys.argv[3]))
except(IndexError):
	pass

# HISAT2 parameters
print("--------------HISAT2--------------")
index = raw_input("HISAT2 index: ")
print("----------------------------------\n")

# FeatureCounts parameters
print("----------FeatureCounts-----------")
gtf = raw_input("GTF file: ")
print("----------------------------------\n")

# EdgeR parameters
print("---------------EdgeR--------------")
condition = "Condition::" + raw_input("Factors: ")
test = raw_input("Contrast of interest: ")
print("----------------------------------\n")

# HAPPY parameters
print("---------------HAPPY--------------")
phenName = raw_input("Phenotype Name: ")
inputFile = raw_input("Input File: ")
print("----------------------------------\n")

# Build arrays with read filenames from glob, to be used with HISAT2
files1 = []
files2 = []
files1 = core.getFiles('*.%s' % fileFormat, path +'reads1/', '/data/reads1/')
files2 = core.getFiles('*.%s' % fileFormat, path +'reads2/', '/data/reads2/')

files1.sort()
files2.sort()

#HISAT2 operator
hisat2 = core.hisat2(index, path, fileFormat, parameters)

#FeatureCounts operator
featureCounts = core.featureCounts(gtf, path, parameters)

# EdgeR operator
edger = core.edgeR(path, condition, test, parameters)

# HAPPY operator
happy = core.happy(path, phenName,  parameters)

if __name__ == '__main__':
	# Check if reads are Single or Paired-end
	if len(files2) == 0:
		print("Single - end reads detected: Comencing DE analysis")
		for i in range(0,len(files1)):
			hisat2.alignSingle(files1[i])
		
		# Build array with alignment filenames from glob, to be used with FeatureCounts
		files3 = []
		files3 = core.getFiles('*.bam', path +'alignments/' , '/data/alignments/')
		for i in range(0,len(files3)):
			featureCounts.countSingle(files3[i])
	else:
		print("Paired - end reads detected: Comencing DE analysis\n(make sure that forward and reverse files are equal)")
		if len(files1) > len(files2) or len(files1) < len(files2):
			print("Forward and Reverse read files are not equal")
			quit()
		for i in range(0,len(files1)):
			hisat2.alignPaired(files1[i], files2[i])
		
		# Build array with alignment filenames from glob, to be used with FeatureCounts
		files3 = []
		files3 = core.getFiles('*.bam', path +'alignments/' , '/data/alignments/')
		for i in range(0,len(files3)):
			featureCounts.countPaired(files3[i])

	# Build the count matrix to be used with EdgeR
	core.buildMatrix(path, fileFormat)

	# Perform the DE test with EdgeR and move the summary file to the EdgeR folder
	edger.deTest('count_matrix.txt')
	subprocess.check_call(['mv', path + '/EdgeR_summary', path + '/EdgeR/'])

	# Filter the Genes List (defaults: p-value < 0.05 and |logFC| > 1) and produce the BioInfominer list
	files4=[]
	files4 = core.getFiles('*.tsv', path +'EdgeR/' , path +'EdgeR/')
	core.filter(path, files4[0])
	
	# Start the QTL analysis
	happy.qtl_map(inputFile)
