import sys

# コマンドライン引数からファイルパスとpitchデータを取得
file_path = sys.argv[1]
pitch_data = sys.argv[2]

# pitch_dataをスペース区切りの文字列からfloatのリストに変換
frequencies = list(map(float, pitch_data.split()))

# pitchデータを出力
# print("受け取ったfrequenciesデータ:")
# print(frequencies)

# ファイルの内容を読み込んで解析処理
with open(file_path, 'r') as f:
    content = f.read()

# 解析処理（例として固定の精度を計算）
accuracy = 90
print(accuracy)
