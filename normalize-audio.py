import glob
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
    duration = 60

    for input_audio in glob.glob('data/tmp/**'):
        file_name = input_audio.split('/')[-1]
        output_audio = 'data/norm/{}'.format(file_name)
        segment_audio(input_audio, output_audio, 0, duration)
