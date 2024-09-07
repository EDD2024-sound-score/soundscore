#0.25秒ごとにFFTを実行し、周波数成分を出力する
from pydub import AudioSegment
import numpy as np
from scipy.fft import fft, fftfreq
import csv

# MP3ファイルを読み込む関数
def load_mp3(file_path):
    audio = AudioSegment.from_file(file_path)
    mono_audio = audio.set_channels(1)
    sample_rate = mono_audio.frame_rate
    samples = np.array(mono_audio.get_array_of_samples())
    return samples, sample_rate

# FFTを実行し、0.25秒ごとの周波数成分を出力する関数
def process_fft(input_file_path, output_file_name, segment_duration_sec=0.25):
    samples, sample_rate = load_mp3(input_file_path)
    segment_length = int(segment_duration_sec * sample_rate)
    total_samples = len(samples)

    with open(output_file_name, "w", newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(["Elapsed Time (s)", "Frequency (Hz)"])

        for elapsed_time in np.arange(0, total_samples / sample_rate, segment_duration_sec):
            start_sample = int(elapsed_time * sample_rate)
            end_sample = start_sample + segment_length
            
            if end_sample > total_samples:
                break

            segment_samples = samples[start_sample:end_sample]
            fft_result = fft(segment_samples)
            frequencies = fftfreq(len(segment_samples), d=1/sample_rate)
            amplitudes = np.abs(fft_result)

            # 最大の振幅を持つ周波数のみを選択
            max_amp_index = np.argmax(amplitudes)
            max_frequency = frequencies[max_amp_index]

            print(f"Elapsed Time: {elapsed_time:.2f} seconds, Frequency: {max_frequency:.2f} Hz")
            writer.writerow([f"{elapsed_time:.2f}", f"{max_frequency:.2f}"])

# 実行
input_mp3_path = "../data/chorale_correct.mp3"  # 任意の入力ファイル名
output_tsv_path = "test_correct_result3.tsv"  # 任意の出力ファイル名
process_fft(input_mp3_path, output_tsv_path)