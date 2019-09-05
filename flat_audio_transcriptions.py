import glob
import json

from config import part_duration


if __name__ == '__main__':
    # Sort file names that have the following format: {start}-{end}.wav.
    files = sorted(glob.iglob('/data/transcriptions/*'))
    output_file = open('/data/audio-transcription.flat.txt', 'w')

    for i, file_path in enumerate(files):
        print(file_path)

        with open(file_path) as f:
            data = f.read()
        data = json.loads(data)

        for result in data['results']:
            # The first alternative is the most likely one for this portion.
            for word in result['alternatives'][0]['words']:
                start = word['startTime'][0:-1] # removes "s" from "startTime"
                start = float(start) + (i * part_duration)
                word['startTime'] = start

                end = word['endTime'][0:-1] # removes "s" from "endTime"
                end = float(end) + (i * part_duration)
                word['endTime'] = end

                line = json.dumps(word)
                output_file.write(line + '\n')
