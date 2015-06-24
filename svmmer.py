# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from sklearn import svm

main()

def main():
    refseqs = []
    with open('RDP_seqs_upper_trimmed.fasta','rU') as f:
        for line in f:
            if line.startswith('>'):
                continue
            else:
                refseqs.append(line.rstrip())
    feats = generate_possible_features(refseqs)
    return feats

def generate_possible_features(refseqs):
    return set(''.join(refseqs))
    