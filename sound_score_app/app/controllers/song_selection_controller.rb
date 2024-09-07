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
    File.open(Rails.root.join('public', 'uploads', uploaded_file.original_filename), 'wb') do |file|
      file.write(uploaded_file.read)
    end

    # 精度計算処理の例（ここで実際の処理を実装）
    @accuracy = calculate_accuracy(@song, uploaded_file)

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
