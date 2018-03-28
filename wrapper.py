#!usr/bin/env python

import sys
import glob, os
import subprocess
import core

# Parameters
files1 = []
files2 = []
files3 = []
path = '/media/pestilence/Data/testFolder2/'
index = 'hisat2_index/mm10/mm10'
gtf = 'Mus_musculus.GRCm38.91.gtf'
extention = 'fastq.gz'

# EdgeR parameters
output1 = 'edgeOut1'
output2 = 'edgeOut2'
condition = 'Condition::O,O,N,N'
test = 'O-N'

# Build arrays with reads filenames from glob, to be used with HISAT2
files1 = de.getFiles('*1.%s' % extention, path +'reads1/', '/data/reads1/')

files2 = de.getFiles('*2.%s' % extention, path +'reads2/', '/data/reads2/')

files1.sort()

files2.sort()

#HISAT2 operator
hisat2 = core.hisat2(index, path)

#FeatureCounts operator
featureCounts = core.featureCounts(gtf, path)

# EdgeR operator
edger = core.edgeR(path, output1, output2, condition, test)

# HAPPY operator
happy = core.happy(path, condensed, 'DBW012', base_dir)

if __name__ == '__main__':
# check if read files are equal
	if len(files1) != len(files2):
		print("ERROR: Make sure that Read1 files (forward reads) and Read2 files (reverse reads) are equal")

	else:
		for i in range(0,len(files1)):
			hisat2.align(files1[i], files2[i])
# Build array with alignment filenames from glob, to be used with FeatureCounts
	files3 = core.getFiles('*.bam', path +'alignments/' , '/data/alignments/')

	for i in range(0,len(files3)):
		featureCounts.count(files3[i])
# Build the count matrix to be used with EdgeR
	core.buildMatrix(path, extention)
# Perform the DE test with EdgeR
	edger.deTest('count_matrix.txt')
# Filter the Genes List (defaults: p-value <= 0.05 and |logFC| > 1) and produce the BioInfominer list
	files4 = core.getFiles('*.tsv', path +'edgeOut2/' , path +'edgeOut2/')
	de.filter(files4[0])
# Start the QTL analysis
	happy.qtl_map()
	happy.ci_est()
