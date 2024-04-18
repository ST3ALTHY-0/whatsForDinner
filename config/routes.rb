Rails.application.routes.draw do
  get 'scripts/execute_python'
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html
  root "menus#index"

  post '/execute_python', to: 'scripts#execute_python'

  get '/menus', to: 'menus#show'
  # Reveal health status on /up that returns 200 if the app boots with no exceptions, otherwise 500.
  # Can be used by load balancers and uptime monitors to verify that the app is live.
  get "up" => "rails/health#show", as: :rails_health_check

  # Defines the root path route ("/")
  # root "posts#index"
end
