# Example

This is an example to demonstrate a step – by – step guide on how to use the RNA – Seq – QTL analysis workflow. The layout of the folder and files above is according to the prerequisites described in 1.3 section.

### Note:
* For this example the datasets used for the RNA – Seq analysis were downloaded from a [study on the metabolic response to a high – fat diet](https://www.nature.com/articles/ijo201670) (for more details please see the Acknowledgements section)

* The HISAT2 mm10 index is freely accessible at: ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/data

* The GTF file used for this example was Mus_musculus.GRCm38.91.gtf. It is freely accessible from [Ensembl](http://www.ensembl.org/info/data/ftp/index.html/)

* The condensed files are freely accessible at: http://mtweb.cs.ucl.ac.uk/mus/www/preCC/MEGA_MUGA/Mar2015.MEGA+MDA+MUGA/CONDENSED/

* The dataset for the QTL analysis (mock.txt) is a mock sample derived from private data. The data file consists of the means of real data after a resampling method was performed on the original dataset

* The user is not required to create the folder /EdgeR/, or the DBW012.Rdata and count_matrix.txt files during the initial set up (they are used in this example to demonstrate the outputs of the workflow)

## Steps
**1.** Install the Docker engine

**2.** Pull the Docker images

**3.** Download core.py and wrapper.py (save both scripts in the same directory)

**4.** Create a working directory (e.g. ~/experiment1/). Inside the directory create the following subdirectories:
* ~/experiment1/reads1/ and ~/experiment1/reads2/ (where you should save the FASTQ files)
* ~/experiment1/CONDENSED/ (where you should save the condensed files)
* ~/experiment1/alignments/
* ~/experiment1/counts/

**5.** Download the RNA – Seq datasets (move _1.fastq files in /reads1/ and _2.fastq files in /reads2/), the condensed 
files (save them in /CONDENSED/), the QTL dataset, the GTF file and the parameters.json (save all 3 files in the default working 
directory ~/experiment1/)

**6.** Open up a terminal (Ctrl + Alt + T on Linux distributions) and issue the following commands:
```
$ cd /path/to/python/scripts
$ sudo python wrapper.py /path/to/experiment1/ fastq parameters.json
```
If everything is done correctly the user will be prompt to issue the tool-specific parameters 
(if you wish to reproduce the results, please enter the following arguments):
```
--------------HISAT2--------------
HISAT2 index: hisat2_index/mm10/mm10
----------------------------------

----------FeatureCounts-----------
GTF file: Mus_musculus.GRCm38.91.gtf
----------------------------------

---------------EdgeR--------------
Factors: ND,ND,ND,HP,HP,HP
Contrast of interest: ND-HP
----------------------------------

---------------HAPPY--------------
Phenotype Name: DBW012
Input File: mock.txt
----------------------------------
```

**7.** Estimate the Confidence Intervals for the QTL analysis (see Section 4. Estimating QTL Confidence Intervals). The command should be something like:
```
$ sudo docker run -v <path/to/working/dir/>:/tmp enios/rnaseq-qtl:happy Rscript /mnt/simlocus.dock.R /tmp/CONDENSED chr5 2235 5 DBW012 /tmp/mock.txt
```

## Acknowledgements
The RNA – Seq data were originally used for the assay on the phenotypic differences underpinning obesity susceptibility
or resistance based on metabolic and transcriptional profiling in C57BL/6J mice fed a high-fat diet 
(Choi JY, McGregor RA, Kwon EY, Kim YJ et al. The metabolic response to a high-fat diet reveals obesity-prone and -resistant 
phenotypes in mice with distinct mRNA-seq transcriptome profiles. Int J Obes (Lond) 2016 Sep;40(9):1452-60. PMID:27146467).

All the data are publicly [available](https://trace.ncbi.nlm.nih.gov/Traces/study/?acc=SRP065955) with the following SRA codes:
* **SRR2932702** - Normal Diet
* **SRR2932703** - Normal Diet
* **SRR2932704** - Normal Diet
* **SRR2932705** - High – Fat Diet
* **SRR2932706** - High – Fat Diet
* **SRR2932707** - High – Fat Diet
* **SRR2932708** - High – Fat Diet

We used the fastq-dump program of the [SRAtoolkit](https://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?view=software) 
to download the FASTQ files:

```
 $ fastq-dump --split-files -O /path/to/directory <SRA>
```
Where `<SRA>` is the SRA code for the specific sample (as described above).
The ––split-files argument is used because both reads for each replicate are stored in the same FASTQ file found in the 
repository.
