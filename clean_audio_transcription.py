import json
import spacy

from utils import clean_token


if __name__ == '__main__':
	nlp = spacy.load('en_core_web_lg')
	input_file = open('/data/audio-transcription.flat.txt')
	output_file = open('/data/audio-transcription.clean.txt', 'w')

	for word in input_file.readlines():
		word = word.replace('’', '\'')
		word = json.loads(word)
		text = word['word']
		for token in nlp(text):
			text = clean_token(token)
			if text is None:
				continue
			tmp_word = {
				'text': text,
				'start': word['startTime'],
				'end': word['endTime']
			}
			tmp_word = json.dumps(tmp_word)
			output_file.write(tmp_word + '\n')

	input_file.close()
	output_file.close()
