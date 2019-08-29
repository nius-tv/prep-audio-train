import glob

from config import duration
from utils import segment_audio


if __name__ == '__main__':
    for input_audio in glob.glob('/data/silence/**'):
        file_name = input_audio.split('/')[-1]
        output_audio = '/data/norm/{}'.format(file_name)
        segment_audio(input_audio, output_audio, 0, duration)
