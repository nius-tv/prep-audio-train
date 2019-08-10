import json
import phonetics

from Levenshtein import distance


def get_audio_transcription_words():
	with open('data/audio.transcription.clean.txt') as f:
		data = f.read()
	return data.split(' ')


def get_book_transcription_words():
	with open('data/book-transcription.clean.json.txt') as f:
		data = f.read()

	all_words, sents_words = [], []
	for line in data.split('\n'):
		words = json.loads(line)
		all_words.extend(words)
		sents_words.append(words)

	return all_words, sents_words


def next_sentence_match(book_next_sent_words, words_a, idx_a, words_b, idx_b):
	print('next sentence match')
	for a in range(10):
		future_idx_a = idx_a + a + 1
		future_a_1 = words_a[future_idx_a]
		future_a_2 = words_a[future_idx_a + 1]

		print('a -current index:', idx_a, '-future index:', future_idx_a, '-words:', future_a_1, future_a_2)
		print('next sentence words:', book_next_sent_words[0], book_next_sent_words[1])

		if future_a_1 != book_next_sent_words[0] or future_a_2 != book_next_sent_words[1]:
			continue

		print('matched!')
		print('searching in "b"...')

		for b in range(10):
			future_idx_b = idx_b + b + 1
			future_b_1 = words_b[future_idx_b]
			future_b_2 = words_b[future_idx_b + 1]

			print('b -current index:', idx_b, '-future index:', future_idx_b, '-words:', future_b_1, future_b_2)

			if future_a_1 == future_b_1 and future_a_2 == future_b_2:
				print('a<>b - next sentence matched!')
				return True, future_idx_a, future_idx_b
			# elif phonetics_match(future_a, future_b):
			# 	print('[PHONETIC MATCH 1]')
			# 	return True, future_idx_a, future_idx_b

	return False, None, None


def next_word_match(book_sent_end_idx, words_a, idx_a, words_b, idx_b):
	print('next word match')
	for a in range(10):
		future_idx_a = idx_a + a + 1
		future_a_1 = words_a[future_idx_a]
		future_a_2 = words_a[future_idx_a + 1]

		print('a -current index:', idx_a, '-future index:', future_idx_a, '-words:', future_a_1, future_a_2)
		
		for b in range(10):
			future_idx_b = idx_b + b + 1
			future_b_1 = words_b[future_idx_b]
			future_b_2 = words_b[future_idx_b + 1]

			if future_idx_b > book_sent_end_idx:
				print('out of bounds!')
				return False, None, None

			print('b -current index:', idx_b, '-future index:', future_idx_b, '-words:', future_b_1, future_b_2)

			if future_a_1 == future_b_1 and future_a_2 == future_b_2:
				print('a<>b - next word matched!')
				return True, future_idx_a, future_idx_b

	return False, None, None


def match_window(book_next_sent_words, words, idx):
	ini_idx = idx
	while ini_idx < len(words):
		end_idx = ini_idx + len(book_next_sent_words)
		if book_next_sent_words == words[ini_idx:end_idx]:
			return ini_idx
		ini_idx += 1
	return False


def skip_sentence(book_next_sent_words, words_a, idx_a, words_b, idx_b):
	print('skip sentence')
	print('book next sentence:', ' '.join(book_next_sent_words))

	future_idx_a = match_window(book_next_sent_words, words_a, idx_a)
	future_idx_b = match_window(book_next_sent_words, words_b, idx_b)

	if future_idx_a and future_idx_b:
		print('a<>b - matched!')
		return True, future_idx_a, future_idx_b
	elif future_idx_b:
		return True, None, future_idx_b
	else:
		raise Exception


audio_words = get_audio_transcription_words()
book_words, book_sents_words = get_book_transcription_words()

audio_idx, book_idx = 0, 0
book_sent_idx, book_sent_start_idx = 0, 0
book_sent_matched = 0

while True:
	audio_w = audio_words[audio_idx]
	book_w = book_words[book_idx]
	edit_dist = distance(audio_w, book_w)

	future_idx_a, future_idx_b = None, None
	book_sent_words = book_sents_words[book_sent_idx]
	book_next_sent_words = book_sents_words[book_sent_idx + 1]
	book_sent = ' '.join(book_sent_words)
	book_sent_end_idx = book_sent_start_idx + len(book_sent_words)

	print('\n')
	print('+', book_sent)
	print('audio index:      ', audio_idx, '/', len(audio_words))
	print('sentences matched:', book_sent_matched, '/', len(book_sents_words))
	print('sentence number:  ', book_sent_idx, '-sentence start index:', book_sent_start_idx)
	print('sentence start:   ', book_idx, '-end:', book_sent_end_idx)
	print('audio:', audio_w, '>>', audio_words[audio_idx + 1], audio_words[audio_idx + 2])
	print('book: ', book_w, '>>', book_words[book_idx + 1], book_words[book_idx + 2])

	next_word_match_result = next_word_match(book_sent_end_idx,
											 audio_words,
											 audio_idx,
											 book_words,
											 book_idx)
	next_sentence_match_result = next_sentence_match(book_next_sent_words,
													 audio_words,
													 audio_idx,
													 book_words,
													 book_idx)

	if edit_dist <= 1:
		future_idx_a = audio_idx + 1
		future_idx_b = book_idx + 1

		if edit_dist == 0:
			print('<same>', audio_w, book_w)
		else:
			print('<edit>', audio_w, book_w)

	elif next_word_match_result[0]:
		print('<next word match>')
		future_idx_a = next_word_match_result[1]
		future_idx_b = next_word_match_result[2]

	elif next_sentence_match_result[0]:
		print('<next sentence match>')
		future_idx_a = next_sentence_match_result[1]
		future_idx_b = next_sentence_match_result[2]

	else:
		print('<skip sentence>')
		book_sent_idx += 1
		book_sent_words = book_sents_words[book_sent_idx]
		book_sent = ' '.join(book_sent_words)
		skip_sentence_result = skip_sentence(book_sent_words, audio_words, audio_idx, book_words, book_idx)
		audio_idx += 1

		if skip_sentence_result[0]:
			tmp_idx_a = skip_sentence_result[1]
			future_idx_b = skip_sentence_result[2]
			book_sent_start_idx = future_idx_b

			if tmp_idx_a is not None:
				future_idx_a = tmp_idx_a

	if future_idx_a and future_idx_b:
		print('-------------------------------------------------------')
		print('audio -current:', audio_idx, '-future:', future_idx_a)
		print('book  -current:', book_idx,  '-future:', future_idx_b)
		print('-------------------------------------------------------')
		audio_idx = future_idx_a
		book_idx = future_idx_b

	tmp_words = book_words[book_sent_start_idx:book_idx]
	tmp_sent = ' '.join(tmp_words)
	print('=', book_sent)
	print('=', tmp_sent)

	if book_sent == tmp_sent:
		print('new sentence found!')
		book_sent_idx += 1
		book_sent_matched += 1
		book_sent_start_idx = book_idx
		print('new sentence start index:', book_sent_start_idx)
