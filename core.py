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

def filter(path, fileName, logFC = 1, pValue = 0.05):
	gene_id=[]
	log_fc=[]
	p_value=[]
	F = open(fileName, "r") 
	O = open(path + '/edgeOut2/BIM_list.txt', "w")
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
	def __init__(self, index, base_dir, fileExtention, jsonArgs=None, singleEnd=None, reads = '-q', orientation = '--fr'):
		if isinstance(jsonArgs, dict):
			self.index = index
			self.base_dir = base_dir
			self.fileExtention = fileExtention
			self.reads=jsonArgs['hisat2'][0]
			self.orientation=jsonArgs['hisat2'][1]
		else:
			self.index = index
			self.base_dir = base_dir
			self.fileExtention = fileExtention
			self.reads = reads
			self.orientation = orientation

	def alignPaired(self, input_files1, input_files2):
		subprocess.check_call(['docker', 'run', '-v', '%s:/data/' % self.base_dir,
			'enios/rnaseq-qtl:hisat2', 'hisat2', self.orientation, self.reads, '-x', '/data/%s' % self.index, '-1', '%s' % 
			input_files1, '-2', '%s' % input_files2, '-S', '/data/alignments/%s.bam' % input_files1.split('/')[3].rstrip('1.%s' % self.fileExtention)])

	def alignSingle(self, input_files):
		subprocess.check_call(['docker', 'run', '-v', '%s:/data/' % self.base_dir,
			'enios/rnaseq-qtl:hisat2', 'hisat2', self.reads, '-x', '/data/%s' % self.index, '-U', '%s' % 
			input_files, '-S', '/data/alignments/%s.bam' % input_files.split('/')[3].rstrip('1.%s' % self.fileExtention)])

class featureCounts(object):
    def __init__(self, gtf, base_dir, jsonArgs=None, fileFormat = 'GTF', featureType = 'gene', attributeType = 'gene_name',  strandness = 2, threads = 1):
    	if isinstance(jsonArgs, dict):
			self.gtf = gtf
			self.base_dir = base_dir
			self.fileFormat = jsonArgs['featureCounts'][0]
			self.featureType = jsonArgs['featureCounts'][1]
			self.attributeType = jsonArgs['featureCounts'][2]
			self.strandness = jsonArgs['featureCounts'][3]
			self.threads = jsonArgs['featureCounts'][4]
        else:
			self.gtf = gtf
			self.base_dir = base_dir
			self.fileFormat = fileFormat
			self.featureType = featureType
			self.attributeType = attributeType
			self.strandness = strandness
			self.threads = threads
   
    def countPaired(self, input_file):
		subprocess.check_call(['docker', 'run', '-v', '%s:/data/' % self.base_dir,
                    'enios/rnaseq-qtl:featurecounts', 'featureCounts', '-F', self.fileFormat, '-t', self.featureType, '-g', self.attributeType, '-s%d' % self.strandness, 
                    '-T%d' % self.threads , '-p', '-a', '/data/%s' % self.gtf, '%s' % input_file, '-o', '/data/counts/%s.txt' % input_file.split('/')[3].rstrip('.bam')])

    def countSingle(self, input_file):
		subprocess.check_call(['docker', 'run', '-v', '%s:/data/' % self.base_dir,
                    'enios/rnaseq-qtl:featurecounts', 'featureCounts', '-F', self.fileFormat, '-t', self.featureType, '-g', self.attributeType, '-s%d' % self.strandness, 
                    '-T%d' % self.threads , '-a', '/data/%s' % self.gtf, '%s' % input_file, '-o', '/data/counts/%s.txt' % input_file.split('/')[3].rstrip('.bam')])

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
                    'enios/rnaseq-qtl:edger', 'Rscript', '/mnt/edger.R', '-R', 
                    '/tmp/%s' % self.output1, '-o', '/tmp/%s' % self.output2, '-m', '/tmp/%s' % input_file,
                    '-i', self.condition, '-C', self.test, '-l', '0.0', '-p', '0.05', '-d', 'BH', '-n', self.normalization, '-b'])

class happy(object):
	def __init__(self, base_dir, condensed, phen_name, output1):
		self.base_dir = base_dir
		self.condensed = condensed
		self.phen_name = phen_name
		self.output1 = output1
		self.cmd1 = ['docker', 'run', '-v', '%s:/tmp/' % self.base_dir, 'enios/rnaseq-qtl:happy', 'Rscript', '/mnt/happy.dock.R', 
			'/tmp/%s' % self.condensed, '/tmp/happy_docker/data.file.txt', self.phen_name, '1000', '/tmp/%s' % 'DBW012.Rdata']
		self.cmd2 = ['docker', 'run', '-v', '%s:/tmp/' % self.base_dir, 'enios/rnaseq-qtl:happy', 'Rscript', '/mnt/simlocus.dock.R', 
			'/tmp/%s' % self.condensed, 'chr5', '2235', '5', self.phen_name, '/tmp/happy_docker/data.file.txt']

	def qtl_map(self):
		subprocess.check_call(self.cmd1)

	def ci_est(self):
		subprocess.check_call(self.cmd2
