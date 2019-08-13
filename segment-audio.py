import json
import subprocess


def segment_audio(input_audio, output_audio, start, end):
    cmd = 'ffmpeg -y -i {i_file} \
           -ss {start} -to {end} \
           -c copy \
           {o_file}'.format(i_file=input_audio,
                            start=start,
                            end=end,
                            o_file=output_audio)
    print(cmd)
    subprocess.call(['bash', '-c', cmd])


if __name__ == '__main__':
    start_offset = 0.3
    end_offset = 0.8
    duration = 60
    input_audio = 'data/original.wav'

    with open('data/audio-sentences.json.txt') as f:
        sents = f.readlines()

    for sent in sents:
        sent = json.loads(sent)
        output_audio = 'data/segments/{start}-{end}.wav'.format(start=sent['audio_start'],
                                                                end=sent['audio_end'])
        start = float(sent['audio_start']) + start_offset
        end = float(sent['audio_end']) - end_offset
        
        assert end - start < duration
        
        start = '{0:.2f}'.format(start)
        end = '{0:.2f}'.format(end)
        segment_audio(input_audio, output_audio, start, end)
