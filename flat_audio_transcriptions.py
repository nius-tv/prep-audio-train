import glob
import json

from config import *


if __name__ == '__main__':
    transcriptions_dir = '{}/*'.format(TRANSCRIPTIONS_DIR_PATH)
    # Sort file names that have the following format: {start}-{end}.wav.
    files = sorted(glob.iglob(transcriptions_dir))
    output_file = open(TRANSCRIPTION_FLAT_FILE_PATH, 'w')

    for i, file_path in enumerate(files):
        print(file_path)

        with open(file_path) as f:
            data = f.read()
        data = json.loads(data)

        for result in data['results']:
            # The first alternative is the most likely one for this portion.
            for word in result['alternatives'][0]['words']:
                start = word['startTime'][0:-1] # removes "s" from "startTime"
                start = float(start) + (i * PART_DURATION)
                word['startTime'] = start

                end = word['endTime'][0:-1] # removes "s" from "endTime"
                end = float(end) + (i * PART_DURATION)
                word['endTime'] = end

                line = json.dumps(word)
                output_file.write(line + '\n')
