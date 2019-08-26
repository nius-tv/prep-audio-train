import json


if __name__ == '__main__':
    files = [
        'data/0-5hours.transcription.json',
        'data/5-10hours.transcription.json',
        'data/10-15hours.transcription.json',
        'data/15-20hours.transcription.json',
        'data/20-25hours.transcription.json'
    ]
    output_file = open('data/audio-transcription.flat.txt', 'w')

    for i, file_path in enumerate(files):
        with open(file_path) as f:
            data = f.read()
        data = json.loads(data)

        for result in data['response']['results']:
            for word in result['alternatives'][0]['words']:
                start = word['startTime'][0:-1]
                start = float(start) + (i * 60 * 60 * 5)
                word['startTime'] = start

                end = word['endTime'][0:-1]
                end = float(end) + (i * 60 * 60 * 5)
                word['endTime'] = end

                line = json.dumps(word)
                output_file.write(line + '\n')
