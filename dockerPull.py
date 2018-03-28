#!usr/bin/env python

import subprocess

subprocess.check_call(['docker', 'pull', 'mebp/qtl-rnaseq-workflow:trim-galore'])

subprocess.check_call(['docker', 'pull', 'mebp/qtl-rnaseq-workflow:hisat2'])

subprocess.check_call(['docker', 'pull', 'mebp/qtl-rnaseq-workflow:featurecounts'])

subprocess.check_call(['docker', 'pull', 'mebp/qtl-rnaseq-workflow:edger'])

subprocess.check_call(['docker', 'pull', 'mebp/qtl-rnaseq-workflow:happy'])
