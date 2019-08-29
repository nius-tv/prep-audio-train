import audioread
import math

from utils import segment_audio


if __name__ == '__main__':
    file_path = '/data/original.wav'
    max_seconds = 5 * 60 * 60 # 5 hours

    with audioread.audio_open(file_path) as f:
        duration = f.duration
    print('duration:', duration)

    parts = math.ceil(duration / max_seconds)
    print('parts:', parts)

    for i in range(parts):
        start = i * max_seconds
        end = (i + 1) * max_seconds
        output_audio = '/data/parts/{}-{}.wav'.format(start, end)
        segment_audio(file_path, output_audio, start, end)
