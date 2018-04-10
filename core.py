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
	O = open(path + '/EdgeR/BIM_list.txt', "w")
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
	def __init__(self, index, base_dir, fileExtention, jsonArgs = None, singleEnd = None, reads = '-q', orientation = '--fr'):
		if isinstance(jsonArgs, dict):
			self.index = index
			self.base_dir = base_dir
			self.fileExtention = fileExtention
			self.reads=jsonArgs['hisat2']['reads']
			self.orientation=jsonArgs['hisat2']['orientation']
		else:
			self.index = index
			self.base_dir = base_dir
			self.fileExtention = fileExtention
			self.reads = reads
			self.orientation = orientation

	def alignPaired(self, inputFile1, inputFile2):
		subprocess.check_call(['docker', 'run', '-v', '%s:/data/' % self.base_dir,
			'enios/rnaseq-qtl:hisat2', 'hisat2', self.orientation, self.reads, '-x', '/data/%s' % self.index, '-1', '%s' % 
			inputFile1, '-2', '%s' % inputFile2, '-S', '/data/alignments/%s.bam' % inputFile1.split('/')[3].rstrip('.%s' % self.fileExtention)])

	def alignSingle(self, inputFile):
		subprocess.check_call(['docker', 'run', '-v', '%s:/data/' % self.base_dir,
			'enios/rnaseq-qtl:hisat2', 'hisat2', self.reads, '-x', '/data/%s' % self.index, '-U', '%s' % 
			inputFile, '-S', '/data/alignments/%s.bam' % inputFile.split('/')[3].rstrip('.%s' % self.fileExtention)])

class featureCounts(object):
    def __init__(self, gtf, base_dir, jsonArgs=None, fileFormat = 'GTF', featureType = 'gene', attributeType = 'gene_name',  strandness = 2, threads = 1):
    	if isinstance(jsonArgs, dict):
			self.gtf = gtf
			self.base_dir = base_dir
			self.fileFormat = jsonArgs['featureCounts']['fileFormat']
			self.featureType = jsonArgs['featureCounts']['featureType']
			self.attributeType = jsonArgs['featureCounts']['attributeType']
			self.strandness = jsonArgs['featureCounts']['strandness']
			self.threads = jsonArgs['featureCounts']['threads']
        else:
			self.gtf = gtf
			self.base_dir = base_dir
			self.fileFormat = fileFormat
			self.featureType = featureType
			self.attributeType = attributeType
			self.strandness = strandness
			self.threads = threads
   
    def countPaired(self, inputFile):
		subprocess.check_call(['docker', 'run', '-v', '%s:/data/' % self.base_dir,
                'enios/rnaseq-qtl:featurecounts', 'featureCounts', '-F', self.fileFormat, '-t', self.featureType, '-g', self.attributeType, '-s%s' % self.strandness, 
                '-T%s' % self.threads , '-p', '-a', '/data/%s' % self.gtf, '%s' % inputFile, '-o', '/data/counts/%s.txt' % inputFile.split('/')[3].rstrip('.bam')])

    def countSingle(self, inputFile):
		subprocess.check_call(['docker', 'run', '-v', '%s:/data/' % self.base_dir,
                'enios/rnaseq-qtl:featurecounts', 'featureCounts', '-F', self.fileFormat, '-t', self.featureType, '-g', self.attributeType, '-s%s' % self.strandness, 
                '-T%s' % self.threads , '-a', '/data/%s' % self.gtf, '%s' % inputFile, '-o', '/data/counts/%s.txt' % inputFile.split('/')[3].rstrip('.bam')])

class edgeR(object):
	def __init__(self, base_dir, condition, test, jsonArgs = None, logFC = 0.0, pValue = 0.05, pAdjust = 'BH', normalization = 'TMM'):
		if isinstance(jsonArgs, dict):
			self.base_dir = base_dir
			self.condition = condition
			self.test = test
			self.logFC = jsonArgs['edger']['logFC']
			self.pValue = jsonArgs['edger']['pValue']
			self.pAdjust = jsonArgs['edger']['pAdjust']
			self.normalization = jsonArgs['edger']['normalization']
		else:
			self.base_dir = base_dir
			self.condition = condition
			self.test = test
			self.logFC = logFC
			self.pValue = pValue
			self.pAdjust = pAdjust
			self.normalization = normalization

	def deTest(self, inputFile):
		subprocess.check_call(['docker', 'run', '-v', '%s:/tmp/' % self.base_dir,
                'enios/rnaseq-qtl:edger', 'Rscript', '/mnt/edger.R', '-R', 
                '/tmp/EdgeR_summary', '-o', '/tmp/EdgeR', '-m', '/tmp/%s' % inputFile,
                '-i', self.condition, '-C', self.test, '-l', '%s' % self.logFC, '-p', '%s' % self.pValue, '-d', self.pAdjust, '-n', self.normalization, '-b'])

class happy(object):
	def __init__(self, baseDir, pheName, jsonArgs = None, permutations = 1000):
		if isinstance(jsonArgs, dict):
			self.baseDir = baseDir
			self.pheName = pheName
			self.permutations = jsonArgs["happy"]["permutations"]
		else:
			self.baseDir = baseDir
			self.pheName = pheName
			self.permutations = permutations

	def qtl_map(self, inputFile):
		subprocess.check_call(['docker', 'run', '-v', '%s:/tmp/' % self.baseDir, 'enios/rnaseq-qtl:happy', 'Rscript', '/mnt/happy.dock.R', 
			'/tmp/CONDENSED', '/tmp/%s' % inputFile, self.pheName, "%s" % self.permutations, '/tmp/%s.Rdata' % self.pheName])

	def ci_est(self, inputFile, chrom, locus):
		subprocess.check_call(['docker', 'run', '-v', '%s:/tmp/' % self.baseDir, 'enios/rnaseq-qtl:happy', 'Rscript', '/mnt/simlocus.dock.R', 
			'/tmp/CONDENSED', chrom, "%s" % locus, "%s" % chrom.lstrip("chr"), self.pheName, '/tmp/%s' % inputFile])
