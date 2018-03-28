#!usr/bin/env python

import subprocess

subprocess.check_call(['docker', 'pull', 'enios/rnaseq-qtl:trim-galore'])

subprocess.check_call(['docker', 'pull', 'enios/rnaseq-qtl:hisat2'])

subprocess.check_call(['docker', 'pull', 'enios/rnaseq-qtl:featurecounts'])

subprocess.check_call(['docker', 'pull', 'enios/rnaseq-qtl:edger'])

subprocess.check_call(['docker', 'pull', 'enios/rnaseq-qtl:happy'])
