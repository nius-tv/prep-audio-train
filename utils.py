import subprocess


def clean_token(token):
    if token.pos_ in ['PUNCT', 'SPACE'] \
        or not token.is_alpha:
        return None
    if token.pos_ in ['PROPN']:
        text = '--TOKEN--'
    else:
        text = token.lemma_.lower()
    return text


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
