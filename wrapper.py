#!usr/bin/env python

import sys
import json
import core


# EdgeR parameters
output1 = 'edgeOut1'
output2 = 'edgeOut2'
condition = 'Condition::O,O,N,N'
test = 'O-N'

# Happy parameters
condensed = 'CONDENSED'

# Input parameters
files1 = []
files2 = []
files3 = []
parameters=None
path = sys.argv[1]
index = sys.argv[2]
gtf = sys.argv[3]
extention = sys.argv[4]
try:
	parameters = json.loads(sys.argv[5])
except: 
	IndexError

# Build arrays with read filenames from glob, to be used with HISAT2
files1 = core.getFiles('*1.%s' % extention, path +'reads1/', '/data/reads1/')
files2 = core.getFiles('*2.%s' % extention, path +'reads2/', '/data/reads2/')

files1.sort()
files2.sort()

#HISAT2 operator
hisat2 = core.hisat2(index, path, extention, parameters)

#FeatureCounts operator
featureCounts = core.featureCounts(gtf, path, parameters)

# EdgeR operator
edger = core.edgeR(path, output1, output2, condition, test)

# HAPPY operator
happy = core.happy(path, condensed, 'DBW012', path)

if __name__ == '__main__':
	# check if read files are equal and if yes run HISAT2 alignment
	if len(files2) == 0:
		print("Single - end reads detected: Comencing DE analysis")
		for i in range(0,len(files1)):
			hisat2.alignSingle(files1[i])
		# Build array with alignment filenames from glob, to be used with FeatureCounts
		files3 = core.getFiles('*.bam', path +'alignments/' , '/data/alignments/')
		for i in range(0,len(files3)):
			featureCounts.countSingle(files3[i])
	else:
		print("Paired - end reads detected: Comencing DE analysis")
		for i in range(0,len(files1)):
			hisat2.alignPaired(files1[i], files2[i])
		# Build array with alignment filenames from glob, to be used with FeatureCounts
		files3 = core.getFiles('*.bam', path +'alignments/' , '/data/alignments/')
		for i in range(0,len(files3)):
			featureCounts.countPaired(files3[i])
	# Build the count matrix to be used with EdgeR
	de.buildMatrix(path, extention)
	# Perform the DE test with EdgeR
	edger.deTest('count_matrix.txt')
	# Filter the Genes List (defaults: p-value <= 0.05 and |logFC| > 1) and produce the BioInfominer list
	files4 = core.getFiles('*.tsv', path +'edgeOut2/' , path +'edgeOut2/')
	core.filter(files4[0])
	# Start the QTL analysis
	happy.qtl_map()
	happy.ci_est()
