class RemoveItemNameFromMenus < ActiveRecord::Migration[7.1]
  def change
    remove_column :menus, :item_name, :string
  end
end
