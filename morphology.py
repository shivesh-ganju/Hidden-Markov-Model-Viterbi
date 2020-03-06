import re
from utilities import *
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

def morph_advanced(word,prefix_prob,suffix_prob):
    prefix_length=7
    suffix_length=15
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
