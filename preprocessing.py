from copy import deepcopy
import math
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

