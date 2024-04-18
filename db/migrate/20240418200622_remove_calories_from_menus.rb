class RemoveCaloriesFromMenus < ActiveRecord::Migration[7.1]
  def change
    remove_column :menus, :calories, :integer
  end
end
