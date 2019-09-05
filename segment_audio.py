import json
import os

from config import original_audio, segment_duration
from utils import segment_audio


if __name__ == '__main__':
    # Speech-to-text audio timestamps are not perfect.
    # Here we define offsets (heuristics) to compensate for the loss of precision.
    start_offset = 0.3
    end_offset = -0.8

    with open('/data/audio-sentences.json.txt') as f:
        sents = f.readlines()

    for sent in sents:
        sent = json.loads(sent)
        output_audio = '/data/segments/{start}-{end}.wav'.format(start=sent['audio_start'],
                                                                 end=sent['audio_end'])

        if os.path.exists(output_audio):
            continue

        start = float(sent['audio_start']) + start_offset
        end = float(sent['audio_end']) + end_offset

        assert end - start < segment_duration

        segment_audio(original_audio, output_audio, start, end)
