import os
def countstate(state,tag_list):
	count=0
	for states in tag_list:
		if states==state:
			count=count+1
	return count

def writeToFile(pos,words):
	file=open("test.pos","a")
	for i in range(0,len(words)):
		if(words[i]==""):
			file.write("\n")
		else:
			file.write(words[i]+"\t"+pos[i]+"\n")
	file.close()

def findMax(pmap):
	_max=float('-inf')
	state='UNK'
	for key in pmap.keys():
		if pmap[key] > _max:
			_max = pmap[key]
			state = key
	return _max,state 

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