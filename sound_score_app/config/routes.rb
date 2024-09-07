Rails.application.routes.draw do
  root 'home#index'
  get 'song_selection/index'
  get 'song_selection/upload/:id', to: 'song_selection#upload', as: 'upload_song' # 楽曲IDを指定してアップロードページへ
  post 'song_selection/upload_song/:id', to: 'song_selection#upload_song', as: 'submit_song'
  get 'song_selection/result' # 結果表示用
  get 'mypage/index/:id', to: 'mypage#index', as: 'mypage' # マイページ


  devise_for :users, controllers: {
    registrations: 'users/registrations',
    sessions: 'users/sessions'
  }


  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # Defines the root path route ("/")
  # root "articles#index"
end
