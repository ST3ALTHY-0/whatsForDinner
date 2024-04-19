class MenusController < ApplicationController
  def index
    @menus = Menu.order(date: :desc, menu_time: :desc).limit(3).includes(:menu_items)
  end

  def show
  end
end
