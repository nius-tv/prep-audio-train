import glob

from config import *
from utils import segment_audio


if __name__ == '__main__':
	silence_dir = '{}/*'.format(SILENCE_DIR_PATH)

    for input_audio in glob.iglob(silence_dir):
        file_name = input_audio.split('/')[-1]
        output_audio = '{}/{}'.format(NORMALIZED_DIR_PATH, file_name)
        segment_audio(input_audio, output_audio, 0, SEGMENT_DURATION)
