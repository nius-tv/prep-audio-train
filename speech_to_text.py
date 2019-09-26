import glob

from config import *
from google.cloud import speech
from google.cloud.speech import types
from google.protobuf.json_format import MessageToJson


def speech_to_text(file_name, output_transcription):
    gcs_uri = 'gs://{}/{}/audio/parts/{}'.format(GCS_BUCKET, PROJECT_NAME, file_name)
    print('processing audio:', gcs_uri)

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        enable_word_time_offsets=True,
        language_code=SPEECH_TO_TEXT_LANG,
        sample_rate_hertz=SAMPLE_RATE,
        # Enhanced models are only available to projects that
        # opt in for audio data collection.
        # For more information see https://cloud.google.com/speech-to-text/docs/enhanced-models.
        use_enhanced=True)

    # Converts speech to text
    print('Waiting for operation to complete...')
    operation = client.long_running_recognize(config, audio)
    response = operation.result()
    # "response" is a plain protobuf object, which can be serialized to string using.
    # Note that "MessageToJson" actually returns a JSON object serialized as a string.
    # For more information on this workaround visit,
    # https://github.com/googleapis/google-cloud-python/issues/3485#issuecomment-307797562.
    response = MessageToJson(response)

    # Save transcription
    with open(output_transcription, 'w') as f:
        f.write(response)


if __name__ == '__main__':
    client = speech.SpeechClient()
    parts_dir = '{}/*'.format(PARTS_DIR_PATH)

    for input_audio in glob.iglob(parts_dir):
        file_name = input_audio.split('/')[-1]
        output_transcription = '{}/{}.json'.format(TRANSCRIPTIONS_DIR_PATH, file_name)
        speech_to_text(file_name, output_transcription)
