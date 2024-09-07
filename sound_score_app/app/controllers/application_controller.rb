class ApplicationController < ActionController::Base
  protected

  # ログイン後のリダイレクト先
  def after_sign_in_path_for(resource)
    song_selection_index_path # ログイン後のリダイレクト先
  end

  # サインアップ後のリダイレクト先
  def after_sign_up_path_for(resource)
    song_selection_index_path # サインアップ後のリダイレクト先
  end
end
