import json
import spacy


if __name__ == "__main__":
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
			if token.pos_ in ['PUNCT', 'SPACE'] \
				or not token.is_alpha:
				continue
			if token.pos_ in ['PROPN']:
				text = '--TOKEN--'
			else:
				text = token.lemma_.lower()
			sent_words.append(text)
		line = json.dumps(sent_words)
		output_file.write(line + '\n')

	output_file.close()
