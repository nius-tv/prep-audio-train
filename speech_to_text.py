import glob

from config import sample_rate
from google.cloud import speech
from google.cloud.speech import types


def speech_to_text(input_audio, output_transcription):
    with open(input_audio, 'rb') as f:
        content = f.read()
    audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        enable_word_time_offsets=True,
        language_code='en-US',
        sample_rate_hertz=sample_rate,
        # Enhanced models are only available to projects that
        # opt in for audio data collection.
        # https://cloud.google.com/speech-to-text/docs/enhanced-models
        use_enhanced=True)

    # Converts speech to text
    response = client.recognize(config, audio)


if __name__ == '__main__':
    client = speech.SpeechClient()

    for input_audio in glob.iglob('/data/parts/*'):
        file_name = input_audio.split('/')[-1]
        output_transcription = '/data/transcriptions/{}.json'.format(file_name)
        speech_to_text(input_audio, output_transcription)
