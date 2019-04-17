#!/usr/bin/env python
# coding: utf8
"""A simple example of extracting relations between phrases and entities using
spaCy's named entity recognizer and the dependency parse. Here, we extract
money and currency values (entities labelled as MONEY) and then check the
dependency tree to find the noun phrase they are referring to – for example:
$9.4 million --> Net income.

Compatible with: spaCy v2.0.0+
Last tested with: v2.1.0
"""
from __future__ import unicode_literals, print_function

import plac
import spacy


TEXTS = [
    "Open the scan on March 10.",
    "The image on January 16 showed a hairline fracture",
]


@plac.annotations(
    model=("Model to load (needs parser and NER)", "positional", None, str)
)
def main(model="en_core_web_sm"):
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
    print("Processing %d texts" % len(TEXTS))

    for text in TEXTS:
        doc = nlp(text)
        relations = extract_currency_relations(doc)
        for r1, r2 in relations:
            print("{:<10}\t{}\t{}".format(r1.text, r2.ent_type_, r2.text))


def extract_currency_relations(doc):
    images = ['image', 'scan', 'CT-scan']
    for token in doc:
        if token.head == token:
            head_idx = 0
        else:
            head_idx = token.i-doc[0].i+1
        #print(token.text, token.pos_, head_idx, token.dep_)
    #for np in doc.noun_chunks:
    #    if np.root.dep_ == "dobj":
    #        print(np.root.text)
    #        print(np.text)
    # merge entities and noun chunks into one token
    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()

    relations = []
    for date in filter(lambda w: w.ent_type_ == "DATE", doc):
        print(date)
        #if date.dep_ in ("attr", "dobj"):
        #    subject = [w for w in date.head.lefts if w.dep_ == "nsubj"]
        #    if subject:
        #        subject = subject[0]
        #        relations.append((subject, date))
        #elif date.dep_ == "pobj" and date.head.dep_ == "prep":
        #    relations.append((date.head.head, date))
        subject = [w for w in doc if w.dep_ == "nsubj"]
        if subject:
            subject = subject[0]
            relations.append((subject,date))
        subject = [w for w in doc.noun_chunks if w.root.text in images]
        if subject:
            subject = subject[0]
            relations.append((subject,date))
    return relations


if __name__ == "__main__":
    plac.call(main)