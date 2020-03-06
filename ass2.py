import os
from copy import deepcopy
import math
import re
def createDictionary (file):
	dictionary1={}
	dictionary2={}
	actual_w_list=[]
	actual_t_list=[]
	word_list=["start"]
	for line in file:
		wordTag = line.split()
		if len(wordTag)>0:
			actual_w_list.append(wordTag[0])
			actual_t_list.append(wordTag[1])
			word_list.append(wordTag[1])
			wordTag[0]=wordTag[0]
			if wordTag[1] in dictionary1:
				map1 = dictionary1[wordTag[1]]
				if wordTag[0] in map1:
					dictionary1[wordTag[1]][wordTag[0]]=dictionary1[wordTag[1]][wordTag[0]]+1
				else:
					dictionary1[wordTag[1]][wordTag[0]]=1
			else:
				dictionary1[wordTag[1]] = {wordTag[0]:1}
			if wordTag[1] in dictionary2:
				dictionary2[wordTag[1]]=dictionary2[wordTag[1]]+1
			else:
				dictionary2[wordTag[1]]=1
		else:
			word_list.append("end")
			word_list.append("start")
	if(word_list[len(word_list)-1]=='start'):word_list=word_list[:-1]
	return dictionary1,dictionary2,word_list,actual_w_list,actual_t_list

def createEmissionProbabilityMap(word_dict,pos_dict):
	emission = {}
	for key in word_dict.keys():
		wordmap = word_dict[key]
		for word in wordmap.keys():
			if word in emission:
				emission[word][key] = math.log((float)(wordmap[word])/(float)(pos_dict[key]))
			else:
				emission[word]={key:math.log((float)(wordmap[word])/(float)(pos_dict[key]))}
	return emission

def createTransitionMap(tag_list):
	transition = {}
	for i in range(0,len(tag_list)-1):
		if tag_list[i]=='end':
			continue
		if tag_list[i] in transition:
			if tag_list[i+1] in transition[tag_list[i]]:
				transition[tag_list[i]][tag_list[i+1]]+=1
			else:
				transition[tag_list[i]][tag_list[i+1]]=1
		else:
			transition[tag_list[i]] = {tag_list[i+1]:1}
	return transition

def createTransitionProbabilityMap(transition,pos_dict):
	ptransition = deepcopy(transition)
	for state in ptransition.keys():
		for gotostate in ptransition[state].keys():
			ptransition[state][gotostate] = math.log((float)(ptransition[state][gotostate])/(float)(pos_dict[state]))
	return ptransition

def countstate(state,tag_list):
	count=0
	for states in tag_list:
		if states==state:
			count=count+1
	return count

def learnFromTraining(file):
	word_dict,pos_dict,tag_list,actual_w_list,actual_t_list = createDictionary(file)
	pos_dict['start'] = countstate('start',tag_list)
	emission_probabilities = createEmissionProbabilityMap(word_dict,pos_dict)
	transition = createTransitionMap(tag_list)
	transition_probabilities = createTransitionProbabilityMap(transition,pos_dict)
	prefix_prob,suffix_prob = createPrefixSuffixProbMap(createPrefixDict(actual_w_list,actual_t_list),createSuffixDict(actual_w_list,actual_t_list))
	return word_dict,pos_dict,tag_list,emission_probabilities,transition_probabilities,prefix_prob,suffix_prob

def viterbi(sentence,emission_probabilities,transition_probabilities,pos_dict,prefixp,suffixp,unknown):
	viterbi=[]
	parent=[]
	states = transition_probabilities.keys()
	states.append("end")
	sentence.append("end")
	for i in range(0,len(sentence)):
		p=[]
		parent.append(p)
	for i in range(0,len(states)):
		parent[0].append("start")
	for i in range(0,len(states)):
		prob=[]
		tp=-15
		ep=-18
		if sentence[0] in emission_probabilities:
			if states[i] in transition_probabilities['start']:
				tp= transition_probabilities['start'][states[i]]
			if states[i] in emission_probabilities[sentence[0]]:
				ep= emission_probabilities[sentence[0]][states[i]]
		else:
			s=morph_advanced(sentence[0].lower(),prefixp,suffixp)
			if s=='UNK':s=morph(sentence[0].lower())
			if s!='UNK':
				if states[i] in transition_probabilities['start']:
					tp= transition_probabilities['start'][states[i]]
				if states[i]==s:
					ep = math.log((float)(unknown[sentence[0]])/(float)(pos_dict[s]))
			else:
				ep=-18
		prob.append(tp+ep)
		viterbi.append(prob)

	for i in range(1,len(sentence)):
		word = sentence[i]
		for j in range(0,len(states)):
			viterbi[j].append(float('-inf'))
			parent[i].append("temp")
			state = states[j]
			for k in range(0,len(states)):
				if states[k]=="end":continue
				prev_prob = viterbi[k][i-1]
				tp=-15
				if state in transition_probabilities[states[k]]:
					tp= transition_probabilities[states[k]][state]
				ep=-18
				if i == len(sentence)-1:
					ep=0
				elif not word in emission_probabilities:
					s = morph(sentence[i])
					if s=='UNK':s=morph_advanced(sentence[i],prefixp,suffixp)
					if s=='UNK':
						ep=-18
					else:
						if  s==state:
							ep = math.log((float)(unknown[sentence[i]])/(float)(pos_dict[state]))
				elif state in emission_probabilities[word]:
					ep= emission_probabilities[word][state]
				new_prob = prev_prob+tp+ep
				if new_prob >= viterbi[j][i]:
					viterbi[j][i] = new_prob
					parent[i][j]=states[k]
	sentence.remove("end")
	states.remove("end")
	return viterbi,parent
def bestPath(sentence,viterbi,parent,states):
	path=[]
	max_index=0
	max_value=float('-inf')
	sentence.append("end")
	states.append("end")
	for i in range(0,len(states)):
		if max_value<=viterbi[i][len(sentence)-1]:
			max_value = viterbi[i][len(sentence)-1]
			max_index=i
	root = ''
	idx = len(sentence)-1
	while root != 'start':
		root = parent[idx][max_index]
		path.append(root)
		idx=idx-1
		max_index=states.index(root)
	path.reverse()
	sentence.remove("end")
	states.remove("end")
	return path

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

def writeToFile(pos,words):
	file=open("test.pos","a")
	for i in range(0,len(words)):
		if(words[i]==""):
			file.write("\n")
		else:
			file.write(words[i]+"\t"+pos[i]+"\n")
	file.close()

def score (keyFileName, responseFileName):
	keyFile = open(keyFileName, 'r')
	key = keyFile.readlines()
	responseFile = open(responseFileName, 'r')
	response = responseFile.readlines()
	if len(key) != len(response):
    		print "length mismatch between key and submitted file"
		exit()
	correct = 0
	incorrect = 0
	for i in range(len(key)):
		key[i] = key[i].rstrip('\n')
		response[i] = response[i].rstrip('\n')
		if key[i] == "":
			if response[i] == "":
				continue
			else:
    				print "sentence break expected at line " + str(i)
				exit()
    		keyFields = key[i].split('\t')
		if len(keyFields) != 2:
    			print "format error in key at line " + str(i) + ":" + key[i]
			exit()
		keyToken = keyFields[0]
		keyPos = keyFields[1]
    		responseFields = response[i].split('\t')
		if len(responseFields) != 2:
    			print "format error at line " + str(i)
			exit()
		responseToken = responseFields[0]
		responsePos = responseFields[1]
    		if responseToken != keyToken:
    			print "token mismatch at line " + str(i)
			exit()
		if responsePos == keyPos:
			correct = correct + 1
		else:
			incorrect = incorrect + 1
			print(responseToken+" " +keyPos+" "+responsePos)
	print str(correct) + " out of " + str(correct + incorrect) + " tags correct"
	accuracy = 100.0 * correct / (correct + incorrect)
	print "  accuracy: %f" % accuracy

def morph(word):
    if not re.search(r'\w', word):
        return word
    elif re.search(r'[A-Z]', word):
        return 'NNP'
    elif "-" in word:
    	return 'JJ'
    elif re.search(r'\d', word):
        return 'CD'
    elif re.search(r'(ion\b|ty\b|ics\b|ment\b|ence\b|ance\b|ness\b|ist\b|ism\b)',word):
    	if word[len(word)-1]=='s':
    		return 'NNS'
    	else:
        	return 'NN'
    elif re.search(r'(ate\b|fy\b|ize\b|\ben|\bem|\bing)', word):
    	if word[len(word)-2:]=="ed":
    		return 'VBD'
    	if word[len(word)-3:]=="ing":
    		return 'VBG'
    	else:
       		return 'VB'
    elif re.search(r'(\bun|\bin|ble\b|ry\b|ish\b|ious\b|ical\b|\bnon)',word):
        return 'JJ'
    else:
        return 'UNK'

def createPrefixDict(words,tag):
	prefix={}
	prefix_length=6
	for i in range(0,len(words)):
		for j in range(2,prefix_length+1):
			prefix1=""
			if len(words[i])>j-1:
				prefix1=words[i][:j]
			if prefix1 in prefix:
				if tag[i] in prefix[prefix1]:
					prefix[prefix1][tag[i]]=prefix[prefix1][tag[i]]+1
				else:
					prefix[prefix1][tag[i]]=1
			else:
				prefix[prefix1]={tag[i]:1}	
	return prefix

def createSuffixDict(words,tag):
	suffix={}
	suffix_length=20
	for i in range(0,len(words)):
		for j in range(2,suffix_length+1):
			suffix1=""
			if len(words[i])>j-1:
				suffix1=words[i][len(words[i])-j:]
			if suffix1 in suffix:
				if tag[i] in suffix[suffix1]:
					suffix[suffix1][tag[i]]=suffix[suffix1][tag[i]]+1
				else:
					suffix[suffix1][tag[i]]=1
			else:
				suffix[suffix1]={tag[i]:1}
	return suffix
def createPrefixSuffixProbMap(prefix,suffix):
	prefix_num={}
	suffix_num={}
	for key in prefix.keys():
		m = prefix[key]
		sum=0
		for keys in m.keys():
			sum+=m[keys]
		prefix_num[key] = sum
	for key in suffix.keys():
		m = suffix[key]
		sum=0
		for keys in m.keys():
			sum+=m[keys]
		suffix_num[key] = sum
	prefix_prob=deepcopy(prefix)
	suffix_prob=deepcopy(suffix)
	for key in prefix_prob.keys():
		for state in prefix_prob[key]:
			prefix_prob[key][state] = math.log((float)(prefix_prob[key][state])/(float)(prefix_num[key]))
	for key in suffix_prob.keys():
		for state in suffix_prob[key]:
			suffix_prob[key][state] = math.log((float)(suffix_prob[key][state])/(float)(suffix_num[key]))
	return prefix_prob,suffix_prob

def findMax(pmap):
	_max=float('-inf')
	state='UNK'
	for key in pmap.keys():
		if pmap[key] > _max:
			_max = pmap[key]
			state = key
	return _max,state 
def morph_advanced(word,prefix_prob,suffix_prob):
	prefix_length=6
	suffix_length=20
	p=[]
	s=[]
	pstate=[]
	sstate=[]
	for i in range(0,prefix_length+1):
		p.append(float('-inf'))
		pstate.append("UNK")
	for i in range(0,suffix_length+1):
		s.append(float('-inf'))
		sstate.append("UNK")

	for i in range(2,prefix_length+1):
		if(len(word)>i-1):
			if word[:i] in prefix_prob:
				(p[i-2],pstate[i-2]) = findMax(prefix_prob[word[:i]])
			else:
				pstate[i-2]='UNK'
	for i in range(2,suffix_length+1):
		if(len(word)>i-1):
			if word[len(word)-i:] in suffix_prob:
				(s[i-2],sstate[i-2]) = findMax(suffix_prob[word[len(word)-i:]])
			else:
				sstate[i-2]='UNK'
	pmax = max(p)
	smax = max(s)
	if pmax>smax:
		return pstate[p.index(pmax)]
	else:
		return sstate[s.index(smax)]
	return 'UNK'

def count_unknown(file):
	unknown = {}
	for line in file:
		wordTag = line.split()
		if len(wordTag)>0:
			word=wordTag[0]
			if word in unknown:
				unknown[word] = unknown[word]+1
			else:
				unknown[word]=1
	return unknown

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

