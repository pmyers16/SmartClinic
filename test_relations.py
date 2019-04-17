# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:04:24 2019

@author: Patrick
"""


import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp(u'Bob brought the pizza to Alice')
for sent in doc.sents:
     for i, word in enumerate(sent):
         if word.head is word:
             head_idx = 0
         else:
            head_idx = doc[i].head.i+1
        
         print("%d\t%s\t%s\t%s\t%s\t%s\t%d\t%s\t%s\t%s"%(
             i+1, # There's a word.i attr that's position in *doc*
             word,
             '_',
             word.pos_, # Coarse-grained tag
             word.tag_, # Fine-grained tag
             '_',
             head_idx,
             word.dep_, # Relation
             '_', '_'))