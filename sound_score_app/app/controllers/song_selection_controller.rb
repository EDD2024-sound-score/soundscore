class SongSelectionController < ApplicationController
  def index
    # 楽曲選択画面の表示
    @songs = Song.all  # Songモデルから全曲を取得（例）
  end

  def upload
    # 自分の楽曲をアップロードする画面の表示
  end

  def upload_song
    # 楽曲アップロードの処理
    uploaded_file = params[:song_file]

    # ファイルを保存する処理（ローカルに保存する場合）
    File.open(Rails.root.join('public', 'uploads', uploaded_file.original_filename), 'wb') do |file|
      file.write(uploaded_file.read)
    end

    # アップロード成功後に結果画面にリダイレクト
    redirect_to song_selection_result_path
  end

  def result
    # アップロードした自分の曲の精度結果を表示
    @accuracy = calculate_accuracy(params[:uploaded_song_id]) # 精度計算の例
  end

  private

  def calculate_accuracy(song_id)
    # 楽曲の精度を計算するためのダミー処理（実装例）
    rand(70..100)  # 実際には分析処理をここに実装
  end
end
