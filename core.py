#!usr/bin/env python

import subprocess
import glob, os
import pandas as pd

def getFiles(extention, path1, path2):
	os.chdir(path1)
	files = []
	for file in glob.glob(extention):
    		file_name = path2 + file
    		files.append(file_name)
    	return files

def buildMatrix(path, extention):
	files = []
	file_names = []
	os.chdir(path + 'counts/')
	
	for file in glob.glob('*.txt'):
		file_name = path + 'counts/' + file
		files.append(file_name)
		file_names.append('/data/alignments/' + file.rstrip('.txt'))
	tmp = pd.read_csv(files[0], sep = "\t", header = 1)
	count_matrix = tmp['Geneid']
	
	for i in range(0,len(files)):
		counts = pd.read_csv(files[i], sep = "\t", header = 1)
		raw_counts = counts['%s.bam' % file_names[i]]
		count_matrix = pd.concat([count_matrix,raw_counts], axis=1)

	count_matrix.columns = count_matrix.columns.str.replace('/data/alignments/','')
	count_matrix.columns = count_matrix.columns.str.replace(extention + '.bam','')
	count_matrix.to_csv(path + 'count_matrix.txt', sep = '	', index=False, header=True)

def filter(fileName, logFC = 1, pValue = 0.05):
	gene_id=[]
	log_fc=[]
	p_value=[]

	F = open(fileName, "r") 
	O = open('/media/pestilence/Data/testFolder2/edgeOut2/BIM_list.txt', "w")

	next(F)
	for line in F:
		gene_id=(line.replace("\"","").split("\t")[0])
		log_fc=(line.replace("NA", "0").split("\t")[1])
		p_value=(line.replace("NA", "1").rstrip().split("\t")[4])
		if float(log_fc) != 0 and float(p_value) <= pValue and (float(log_fc)<=-logFC or float(log_fc)>=logFC):
			O.writelines(gene_id+"\t"+log_fc+"\t"+p_value+"\n")

	F.close()
	O.close()

class hisat2(object):
    def __init__(self, index, base_dir, *args):
        self.index = index
        self.base_dir = base_dir

    def align(self, input_file1, input_file2):
        subprocess.check_call(['docker', 'run', '-v', '%s:/data/' % self.base_dir,
                    'hisat2', 'hisat2', '-x', '/data/%s' % self.index, '-q', '-1', '%s' % 
                    input_file1, '-2', '%s' % input_file2, '-S', '/data/alignments/%s.bam' % input_file1.split('/')[3].rstrip('1.fastq')])

class featureCounts(object):
    def __init__(self, gtf, base_dir, strandness = 2, *args):
        self.gtf = gtf
        self.base_dir = base_dir
	self.strandness = strandness
   
    def count(self, input_file):
        subprocess.check_call(['docker', 'run', '-v', '%s:/data/' % self.base_dir,
                    'featurecounts', 'featureCounts', '-s%d' % self.strandness, '-T', '8', '-F', 'GTF', '-p', '-t', 'gene', '-g', 'gene_name', '-a', '/data/%s' % self.gtf, 
                    '%s' % input_file, '-o', '/data/counts/%s.txt' % input_file.split('/')[3].rstrip('.bam')])

class edgeR(object):
	def __init__(self, base_dir, output1, output2, condition, test, normalization='TMM', *args):
		self.base_dir = base_dir
		self.output1 = output1
		self.output2 = output2
		self.condition = condition
		self.test = test
		self.normalization = normalization

	def deTest(self, input_file):
		subprocess.check_call(['docker', 'run', '-v', '%s:/tmp/' % self.base_dir,
                    'edger', 'Rscript', '/mnt/edger.R', '-R', 
                    '/tmp/%s' % self.output1, '-o', '/tmp/%s' % self.output2, '-m', '/tmp/%s' % input_file,
                    '-i', self.condition, '-C', self.test, '-l', '0.0', '-p', '0.05', '-d', 'BH', '-n', self.normalization, '-b'])

class happy(object):
	def __init__(self, base_dir, condensed, phen_name, output1):
		self.base_dir = base_dir
		self.condensed = condensed
		self.phen_name = phen_name
		self.output1 = output1
		self.cmd1 = ['docker', 'run', '-v', '%s:/tmp/' % self.base_dir, 'happy', 'Rscript', '/mnt/happy.dock.R', 
			'/tmp/%s' % self.condensed, '/tmp/happy_docker/data.file.txt', self.phen_name, '1000', '/tmp/%s' % 'DBW012.Rdata']
		self.cmd2 = ['docker', 'run', '-v', '%s:/tmp/' % self.base_dir, 'happy', 'Rscript', '/mnt/simlocus.dock.R', 
			'/tmp/%s' % self.condensed, 'chr5', '2235', '5', self.phen_name, '/tmp/happy_docker/data.file.txt']

	def qtl_map(self):
		subprocess.check_call(self.cmd1)

	def ci_est(self):
		subprocess.check_call(self.cmd2)
