import pickle
import pandas as pd
import numpy as np
import nltk
import json
import sys

arg=sys.argv
name1=arg[1]+'_analisis.json'
name2=arg[1]+'_resultados.json'
with open(arg[1]+'.json', 'r') as fp:
	data = json.load(fp)

with open('objs.pickle', "rb") as f:
        classifier, word_features=pickle.load(f)

def extract_features(document):
        document_words = set(document)
        features = {}
        for word in word_features:
                features['contains(%s)' % word] = (word in document_words)
        return features

load=[]

for i in range(1,len(data['texts'])):
	load.append(data['texts'][str(i)])
	#print(data['texts'][str(i)])

a=pd.DataFrame(load)
a.columns=['text']
aux=[]
p=0
n=0
ne=0
values={}
values.setdefault('text',[])
values.setdefault('sentiment',[])

sentiments={}
sentiments.setdefault('positivos',[])
sentiments.setdefault('negativos',[])
sentiments.setdefault('neutros',[])



for element in a['text']:
	values['text'].append(element)
	aux=element.split()
	prob1=classifier.prob_classify(extract_features(aux))
	dist1=prob1.samples()
	prob_pos=prob1.prob("positive")
	print(prob_pos)
	if prob_pos < 0.25 and prob_pos > 0.2:
		values['sentiment'].append('neutral')
	elif prob_pos < 0.2:
		values['sentiment'].append('malo')
	else:
		values['sentiment'].append('bueno')

for sen in values['sentiment']:
	if sen =='bueno':
		p=p+1
	elif sen == 'malo':
		n=n+1
	else:
		ne=ne+1 

sentiments['positivos'].append(p)
sentiments['negativos'].append(n)
sentiments['neutros'].append(ne)

print(values)

with open(name1, 'w') as fp1:
    json.dump(values, fp1)

with open(name2, 'w') as fp2:
    json.dump(sentiments, fp2)

print(p)
print(n)
print(ne)
