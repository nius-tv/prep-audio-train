import glob
import subprocess

from config import *


def add_silence(input_audio, output_audio):
    cmd = 'sox {i_file} {s_file} {o_file}'.format(i_file=input_audio,
    											  s_file=SILENCE_AUDIO_FILE_PATH,
    											  o_file=output_audio)
    print(cmd)
    subprocess.call(['bash', '-c', cmd])


if __name__ == '__main__':
	segments_dir = '{}/*'.format(SEGMENTS_DIR_PATH)

    for input_audio in glob.iglob(segments_dir):
        file_name = input_audio.split('/')[-1]
        output_audio = '{}/{}'.format(SILENCE_DIR_PATH, file_name)
        add_silence(input_audio, output_audio)
