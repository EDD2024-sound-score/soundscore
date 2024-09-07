require 'open3'
class SongSelectionController < ApplicationController

  before_action :authenticate_user!
  def index
    @songs = Song.all # 全楽曲を表示
  end

  def upload
    @song = Song.find(params[:id]) # 選択された楽曲情報を取得
  end

  def upload_song
    @song = Song.find(params[:id]) # 選択された楽曲

    # 演奏ファイルのアップロード処理
    uploaded_file = params[:performance_file]
    temp_file_path = Rails.root.join('public', 'uploads', uploaded_file.original_filename)
    
    # ファイルを一時ディレクトリに保存
    File.open(temp_file_path, 'wb') do |file|
      file.write(uploaded_file.read)
    end

    # Pythonスクリプトを実行してファイルを解析
    stdout, stderr, status = Open3.capture3("python3 #{Rails.root.join('lib', 'python_scripts', 'file_read.py')} #{temp_file_path}")

    if status.success?
      @accuracy = stdout.strip # Pythonスクリプトからの出力を使用
    else
      @error = stderr # エラーメッセージを取得
      Rails.logger.error("Pythonスクリプトエラー: #{@error}")
      flash[:alert] = "解析に失敗しました: #{@error}"
      render :upload # 元のページに戻る
    end

    # 結果ページへリダイレクト
    redirect_to song_selection_result_path(accuracy: @accuracy)
  end

  def result
    @accuracy = params[:accuracy] # 結果表示用
  end

  private

  def calculate_accuracy(song, uploaded_file)
    # 精度を計算する処理をここに記述（例: ダミーでランダム値を返す）
    rand(70..100)
  end
end
