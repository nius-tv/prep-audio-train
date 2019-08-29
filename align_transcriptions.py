import json

from Levenshtein import distance


def get_audio_transcription_words():
	with open('/data/audio-transcription.clean.txt') as f:
		lines = f.readlines()

	texts, words = [], []
	for line in lines:
		word = json.loads(line)
		texts.append(word['text'])
		words.append(word)

	return texts, words


def get_book_transcription_words():
	with open('/data/book-transcription.clean.json.txt') as f:
		lines = f.readlines()

	all_words, sents_words = [], []
	for line in lines:
		words = json.loads(line)
		all_words.extend(words)
		sents_words.append(words)

	return all_words, sents_words


def match_window(book_next_sent_words, words, idx):
	'''
	Scans the book's words list using a moving window 
	in search of the words of the next sentence.
	'''
	ini_idx = idx
	while ini_idx < len(words):
		end_idx = ini_idx + len(book_next_sent_words)
		if book_next_sent_words == words[ini_idx:end_idx]:
			return ini_idx
		ini_idx += 1
	return False

	
def next_word_match(book_sent_end_idx, words_a, idx_a, words_b, idx_b):
	'''
	Scans book and audio words for a consecutive two words match.
	'''
	print('> next word match')
	for b in range(max_next_word):
		future_idx_b = idx_b + b

		if future_idx_b > book_sent_end_idx:
			continue

		future_b_1 = words_b[future_idx_b]
		future_b_2 = words_b[future_idx_b + 1]

		print('\nb -current:', idx_b, '-future:', future_idx_b, '-words:', future_b_1, future_b_2)

		for a in range(max_next_word):
			future_idx_a = idx_a + a

			if len(words_a) == future_idx_a + 1:
				return False, None, None

			future_a_1 = words_a[future_idx_a]
			future_a_2 = words_a[future_idx_a + 1]

			print('-- a -current:', idx_a, '-future:', future_idx_a, '-words:', future_a_1, future_a_2)

			if future_a_1 == future_b_1 and future_a_2 == future_b_2:
				print('matched!')
				return True, future_idx_a, future_idx_b

	return False, None, None


def save_audio_chunks(audio_start, audio_end, book_start_idx, book_end_idx):
	data = {
		'audio_start': audio_start,
		'audio_end': audio_end,
		'book_start_idx': book_start_idx,
		'book_end_idx': book_end_idx
	}
	data = json.dumps(data)
	output_file.write(data + '\n')


def skip_sentence(book_next_sent_words, words_a, idx_a, words_b, idx_b):
	print('> skip sentence')
	print('book next sentence:', '\n', ' '.join(book_next_sent_words))

	future_idx_a = match_window(book_next_sent_words, words_a, idx_a)
	future_idx_b = match_window(book_next_sent_words, words_b, idx_b)

	if future_idx_a and future_idx_b:
		print('matched A <> B!')
		return True, future_idx_a, future_idx_b
	elif future_idx_b:
		print('matched B!')
		return True, None, future_idx_b

	return False, None, None


if __name__ == '__main__':
	max_next_word = 10
	output_file = open('/data/audio-sentences.json.txt', 'w')

	audio_words, audio_objs = get_audio_transcription_words()
	assert len(audio_words) == len(audio_objs)
	book_words, book_sents_words = get_book_transcription_words()

	audio_idx, book_idx = 0, 0
	audio_sent_start_idx, book_sent_start_idx = 0, 0
	book_sent_idx, book_sents_matched = 0, 0
	first_sentence_found = False

	while len(book_sents_words) > book_sent_idx + 1:
		audio_w = audio_words[audio_idx]
		book_w = book_words[book_idx]
		edit_dist = distance(audio_w, book_w)

		future_idx_a, future_idx_b = None, None
		book_sent_words = book_sents_words[book_sent_idx]
		book_sent = ' '.join(book_sent_words)
		book_sent_end_idx = book_sent_start_idx + len(book_sent_words)

		print('\n---------------------------------------------------')
		print('first sent found:   ', first_sentence_found)
		print('audio:              ', audio_idx, '/', len(audio_words))
		print('book:               ', book_idx, '/', len(book_words))
		print('audio words:        ', audio_w, '|', audio_words[audio_idx + 1], audio_words[audio_idx + 2])
		print('book words:         ', book_w, '|', book_words[book_idx + 1], book_words[book_idx + 2])
		print('sentences processed:', book_sent_idx, '/', len(book_sents_words))
		print('sentences matched:  ', book_sents_matched)

		next_word_match_result = next_word_match(book_sent_end_idx,
												 audio_words,
												 audio_idx,
												 book_words,
												 book_idx)

		# Exact and almost match
		if first_sentence_found and edit_dist <= 1:
			future_idx_a = audio_idx + 1
			future_idx_b = book_idx + 1

			if edit_dist == 0:
				print('> exact:', audio_w, book_w)
			else:
				print('> distance:', audio_w, book_w)

		# Find two consecutive words
		elif first_sentence_found and next_word_match_result[0]:
			future_idx_a = next_word_match_result[1]
			future_idx_b = next_word_match_result[2]

		# Skip sentence
		else:
			print('> first sent found:', first_sentence_found)
			book_sent_idx += 1
			book_sent_words = book_sents_words[book_sent_idx]
			book_sent = ' '.join(book_sent_words)
	
			skip_sentence_result = skip_sentence(book_sent_words, audio_words, audio_idx, book_words, book_idx)

			if skip_sentence_result[0]:
				tmp_idx_a = skip_sentence_result[1]
				future_idx_b = skip_sentence_result[2]
				book_sent_start_idx = future_idx_b

				if tmp_idx_a is not None:
					first_sentence_found = True
					future_idx_a = tmp_idx_a
					audio_sent_start_idx = future_idx_a

		if future_idx_b:
			print('\nbook  -current:', book_idx,  '-future:', future_idx_b)
			book_idx = future_idx_b
		if future_idx_a:
			print('audio -current:', audio_idx, '-future:', future_idx_a)
			audio_idx = future_idx_a

		tmp_words = book_words[book_sent_start_idx:book_idx]
		tmp_sent = ' '.join(tmp_words)
		print('\n ', book_sent)
		print('>>', tmp_sent)

		if book_sent == tmp_sent:
			print('\n++++++++++++++++++++++++++++++++')
			print('new sentence matched!')
			audio_start = audio_objs[audio_sent_start_idx]['start']
			audio_end = audio_objs[audio_idx]['end']
			print('audio -start:', audio_start , '-end:', audio_end)
			audio_sent = ' '.join(audio_words[audio_sent_start_idx:audio_idx])
			print('audio words:\n', audio_sent)

			save_audio_chunks(audio_start, audio_end, book_sent_start_idx, book_idx)

			audio_sent_start_idx = audio_idx
			book_sent_idx += 1
			book_sents_matched += 1
			book_sent_start_idx = book_idx
			print('next sent audio start:', audio_sent_start_idx)
			print('next sent book start: ', book_sent_start_idx)
			print('++++++++++++++++++++++++++++++++')
