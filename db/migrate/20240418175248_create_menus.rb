class CreateMenus < ActiveRecord::Migration[7.1]
  def change
    create_table :menus do |t|
      t.string :date
      t.string :menu_time
      t.string :item_name
      t.string :calories

      t.timestamps
    end
  end
end
