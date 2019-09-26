import json
import os

from config import *
from utils import segment_audio


if __name__ == '__main__':
    # Speech-to-text audio timestamps are not perfect.
    # Here we define offsets (heuristics) to compensate for the loss of precision.
    start_offset = 0.3
    end_offset = -0.8

    with open(AUDIO_SENTENCES_FILE_PATH) as f:
        sents = f.readlines()

    for sent in sents:
        sent = json.loads(sent)
        output_audio = '{dir}/{start}-{end}.{fmt}'.format(dir=SEGMENTS_DIR_PATH,
                                                          start=sent['audio_start'],
                                                          end=sent['audio_end'],
                                                          fmt=AUDIO_FMT)

        if os.path.exists(output_audio):
            continue

        start = float(sent['audio_start']) + start_offset
        end = float(sent['audio_end']) + end_offset

        assert end - start < SEGMENT_DURATION

        segment_audio(ORIGIN_AUDIO_FILE_PATH, output_audio, start, end)
