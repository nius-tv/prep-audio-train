import json


with open('data/audio.transcription.json', 'r') as f:
	data = f.read()
data = json.loads(data)

lines = []
for result in data['response']['results']:
	words = result['alternatives'][0]['words']
	line = json.dumps(words)
	lines.append(line)

lines = '\n'.join(lines)
with open('data/audio.transcription.flat.txt', 'w') as f:
	f.write(lines)
