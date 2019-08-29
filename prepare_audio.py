import audioread
import math

from config import max_seconds, original_audio
from utils import segment_audio


if __name__ == '__main__':
    with audioread.audio_open(original_audio) as f:
        duration = f.duration
    print('duration:', duration)

    parts = math.ceil(duration / max_seconds)
    print('parts:', parts)

    for i in range(parts):
        start = i * max_seconds
        end = (i + 1) * max_seconds
        output_audio = '/data/parts/{}-{}.wav'.format(start, end)
        segment_audio(original_audio, output_audio, start, end)
