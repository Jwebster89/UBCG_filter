#!/usr/bin/env python

from Bio import SeqIO
from collections import defaultdict
from collections import Counter
import os,sys,argparse,logging


parser = argparse.ArgumentParser(description="Finds subset of isolates and UBCG genes to produce UBCG alignments with only those isolates that meet the criteria",add_help=False)

required = parser.add_argument_group('Required Arguments')
required.add_argument('-p', '--path', type=str, required=True, help="absolute directory of UBCG output folder")
required.add_argument('-i', '--isolates', type=str, required=True, help="a list of user provided isolates to be included in final output if UBCGs greater than threshold")

optional = parser.add_argument_group('Optional Arguments')
optional.add_argument("-h", "--help", action="help", help="show this help message and exit")
optional.add_argument('-t', '--threshold', type=int, default=85, help="minimum number of UBCGs to include in final output (default 85)")


args=parser.parse_args()

threshold=args.threshold
isolates=args.isolates
path=os.path.normpath(args.path)

prefix=os.path.basename(os.path.normpath(path))


"""
Usage: python UBCG_filter.py <-p UBCG_output_path> <-i isolate list>
e.g python UBCG_filter.py -p /home/jwebster89/UBCG/output_experiment1 -i isolate.list -t 88
"""

#Find all fasta files in directory of UBCG minus any files that don't start with the output name + .align
def get_sequence_list(dir):
	fastas=[]
	files=os.listdir(dir)
	for file in files:
		(shortname, extension) = os.path.splitext(file)
		if extension == ".fasta":
			if shortname[len(prefix):len(prefix)+6]== ".align":
				fastas.append(file)
			else:
				continue
		else:
			continue
	return(fastas)

#Creates Dictionary of Isolates (key) and number of UBCG genes (value) that were found in the isolates.
def UBCG_count(list):
	sequence_count_d=defaultdict(int)
	for fasta in list:
		for seq_record in SeqIO.parse(os.path.join(path, fasta), "fasta"):
			sequence_count_d[seq_record.id]+=1
	return(sequence_count_d)

#Counts the occurence of UBCGs across all isolates and returns a list of sequences for the final output
def print_dict(dict, isolate_list):
	with open(isolate_list) as f:
		lines = [line.rstrip() for line in f]
	max_key=max(dict, key=dict.get)
	outseq_list=[]
	unused_list=[]
	for key in dict:
		if dict[key] == dict[max_key]: # if the count of UBCGs in isolate = the max count seen in set, then add it to the output list
			outseq_list.append(key)
		elif key in lines and dict[key] >= threshold: # if the count of UBCGS for a list of sequenced isolates (not references) is more than threshold (default 85), then add it to the output list and report that the isolate has less.
			outseq_list.append(key)
			print("Warning: " + key + " Only has " + str(dict[key]) + "  UBCGS, but has still been added to output. Remove from isolate list to exclude from analysis")
		elif key in lines and dict[key] < threshold: # if the count of UBCGs is less than threshold (default 85) in a set of sequenced isolates (not references), exclude from analysis.
			print("Error: "+ key + " has been excluded from output as it only has " + str(dict[key]) + " UBCGs")
			unused_list.append(key)
		else:
			unused_list.append(key)

#Creates a counter of how many isolates have how many UBCGs. Useful for understanding distribution of UBCGS.
	unique_values=set(dict.values())
	counter = Counter(dict.values())
	#counts_counter = Counter(counter.values())
	print('\nDistribution of UBCGS:')
	for i in counter:
		if counter[i] == 1:
			print("There is " + str(counter[i]) + " isolate with " + str(i) + " UBCGs")
		else:
			print("There are " + str(counter[i]) + " isolates with " + str(i) + " UBCGs")
	
	with open('unused.txt', 'w') as g:
		for item in unused_list:
			g.write("%s\n" % item)
	print("\nList of unused samples saved to 'unused.txt'")
	return(outseq_list)


#Writes new fasta files with only the sequences from the outseq_list
def UBCG_filter(seq_list, outseq_list):
	print("\nFiltering fasta files, this may take a while depending on number of samples")
	for fasta in seq_list: # For each fasta file
		match_fasta=[]
		for isolate in outseq_list: # and for each isolate in the outseq_list
			for seq_record in SeqIO.parse(os.path.join(path, fasta), "fasta"): # for each fasta in the fasta file
				if seq_record.id == isolate: #if the isolate in the alignment is in the outseq list, add to a new file
					match_fasta.append(seq_record)
		if len(match_fasta) == len(outseq_list): #only write that file if it contains all isolates (removes the UBCGs that sequenced isolates were missing).
			SeqIO.write(match_fasta, os.path.join(path,"filtered_" + fasta), 'fasta') 
		else:
			print(fasta + " excluded from output")
	print("\nDone!")


def main():
	sequences=get_sequence_list(path)
	dict=UBCG_count(sequences)
	outseq_list=print_dict(dict,isolates)
	UBCG_filter(sequences, outseq_list)

main()
