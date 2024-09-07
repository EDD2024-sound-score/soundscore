Rails.application.routes.draw do
  get 'mypage/index'

  root "song_selection#index"       # 楽曲選択画面
  get 'song_selection/upload'       # 自分の楽曲をアップロードする画面
  post 'song_selection/upload_song' # 楽曲をアップロードする処理
  get 'song_selection/result'       # 精度の結果を出力する画面

  devise_for :users, controllers: {
    registrations: 'users/registrations',
    sessions: 'users/sessions'
  }


  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Defines the root path route ("/")
  # root "articles#index"
end
