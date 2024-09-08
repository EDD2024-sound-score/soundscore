# 周波数のみを配列に保存し、Railsからの入力に対応したプログラム(完成形)
from pydub import AudioSegment
import numpy as np
from scipy.fft import fft, fftfreq
import sys

# テスト用
#file_path = "../data/chorale_correct.mp3"  # 任意の入力ファイル名
#frequencies = [1392.0, 1056.0, 186.0]


# コマンドライン引数からファイルパスとpitchデータを取得
file_path = sys.argv[1]
pitch_data = sys.argv[2]

# pitch_dataをスペース区切りの文字列からfloatのリストに変換
frequencies = list(map(float, pitch_data.split()))


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



# FFT処理を実行して結果を配列に保存
testdata = process_fft(file_path)

# 結果の配列を表示
#print(testdata)

# ここからはスコアの算出のプログラム
def align_arrays(array1, array2):
    # 配列の長さを取得
    len1 = len(array1)
    len2 = len(array2)

    # 短い配列の長さを取得
    min_length = min(len1, len2)

    # 長い配列を短い配列の長さに合わせてスライス
    aligned_array1 = array1[:min_length]
    aligned_array2 = array2[:min_length]

    return aligned_array1, aligned_array2


# aligned_testdataには１つ目の戻り値, aligned_frequencies
aligned_testdata, aligned_frequencies = align_arrays(testdata, frequencies)

#print("Aligned Test Data:", aligned_testdata)
#print("Aligned Frequencies:", aligned_frequencies)

#　ここから正解はaligned_frequencies、テストデータはaligned_testdataとして扱う
# スコアを算出するプログラム
def calculate_score(aligned_testdata, aligned_frequencies):
    match = 0
    total = len(aligned_frequencies)  # 配列の長さを取得

    # 配列を0から最後まで回して、正解データの-10%から+10%の範囲にテストデータの値があるかをチェック
    for test_val, correct_val in zip(aligned_testdata, aligned_frequencies):
        lower_bound = correct_val * 0.9  # 正解データの-10%
        upper_bound = correct_val * 1.1  # 正解データの+10%

        if lower_bound <= test_val <= upper_bound:
            match += 1  # 一致する場合、matchを増加

    # スコアを計算
    score = match / total
    return score

# スコアを計算
score = calculate_score(aligned_testdata, aligned_frequencies)

# 結果のスコアを表示
print(score)
