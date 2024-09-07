# 計算できているが、出力が0.25秒ごとになっていない 
from pydub import AudioSegment
import numpy as np
from scipy.fft import fft, fftfreq

# MP3ファイルを読み込む
def load_mp3(file_path):
    # pydubでMP3ファイルを読み込む
    audio = AudioSegment.from_file(file_path)
    # チャンネルをモノラルに変換し、サンプリングレートを取得
    mono_audio = audio.set_channels(1)
    sample_rate = mono_audio.frame_rate
    # 音声データをnumpy配列に変換
    samples = np.array(mono_audio.get_array_of_samples())
    return samples, sample_rate

# FFTを実行し、0.25秒ごとの周波数成分を出力し、結果をTSVファイルに保存する
def process_fft(file_path, output_file, segment_duration_sec=0.25):
    samples, sample_rate = load_mp3(file_path)
    segment_length = int(segment_duration_sec * sample_rate)
    total_segments = len(samples) // segment_length

    # TSVファイルを開く
    with open(output_file, 'w') as f:
        # TSVファイルのヘッダーを作成
        f.write("Segment\tElapsed Time (s)\tFrequency (Hz)\tAmplitude\n")

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

            # 結果をターミナルに出力し、TSVファイルに書き込む
            print(f"Segment {i + 1} (Elapsed Time: {elapsed_time:.2f} s):")
            for freq, amp in zip(frequencies, amplitudes):
                if freq >= 0:  # 正の周波数のみを表示
                    output_line = f"{i + 1}\t{elapsed_time:.2f}\t{freq:.2f}\t{amp:.2f}\n"
                    print(f"Frequency: {freq:.2f} Hz, Amplitude: {amp:.2f}")
                    f.write(output_line)

# MP3ファイルのパスと出力ファイルのパスを指定して実行
mp3_file_path = "../data/chorale_correct.mp3"
output_file_path = "test_correct_result.tsv"
process_fft(mp3_file_path, output_file_path)