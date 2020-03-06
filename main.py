import os
from morphology import *
from viterbi import *
from preprocessing import *
from utilities import *
from score import *

def learnFromTraining(file):
	word_dict,pos_dict,tag_list,actual_w_list,actual_t_list = createDictionary(file)
	pos_dict['start'] = countstate('start',tag_list)
	emission_probabilities = createEmissionProbabilityMap(word_dict,pos_dict)
	transition = createTransitionMap(tag_list)
	transition_probabilities = createTransitionProbabilityMap(transition,pos_dict)
	prefix_prob,suffix_prob = createPrefixSuffixProbMap(createPrefixDict(actual_w_list,actual_t_list),createSuffixDict(actual_w_list,actual_t_list))
	return word_dict,pos_dict,tag_list,emission_probabilities,transition_probabilities,prefix_prob,suffix_prob


def test(trainfile,testfile):
	word_dict,pos_dict,tag_list,emission_probabilities,transition_probabilities,prefixp,suffixp = learnFromTraining(trainfile)
	file = open(testfile,"r")
	unknown = count_unknown(file)
	file = open(testfile,"r")
	words = []
	for line in file:
		words.append(line.rstrip())
	pos=[]
	new_sentence=[]
	for i in range(0,len(words)):
		if words[i]=='' or words[i]=='\n':
			v,p = viterbi(new_sentence,emission_probabilities,transition_probabilities,pos_dict,prefixp,suffixp,unknown)
			tags = bestPath(new_sentence,v,p,transition_probabilities.keys())
			tags.append('')
			tags=tags[1:]
			pos.extend(tags)
			new_sentence=[]
		else:
			new_sentence.append(words[i])
	return pos,words

def main():
	f1 = open("WSJ_02-21.pos","r")
	file2 = "WSJ_24.words"
	p,w=test(f1,file2)
	writeToFile(p,w)
	score("WSJ_24.pos","test.pos")
	os.remove("test.pos")
	f1 = open("WSJ.pos","r")
	file2 = "WSJ_23.words"
	p,w=test(f1,file2)
	writeToFile(p,w)
main()

