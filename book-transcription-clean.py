#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import spacy


with open('data/book-transcription.txt', 'r') as f:
	text = f.read()
lines = text.split('\n')
text = ' '.join(lines)

nlp = spacy.load('en_core_web_lg')
nlp.max_length = 2000 * 1000
doc = nlp(text)
sents = []

for sent in doc.sents:
	sent = sent.text
	sent = sent.strip().lower().replace('’', '\'')
	if not sent[0].isalpha():
		continue
	if sent.endswith('.') or sent.endswith('!') or sent.endswith('?'):
		sents.append(sent)
		print(sent)

print('sentences:', len(sents))

lines = []
for sent in sents:
	sent_words = []
	for token in nlp(sent):
		if token.pos_ in ['PUNCT', 'SPACE']:
			continue
		word = token.text
		sent_words.append(word)
	line = json.dumps(sent_words)
	lines.append(line)

lines = '\n'.join(lines)
with open('data/book-transcription.clean.json.txt', 'w') as f:
	f.write(lines)
