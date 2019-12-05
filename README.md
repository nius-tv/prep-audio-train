gcloud compute copy-files plasmic:/home/carloschinchilla/prep-audio/data/segments \
  ./samples \
  --zone us-central1-f

gcloud compute scp --recurse \
  ./prep-audio plasmic:~/prep-audio \
  --zone us-central1-f

docker build \
  -t prep-audio \
  .

docker run \
  -v $(pwd):/app \
  -v /Users/carloschinchilla/triphop/data/audio:/data \
  -it prep-audio \
  bash

TODO:

- Expore using https://github.com/seatgeek/fuzzywuzzy for alignment step.

1. Activate service account

https://cloud.google.com/sdk/docs/downloads-apt-get
gcloud auth activate-service-account --key-file=service-account.json

2. Transcribe PDF to text

To transcribe PDF book files to text navigate to https://www.zamzar.com/.

Follow the instructions on the website, and save the transcription in the "data" directory as "book-transcription.txt".

3. Convert audio book from M4A to WAV

ffmpeg \
    -i      /data/original.m4a \
    -ac     1 \
    -acodec pcm_s16le \
    -ar     16000 \
    /data/original.wav

4. Split WAV into 5 hour chunks (parts)

python3 prepare_audio.py

5. Speech to text first 5 hours

python3 speech_to_text.py

6. Prepare audio transcription

python3 flat_audio_transcriptions.py
python3 clean_audio_transcription.py

7. Prepare book transcription

python3 clean_book_transcription.py

8. Align transcriptions

python3 align_transcriptions.py

9. Create audio segments

python3 segment_audio.py

10. Add silence to audio segments

python3 add_silence.py

11. Normalize audio

python3 normalize_audio.py



tacotron 2

I thought I matched the LJ set but after 90,000 iterations it is gibberish just like it was at 1000 iterations. (The LJ set could speak fairly well at 90,000).

When training other datasets and assuming you have at least say 14 hours:

- make sure the audio matches the transcription – you'd be surprised...
- make sure you trim silences from both the beginning and end.
- make sure the symbols match the transcription
-- if no transitionsn, it will break step

To make sure that the symbols used in the language are the same symbols in the list of symbols. If you're using english, the current symbol list should be fine.

