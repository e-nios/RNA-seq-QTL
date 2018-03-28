![My image](https://github.com/e-nios/RNA-seq-QTL/blob/master/enios.png)

# RNA-seq-QTL
Workflow for Integration of RNAseq and QTL Analyses in Collaborative Cross Mice

This workflow is designed for automated integration analysis of RNA-seq and μ-array data. The RNA-seq part is optimized for Illumina TruSeq Technology, so if the scripts are run on default parameters the user is required to input paired – end (forward – reverse) stranded Illumina reads.

## Prerequisites

In order to run the scripts the user is required to:

### 1. Download Docker engine
The user is required to download and install the Docker engine. If you are unfamiliar with Docker please visit [Docker](https://docs.docker.com/install/)

### 2. Pull the images
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

### 3. Prepare the working directory
In order for the workflow to run the user is required to create a directory with the following files and folders

#### (1) reads1: FOLDER where the forward reads are stored
#### (2) reads2: FOLDER where the reverse reads are stored
#### (3) hisat2_index:  FOLDER where the index for HISAT2 is stored, if you need to download a specific index please visit the HISAT 2 index repository (ftp://ftp.ccb.jhu.edu/pub/infphilo/hisat2/data)
#### (4) alignments: FOLDER where the aligned reads are stored (HISAT2 output)
#### (5) counts: FOLDER where the raw counts are stored (FeatureCounts output)
#### (6) CONDENSED: FOLDER where the condensed data are stored (HAPPY input, please visit)
#### (7) file.gtf: a GTF FILE for the appropriate genome (for example Mus_musculus.GRCm38.91.gtf)
#### (8) data.txt: a TXT FILE (HAPPY input)

### 4. Clone and run the scripts locally
The scripts should be downloaded and run from inside the same directory (core.py is called as a module inside wrapper.py and needs to be in the same directory):
```
$ cd /path/to/scripts/

$ sudo python wrapper.py <arguments>
```

## Authors

* **Fotakis Giorgos** - *QTL-RNAseq analysis workflow development, Docker containerization*

## Acknowledgments

* **Binenbaum Ilona** - *QTL analysis*
* **Vlachavas Eustathios** - *Rscripts development*
