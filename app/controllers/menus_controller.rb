class MenusController < ApplicationController
  def index
    @menus = Menu.all
    @menuitems = MenuItem.all
  end
  
    def show
    end

end
