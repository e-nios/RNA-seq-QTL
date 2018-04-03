# Advanced Arguments – JSON file

This workflow is designed for automated downstream analysis of RNA-seq and μ-array data. The RNA-seq part is optimized for Illumina TruSeq Technology, so if the scripts are run on default parameters the user is required to input paired – end (forward – reverse) reversely stranded Illumina reads. However, the user can modify the parameters.json and use different tool parameters.

In order access the tool – specific parameters the user is required to create a JSON file (using the parameters.json template) or copy and modify the above file. The workflow can automatically detect whether paired – end or single – end reads are being used and adapt accordingly (for more information please read the following paragraphs). 

## 1.Paired – end reads

For paired – end reads the user is required to store the reads in the folders specified in "1.3. Prepare the working directory". Please **make sure** that the reads are in /reads1/ and /reads2/ **folders** respectively, that the **names** are similar (for example DT_189_read1.fastq and  DT_189_read2.fastq) and that the reads are **equal** in numbers.

### JSON file parameters
If you wish to modify the JSON file (or create a new one) please make sure that the first argument for each parameter **remains the same**. The first argument (`<arg1>`) of the template **`<arg1>`**:`<arg2>` must be the same string in all cases. For example if you are using QSEQ read files and you wish to make sure that HISAT2 can recognize the correct file format change the arguments **”reads”:“-q”** to **”reads”:“--qseq”** and so on.

#### 1.1. HISAT2
**”reads”**:	**“-q”** - Reads are FASTQ files. FASTQ files usually have extension .fq, .fastq or fastq.gz. “--qseq” should be used when the reads are QSEQ files. QSEQ files usually end in _qseq.txt. ("-q" by **default**)

**”orientation”**:	**”--fr”** - The upstream/downstream mate orientations for a valid paired-end alignment against the forward reference strand. E.g., if **”--fr”** is specified and there is a candidate paired-end alignment where mate 1 appears upstream of the reverse complement of mate 2, that alignment is valid. Also, if mate 2 appears upstream of the reverse complement of mate 1 and all other constraints are met, that too is valid. **”--rf”** likewise requires that an upstream mate1 be reverse-complemented and a downstream mate2 be forward-oriented. **”--ff”** requires both an upstream mate 1 and a downstream mate 2 to be forward-oriented. **Default**: “--fr” (appropriate for Illumina's Paired-end Sequencing Assay).

#### 1.2. FeatureCounts
**"fileFormat"**:	**"GTF"** - Specify the format of the annotation file. Acceptable formats include “GTF” and “SAF”. “GTF” by **default**.

**"featureType"**:**"gene"**, Specify the feature type (for example “gene”, “exon” etc.) Only rows which have the matched feature type in the provided GTF annotation file will be included for read counting. “gene” by **default**.

**"attributeType"**:**"gene_name"** - Specify the attribute type (for example “gene_id”, “gene_name” etc.) used to group features (eg.  exons) into meta-features (eg.  genes) when GTF annotation is provided. “gene_id” by **default**. This attribute type is usually the gene identifier.  This argument is useful for the meta-feature level summarization.
			

**"strandness"**:**"2"** - Indicate if strand-specific read counting should be performed. It has three **possible values**:  **”0”** (unstranded), **”1”** (stranded) and **”2”**  (reversely  stranded). "2"  by **default**.

**"threads"**:**"4"** - Number of the threads. The value should be between 1 and 32. “1” by **default**.

#### 1.3. EdgeR
**"logFC"**:	**"0.0"** - Float specifying the log-fold-change requirement. “0.0” by **default**.

**"pValue"**:	**"0.05"** - Float specifying the p – value requirement. “0.05” by **default**

**"pAdjast"**:	**"BH"** - String specifying the p-value adjustment method. The adjustment methods include Benjamini & Hochberg (1995) ("BH"), and Benjamini & Yekutieli (2001) ("BY"). “BH” by **default**.

**"normalization"**:	**"TMM"** - String specifying type of normalisation used. Should be one of “TMM” (Trimmed Mean of M values), “RLE” (Relative Log Expression), “upperquartile” or “none”. “TMM” by **default**.

#### 1.4. HAPPY
**"permutations"**: **"1000"** - Number of permutations to be performed by HAPPY for the QTL analysis. 1000 by **default**.

## 2. Single – end reads

For Single – end reads the user is required to store all the reads in the folder specified as /reads1/ **only**. Please **make sure** that all the reads are in /reads1/ **folder**.

The script will automatically detect that Single – end reads are used and adjust accordingly. The user can modify all the above parameters as described in the previous section.

**Note**: For single – end reads the FeatureCounts **”strandness”** parameter is not required (as it is paired – end read specific), the user may leave the default or input an empty string (**””**).
