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
  
    # アップロード先ディレクトリが存在しない場合は作成
    FileUtils.mkdir_p(Rails.root.join('public', 'uploads'))
  
    # ファイルを一時ディレクトリに保存
    File.open(temp_file_path, 'wb') do |file|
      file.write(uploaded_file.read)
    end
  
    # pitchのfrequenciesデータをfloatに変換してスペース区切りの文字列にする
    pitch_data = @song.pitch['frequencies'].map(&:to_f).join(' ')
  
    # Pythonスクリプトを実行してファイルとpitchデータを渡す
    stdout, stderr, status = Open3.capture3("python3 #{Rails.root.join('lib', 'python_scripts', 'file_read.py')} #{temp_file_path} '#{pitch_data}'")
  
    if status.success?
      @accuracy = stdout.strip.to_f # Pythonスクリプトからの出力をfloat型に変換
  
      # Historyレコードを作成して保存
      current_user.histories.create!(
        song: @song,
        score: @accuracy,        # accuracyをscoreに保存
        played_at: Time.current + 9.hours # 演奏された日時を保存
      )
  
      # 結果ページへリダイレクト
      redirect_to song_selection_result_path(accuracy: @accuracy)
    else
      @error = stderr # エラーメッセージを取得
      Rails.logger.error("Pythonスクリプトエラー: #{@error}")
      flash[:alert] = "解析に失敗しました: #{@error}"
      render :upload # 元のページに戻る
    end
  end
  

  def result
    @accuracy = params[:accuracy] # 結果表示用
  end

  private

end
