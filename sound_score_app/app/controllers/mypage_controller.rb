class MypageController < ApplicationController
  def index
    @history = current_user.histories
  end
end
