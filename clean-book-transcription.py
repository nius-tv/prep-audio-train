import json
import spacy

from utils import clean_token


if __name__ == '__main__':
	with open('data/book-transcription.txt', 'r') as f:
		text = f.read()

	nlp = spacy.load('en_core_web_lg')
	nlp.max_length = 2000 * 1000
	doc = nlp(text)
	sents = []

	for sent in doc.sents:
		sent = sent.text
		sent = sent.strip().replace('’', '\'')
		if not sent[0].isalpha():
			continue
		if sent.endswith('.') or sent.endswith('!') or sent.endswith('?'):
			sents.append(sent)
			print(sent)

	print('sentences:', len(sents))

	output_file = open('data/book-transcription.clean.json.txt', 'w')

	for sent in sents:
		sent_words = []
		for token in nlp(sent):
			text = clean_token(token)
			if text is None:
				continue
			sent_words.append(text)
		line = json.dumps(sent_words)
		output_file.write(line + '\n')

	output_file.close()
