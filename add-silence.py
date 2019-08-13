import glob
import subprocess


def add_silence(input_audio, output_audio):
    cmd = 'sox {i_file} data/silence.wav {o_file}'.format(i_file=input_audio,
                                                          o_file=output_audio)
    print(cmd)
    subprocess.call(['bash', '-c', cmd])


if __name__ == '__main__':
    for input_audio in glob.glob('data/segments/**'):
        file_name = input_audio.split('/')[-1]
        output_audio = 'data/tmp/{}'.format(file_name)
        add_silence(input_audio, output_audio)
