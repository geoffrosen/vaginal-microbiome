#!/usr/bin/env python

#gcstripper.py

#    Copyright (C) <2012>  <Benjamin C. Smith>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os, re, argparse, csv, fileinput
from collections import deque, Counter
import cPickle as Pickle
from numpy import zeros, hstack, vstack, array, arange




parser = argparse.ArgumentParser(
    description='''Convert a csv file produced by SQL queries on a guppy classify
    sqlite3 databse, to an OTU table .''',
    formatter_class= argparse.ArgumentDefaultsHelpFormatter,
    fromfile_prefix_chars='@')
parser.add_argument('-i','--input', nargs=1, required=True,
                    type=str, help='''input file. Should be a csv file
                    containing a list of classifications produced by
                    the sqlite3 command in sqlite3_script.sh on a "guppy
                    classify" SQL database.''')
parser.add_argument('-o', '--outpath', nargs='?', type=str,
                    help='''output path. The resulting OTU table is written
                    to this filename. If not set, creates a file in the current
                    directory called results_table.txt''')
parser.add_argument('-r', '--rank', nargs=1, type=str, default=['genus'],
                    help='''specify taxonomic rank at which to extract counts.
                    Acceptable arguments are "superkingdom", "phylum", "class",
                    "subclass", "order", "family", "genus", "species" or "otu".
                    The latter gives the deepest taxonomic classification
                    that has a maximum likelihood greater than the minimum
                    threshold (-c/--conf).''')
parser.add_argument('-c', '--conf', nargs=1, default=[0.8], type=float,
                    help='''set minimum acceptable maximum likelihood value for
                    an assignment to be counted.''')
parser.add_argument('-s', '--split_on', nargs=1, default=['_'], type=str,
                    help='''set the chracter to split the sample name on. E.g.,
                    if the read name is sample1_00001 and the split is set to
                    "_", the sample name will be read as "sample1".''')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='''activate verbose mode. Indicates progress and other
                    information.''')

#Setting required variables from command line arguments.
args = parser.parse_args()
infile = args.input[0]
outpath = args.outpath
rank = args.rank[0]
conf = args.conf[0]
split_on = args.split_on[0]
verbose = args.verbose


if not outpath:
    outpath = '/'.join(os.path.abspath(infile).split('/')[:-1]) + \
    "/results_table.txt"
try:
    os.mkdir('/'.join(outpath.split('/')[:-1]))
except OSError:
    pass

print "Running..."
    
inhandle = csv.reader(open(infile, "rb"), delimiter=',')#input file handle
outhandle = csv.writer(open(outpath, "wb"), dialect='excel', delimiter='\t')# output file handle

tax_ranks = ["root", "below_root", "superkingdon", "phylum", "class", "subclass"
            , "order", "family", "genus", "species"]
len_tr = len(tax_ranks)

inhandle.next()#skip first row of input file containing headers
#generate dictionary with keys = sample names, values = list of otus in sample
samples = {}
current = None
classification = {}
for j, row in enumerate(inhandle) :
    if verbose :#print line number to stdout
        sys.stdout.write("Line: " + str(j+1))
        sys.stdout.flush()
        sys.stdout.write("\b"*len("Line: " + str(j+1)))
    result = None
    read = str(row[0])
    sample = read.split(split_on)[0]
    tax_name = str(row[1])
    tax_level = str(row[2])
    likelihood = float(row[3])
    #if at start of run or on same read, set curent read name and add that
    #level's classification to the dictionary for the current read
    if current == None or current == read:
        current = read
        #test that confidence is high enough
        if likelihood > conf:
            classification[tax_level] = tax_name
    #if move onto a new read, must output the classification for the previous
    #read
    else:
        #attempt to retrieve classification at desired rank
        try:
            result = classification[rank]
        #if this fails, it means either that the read couldn't be classified
        #to that depth or that there is missing taxonomic information, as in the
        #case of unclassified sequences in the reference database
        except KeyError:
            #in case it is an unclassified case, seek the lowest level of
            #classification possible.
            try:
                #set counter equal to last position in tax_ranks
                if rank=="otu":
                    i = len_tr-1
                    #iterate until get to the shallowest classifcation level
                    while i >= 0:
                    #attempt to pull the classification at the level given by i.
                    #If a match is found at that level, return it, indicating
                    #that it is not at the desired rank.
                        try:
                            result = ''.join([classification[tax_ranks[i]],
" (", tax_ranks[i], ")"])
                            break
                        #if still no match at that level, decrement counter
                        except KeyError:
                            i -= 1
                else:
                    #set counter equal to 1 + position of desired rank in "tax_ranks"
                    i = 1+tax_ranks.index(rank)
                    #iterate until get to the end of "tax_ranks" or find a
                    #classification
                    while i < len_tr:
                        #attempt to pull the classification at the level given by i.
                        #If a match is found at that level, return it, indicating
                        #that it is not at the desired rank.
                        try:
                            result = ''.join([classification[tax_ranks[i]],
" (", tax_ranks[i],")"])
                            break
                        #if still no match at that level, increment counter
                        except KeyError:
                            i += 1
                             
            #if could not set i based on desired rank, it means the desired rank
            #is not in the list of understood ranks ("tax_ranks").
            except ValueError:
                print rank + " is and invalid taxonomic rank. Use -h/--help to\
see help documentation."
                sys.exit(3)  
        #if a result was returned, add it to the dictionary that keeps track
        #of all results for each sample
        if result:
            try:
                samples[sample].append(result)
            except KeyError:
                samples[sample] = [result]
        #since this is now a new read, reset the relevant variables and add
        #the information for this read to the, now empty, classification
        #dictionary
        current = read
        classification = {}
        if likelihood > conf:
            classification[tax_level] = tax_name


#generate list of sample ids and
#generate list of all observed otus (no duplicates)
sample_ids = []
otus = []
for key, otu_list in samples.items():
    sample_ids.append(str(key))
    for otu in otu_list:
        if otu not in otus:
            otus.append(otu)

#create empty count matrix
count_matrix = zeros( (len(otus), len(sample_ids)), dtype=int )

#populate count matrix with counts from samples dictionary
for key, values in samples.items():
    col = sample_ids.index(key)
    for value in values:
        row = otus.index(value)
        count_matrix[row, col] += 1

#construct output table
otu_ids = ["#OTU ID"] + list(arange(len(otus)))
otus = ["Consensus Lineage"] + otus
sample_ids = array(sample_ids)
len_otus = len(otus)
otus = array([[i] for i in otus])
otu_ids = array([[i] for i in otu_ids])
pre_table = vstack((sample_ids, count_matrix))
final_table = hstack((otu_ids, pre_table, otus))

outhandle.writerow([''.join(["#guppy classify ", rank, " table"])])
for row in final_table:
    outhandle.writerow(row)
            

print "\nFinished."

