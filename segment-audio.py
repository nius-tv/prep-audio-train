import json
import subprocess


if __name__ == '__main__':
    with open('data/audio-sentences.json.txt') as f:
        sents = f.readlines()

    input_audio = 'data/original.wav'

    for sent in sents:
        sent = json.loads(sent)
        start = float(sent['audio_start']) + 0.15
        end = sent['audio_end']
        if start >= end:
            continue
        output_file = 'data/segments/{start}-{end}.wav'.format(start=start, end=end)
        cmd = 'ffmpeg -i {a_file} -ss {start} -to {end} -c copy {o_file}'.format(a_file=input_audio,
                                                                                start=start,
                                                                                end=end,
                                                                                o_file=output_file)
        print(cmd)
        subprocess.check_output(['bash', '-c', cmd])
