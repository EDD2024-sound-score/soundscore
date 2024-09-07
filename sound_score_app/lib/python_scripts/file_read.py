import sys

# コマンドライン引数からファイルパスを取得
file_path = sys.argv[1]

try:
    # ファイルの内容を読み込んで出力
    with open(file_path, 'r') as f:
        content = f.read()
        print("ファイルの内容:")
        print(content)
except FileNotFoundError:
    print(f"エラー: ファイル '{file_path}' が見つかりません。")
except Exception as e:
    print(f"エラー: {e}")
