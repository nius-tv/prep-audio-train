import glob
import json


if __name__ == '__main__':
    max_seconds = 5 * 60 * 60 # 5 hours
    files = sorted(glob.glob('/data/transcriptions/*'))
    output_file = open('/data/audio-transcription.flat.txt', 'w')

    for i, file_path in enumerate(files):
        print(file_path)

        with open(file_path) as f:
            data = f.read()
        data = json.loads(data)

        for result in data['response']['results']:
            for word in result['alternatives'][0]['words']:
                start = word['startTime'][0:-1]
                start = float(start) + (i * max_seconds)
                word['startTime'] = start

                end = word['endTime'][0:-1]
                end = float(end) + (i * max_seconds)
                word['endTime'] = end

                line = json.dumps(word)
                output_file.write(line + '\n')
