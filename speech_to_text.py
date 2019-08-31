import glob

from config import gcs_bucket, sample_rate, voice_name
from google.cloud import speech
from google.cloud.speech import types
from google.protobuf.json_format import MessageToJson


def speech_to_text(input_audio, output_transcription):
    gcs_uri = 'gs://{}/{}{}'.format(gcs_bucket, voice_name, input_audio)
    print('processing audio:', gcs_uri)

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        enable_word_time_offsets=True,
        language_code='en-US',
        sample_rate_hertz=sample_rate,
        # Enhanced models are only available to projects that
        # opt in for audio data collection.
        # https://cloud.google.com/speech-to-text/docs/enhanced-models
        use_enhanced=True)

    # Converts speech to text
    print('Waiting for operation to complete...')
    operation = client.long_running_recognize(config, audio)
    response = operation.result()
    # https://github.com/googleapis/google-cloud-python/issues/3485#issuecomment-307797562
    response = MessageToJson(response)

    # Save transcription
    with open(output_transcription, 'w') as f:
        f.write(response)


if __name__ == '__main__':
    client = speech.SpeechClient()

    for input_audio in glob.iglob('/data/parts/*'):
        file_name = input_audio.split('/')[-1]
        output_transcription = '/data/transcriptions/{}.json'.format(file_name)
        speech_to_text(input_audio, output_transcription)
