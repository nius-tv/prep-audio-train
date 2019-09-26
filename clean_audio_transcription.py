import json
import spacy

from config import *
from utils import clean_token


if __name__ == '__main__':
	nlp = spacy.load(SPACY_MODEL)
	input_file = open(TRANSCRIPTION_FLAT_FILE_PATH)
	output_file = open(TRANSCRIPTION_CLEAN_FILE_PATH, 'w')

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
			print(tmp_word)

			output_file.write(tmp_word + '\n')

	input_file.close()
	output_file.close()
