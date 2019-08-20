'''
Part of this script has been inspired by Kyubyong's excelent work.
https://github.com/Kyubyong/expressive_tacotron/blob/master/utils.py
'''
import glob
import librosa
import numpy as np


def get_spectrogram(file_path):
    # Load audio file
    y, sr = librosa.load(file_path, sr=sample_rate)

    # stft
    linear = librosa.stft(y=y,
                          n_fft=n_fft,
                          hop_length=hop_length,
                          win_length=win_length)

    # Magnitude spectrogram
    mag = np.abs(linear) # (1+n_fft//2, T)

    # Mel spectrogram
    mel_basis = librosa.filters.mel(sr, n_fft, n_mels) # (n_mels, 1+n_fft//2)
    mel = np.dot(mel_basis, mag) # (n_mels, t)

    # Convert to decibel
    mel = 20 * np.log10(np.maximum(1e-5, mel))
    mag = 20 * np.log10(np.maximum(1e-5, mag))

    # Normalize
    mel = np.clip((mel - ref_db + max_db) / max_db, 1e-8, 1)
    mag = np.clip((mag - ref_db + max_db) / max_db, 1e-8, 1)

    # Transpose
    mel = mel.T.astype(np.float32) # (T, n_mels)
    mag = mag.T.astype(np.float32) # (T, 1+n_fft//2)

    return mel, mag


if __name__ == '__main__':
    sample_rate = 16000 # audio sample rate
    n_fft = 2048 # fft points (samples)
    frame_shift = 0.0125 # in seconds
    frame_length = 0.05 # in seconds
    hop_length = int(sample_rate * frame_shift) # of samples
    win_length = int(sample_rate * frame_length) # of samples
    n_mels = 80 # number of Mel banks to generate
    max_db = 100
    ref_db = 20

    expected_shape = None
    for input_audio in glob.glob('data/norm/**'):
        print(input_audio)
        mel, _ = get_spectrogram(input_audio)

        if expected_shape is None:
            expected_shape = mel.shape
        print(expected_shape, mel.shape)
        assert expected_shape == mel.shape

        audio_name = input_audio.split('/')[-1]
        output_audio = 'data/features/{}'.format(audio_name)
        np.save(output_audio, mel)
