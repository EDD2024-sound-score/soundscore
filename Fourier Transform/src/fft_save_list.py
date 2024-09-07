# 振幅が初めて1,000,000を超えた時の周波数のみを配列に保存するプログラム(完成形)
from pydub import AudioSegment
import numpy as np
from scipy.fft import fft, fftfreq

# MP3ファイルを読み込む関数
def load_mp3(file_path):
    audio = AudioSegment.from_file(file_path)
    mono_audio = audio.set_channels(1)
    sample_rate = mono_audio.frame_rate
    samples = np.array(mono_audio.get_array_of_samples())
    return samples, sample_rate

# FFTを実行し、0.25秒ごとの周波数成分を出力する関数
def process_fft(input_file_path, segment_duration_sec=0.25):
    samples, sample_rate = load_mp3(input_file_path)
    segment_length = int(segment_duration_sec * sample_rate)
    total_samples = len(samples)
    
    # 結果を保存するリスト
    frequency_results = []
    # 振幅が初めて1,000,000を超えたかどうかを確認するフラグ
    threshold_exceeded = False

    for elapsed_time in np.arange(0, total_samples / sample_rate, segment_duration_sec):
        start_sample = int(elapsed_time * sample_rate)
        end_sample = start_sample + segment_length

        if end_sample > total_samples:
            break

        segment_samples = samples[start_sample:end_sample]
        fft_result = fft(segment_samples)
        frequencies = fftfreq(len(segment_samples), d=1/sample_rate)
        amplitudes = np.abs(fft_result)

        # 最大の振幅を持つ周波数とその振幅を選択
        max_amp_index = np.argmax(amplitudes)
        max_frequency = frequencies[max_amp_index]
        max_amplitude = amplitudes[max_amp_index]

        # 振幅が初めて1,000,000を超えたかどうかをチェック
        if max_amplitude > 1000000 or threshold_exceeded:
            threshold_exceeded = True  # 一度超えたら以降すべて出力
            # print(f"{max_frequency:.2f}")
            frequency_results.append(max_frequency)  # リストに結果を追加

    return frequency_results

# 実行
input_mp3_path = "../data/chorale_correct.mp3"  # 任意の入力ファイル名

# FFT処理を実行して結果を配列に保存
resulting_frequencies = process_fft(input_mp3_path)

# 結果の配列を表示
print(resulting_frequencies)