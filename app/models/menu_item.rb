class MenuItem < ApplicationRecord
  belongs_to :menu

  # Attributes: item_name (string), calories (integer), menu_id (integer)
  # Define the attributes using attribute method:
  attribute :item_name, :string
  attribute :calories, :integer
  attribute :menu_id, :integer
end
