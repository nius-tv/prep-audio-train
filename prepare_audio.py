import audioread
import math

from config import original_audio, part_duration
from utils import segment_audio


if __name__ == '__main__':
    with audioread.audio_open(original_audio) as f:
        duration = f.duration
    print('duration:', duration)

    parts = math.ceil(duration / part_duration)
    print('parts:', parts)

    for i in range(parts):
        start = i * part_duration
        end = (i + 1) * part_duration
        output_audio = '/data/parts/{}-{}.wav'.format(start, end)
        segment_audio(original_audio, output_audio, start, end)
