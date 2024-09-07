from pydub import AudioSegment
import numpy as np
from scipy.fft import fft, fftfreq
import csv

# MP3ファイルを読み込む関数
def load_mp3(file_path):
    # pydubでMP3ファイルを読み込む
    audio = AudioSegment.from_file(file_path)
    # チャンネルをモノラルに変換し、サンプリングレートを取得
    mono_audio = audio.set_channels(1)
    sample_rate = mono_audio.frame_rate
    # 音声データをnumpy配列に変換
    samples = np.array(mono_audio.get_array_of_samples())
    return samples, sample_rate

# FFTを実行し、0.25秒ごとの周波数成分を出力する関数
def process_fft(file_path, output_file_name="frequency_output.tsv", segment_duration_sec=0.25):
    samples, sample_rate = load_mp3(file_path)
    segment_length = int(segment_duration_sec * sample_rate)
    total_segments = len(samples) // segment_length

    # 結果を保存するTSVファイルを作成
    with open(output_file_name, "w", newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(["Segment", "Elapsed Time (s)", "Frequency (Hz)", "Amplitude"])

        for i in range(total_segments):
            # セグメントのサンプルを抽出
            segment_samples = samples[i * segment_length : (i + 1) * segment_length]
            # FFTを実行
            fft_result = fft(segment_samples)
            # 周波数成分を計算
            frequencies = fftfreq(len(segment_samples), d=1/sample_rate)
            # 振幅の絶対値を計算
            amplitudes = np.abs(fft_result)

            # 経過時間を計算
            elapsed_time = i * segment_duration_sec

            # 結果を出力
            print(f"Segment {i + 1}: Elapsed Time: {elapsed_time:.2f} seconds")
            for freq, amp in zip(frequencies, amplitudes):
                if freq >= 0:  # 正の周波数のみを表示
                    print(f"Frequency: {freq:.2f} Hz, Amplitude: {amp:.2f}")
                    # ファイルに書き込み
                    writer.writerow([i + 1, f"{elapsed_time:.2f}", f"{freq:.2f}", f"{amp:.2f}"])

# MP3ファイルのパスと出力ファイル名を指定して実行
mp3_file_path = "../data/chorale_correct.mp3"
output_file_name = "test_correct_result2.tsv"  # 任意の出力ファイル名を指定
process_fft(mp3_file_path, output_file_name)