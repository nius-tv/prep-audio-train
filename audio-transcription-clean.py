import json
import spacy


with open('data/audio-transcription.flat.txt') as f:
	data = f.read()
data = data.lower().replace('’', '\'')

nlp = spacy.load('en_core_web_lg')
words = []
for line in data.split('\n'):
	if line.strip() == '':
		continue
	for word in json.loads(line):
		text = word['word']
		for token in nlp(text):
			if token.pos_ in ['PUNCT', 'SPACE']:
				continue
			words.append(token.text)

print(len(words))
words = ' '.join(words)
with open('data/audio-transcription.clean.txt', 'w') as f:
	f.write(words)
