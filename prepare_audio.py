import audioread
import math

from config import *
from utils import segment_audio


if __name__ == '__main__':
    with audioread.audio_open(ORIGIN_AUDIO_FILE_PATH) as f:
        duration = f.duration
    print('duration:', duration)

    parts = math.ceil(duration / PART_DURATION)
    print('parts:', parts)

    for i in range(parts):
        start = i * PART_DURATION
        end = (i + 1) * PART_DURATION
        output_audio = '{}/{}-{}.{}'.format(PARTS_DIR_PATH, start, end, AUDIO_FMT)
        segment_audio(ORIGIN_AUDIO_FILE_PATH, output_audio, start, end)
