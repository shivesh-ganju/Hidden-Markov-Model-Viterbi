import math
from morphology import *

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
