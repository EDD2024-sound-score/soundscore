class MypageController < ApplicationController
  # ユーザーがログインしていない場合、ログインページにリダイレクトする
  before_action :authenticate_user!
  before_action :correct_user

  def index
    # Kaminariを使用して、履歴を15件ずつ取得し、ページネーションを実装
    @histories = current_user.histories.order(played_at: :desc).page(params[:page]).per(15)
  end

    private
    def correct_user
      @user = User.find(params[:id])
      redirect_to(root_path, status: :see_other) unless @user == current_user
    end
  
end