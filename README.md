![My image](https://github.com/e-nios/RNA-seq-QTL/blob/master/enios.png)

# RNA-seq-QTL
Workflow for Integration of RNAseq and QTL Analyses in Collaborative Cross Mice

This workflow is designed for automated integration analysis of RNA-seq and QTL (genotype/phenotype) data. The RNA-seq part is optimized for Illumina TruSeq Technology, so if the scripts are run on default parameters the user is required to input paired – end (forward – reverse) stranded Illumina reads.

## 1. Prerequisites

In order to run the scripts the user is required to:

### 1.1. Download Docker engine
The user is required to download and install the Docker engine. If you are unfamiliar with Docker please visit [Docker](https://docs.docker.com/install/)

### 1.2. Pull the images
After the Docker engine installation the user is required to pull the images from enios/rnaseq-qtl Docker Hub repository. The pull command should be something like:
```
$ sudo docker pull enios/rnaseq-qtl:<tag>
```
Where `<tag>` is the name of the specific tool needed for the workflow to run properly.

### Available images:
* enios/rnaseq-qtl:trim-galore
* enios/rnaseq-qtl:hisat2
* enios/rnaseq-qtl:featurecounts
* enios/rnaseq-qtl:edger
* enios/rnaseq-qtl:happy


If you are unfamiliar with Docker please clone the dockerPull.py script locally and run:

```
$ sudo python /path/to/script/dockerPull.py
```

### 1.3. Prepare the working directory
In order for the workflow to run the user is required to create a directory with the following files and folders

#### (1) reads1: FOLDER where the forward reads are stored
#### (2) reads2: FOLDER where the reverse reads are stored
#### (3) hisat2_index:  FOLDER where the index for HISAT2 is stored, if you need to download a specific index please visit the HISAT 2 index repository (ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/data)
#### (4) alignments: FOLDER where the aligned reads are stored (HISAT2 output)
#### (5) counts: FOLDER where the raw counts are stored (FeatureCounts output)
#### (6) CONDENSED: FOLDER where the condensed genotype data are stored (HAPPY input, please visit http://mtweb.cs.ucl.ac.uk/mus/www/preCC/MEGA_MUGA/Mar2015.MEGA+MDA+MUGA/CONDENSED/)
#### (7) file.gtf: a GTF FILE for the appropriate genome (for example Mus_musculus.GRCm38.91.gtf)
#### (8) data.txt: a TXT FILE with phenotypes (HAPPY input)
#### (9) parameters.json: a JSON FILE containing user specified parameters for each tool (optional)

### 1.4. Clone and run the scripts locally
The scripts should be downloaded and run from inside the same directory (core.py is called as a module inside wrapper.py and needs to be in the same directory):
```
$ cd /path/to/scripts/

$ sudo python wrapper.py <arguments>
```

## 2. Arguments
The command line arguments are divided into two categories. The Basic arguments that start the workflow using default parameters and the Advanced (optional) arguments that modify each tool according to the individual needs of the researcher.

### 2.1. Basic arguments
There are two (2) basic arguments the user is required to input in order for the scripts to run on default parameters:
#### a. Path to files/folders: the absolute path to the directory containing the folders and data for the RNA-seq – QTL workflow (see 1.3. Prepare the working directory)
#### b. The file format of the RNA-seq input files

For example, if the user has set up a working directory named “Experiment1” and the input files are FASTQ, the command should be something like:
```
$ sudo python wrapper /home/$user/Experiment1/ fastq
```
#### Note:
The script must be run with **sudo privileges** (on Linux distributions) in order for the docker daemon to launch the containers. 

### 2.2. Advanced arguments (optional)
If the user needs to modify the tool – specific arguments, he/she is required to input a JSON file (please see the JSON folder for more information) as an extra argument.
For example, if the user has set up a working directory named “Experiment1” and the input files are FASTQ, the command should be something like:
```
$ sudo python wrapper /home/$user/Experiment1/ fastq parameters.json
```

## 3. Tool – specific parameters
If the script is run with the correct arguments, the user will be prompt to input the following parameters:

### 3.1. HISAT2
**HISAT2 index**:	The basename of the index for the reference genome. The basename is the name of any of the index files up to but not including the final. For example if the index is stored in the working directory inside a folder named hisat2_index, the input should be **hisat2_index/mm10/mm10**.

### 3.2. FeatureCounts
**GTF File**: the GTF file name for the appropriate genome, for example **Mus_musculus.GRCm38.91.gtf**.

### 3.3. EdgeR
**Factors**: A string containing factors, for example if there are 6 biological replicates, 3 Normal and 3 Case the input should be **Normal,Normal,Normal,Case,Case,Case** (make sure that the order of the factors corresponds to the appropriate replicate).

**Contrast of interest**: A string containing the contrast of interest, following the previous example the input should be **Normal-Case** (or **Case-Normal**, depending on the contrast the user needs to test).

### 3.4. HAPPY
**Phenotype Name**: A string specifying the phenotype name in the data.txt file. For example **DB0123**.

**Input File**: A string specifying the input phenotype file for the QTL analysis. For example **data.txt** (the path to the file is not required, provided that it is inside the working directory as described in  1.3. Prepare the working directory).

## 4. Estimating QTL Confidence Intervals
If the user wishes to assess the CI of the QTL peak from the analysis performed in step 3.4, he/she is required to run the HAPPY Docker container with the following command:
```
$ sudo docker run -v <path/to/working/dir/>:/tmp enios/rnaseq-qtl:happy Rscript /mnt/simlocus.dock.R /tmp/CONDENSED <Chromosome> <Locus> <Chrom_Number> <Phenotype_Name> /tmp/<Input_File>
```
Where:

**Chromosome**: A string specifying the chromosome containing the QTL peak from the QTL analysis. For example **chr5** (the user is required to input the chr prefix)

**Locus**: An integer specifying the genetic locus of the QTL peak from the QTL analysis. For example **2235**.

**Chrom_Number**: An integer or character specifying the chromosome containing the QTL peak from the QTL analysis. For example **5** or **X**.

**Phenotype_Name**: A string specifying the phenotype name in the data.txt file. For example **DB0123**.

**Input_File**: A string specifying the input phenotype file for the QTL analysis. For example **data.txt** (the path to the file is not required, see above – section 3.4)

### Authors

* **Fotakis Giorgos** - *QTL-RNAseq analysis workflow development, Docker containerization*

### Acknowledgments

* **Binenbaum Ilona** - *QTL analysis*
* **Vlachavas Iason Efstathios** - *Rscripts development*

### Tools

* [BioInfoMiner](https://e-nios.com/bioinfominer/)
* [Trim-Galore!](https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/)
* [HISAT2](https://ccb.jhu.edu/software/hisat2/index.shtml)
* [FeatureCounts](http://bioinf.wehi.edu.au/featureCounts/)
* [EdgeR](http://bioconductor.org/packages/release/bioc/html/edgeR.html)
* [HAPPY](http://r-forge.r-project.org/projects/happy/)
