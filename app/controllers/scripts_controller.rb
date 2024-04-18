class ScriptsController < ApplicationController

  def execute_python
    # Execute the Python script and capture output
    output = `python3 /home/luke/whatsForDinner/lib/assets/IUPUIDiningWebScrapper.py`
    
    # Split the output into sections based on "Time of Day" headers
    menu_sections = output.split("***************************\n")
    
    # Loop through each menu section
    menu_sections.each do |section|
      # Extract the menu date and time of day from the section
      menu_date = section[/Menu Date: (.*)/, 1]
      time_of_day = section[/Time of Day: (.*)/, 1]

      existing_menu = Menu.find_by(date: menu_date, menu_time: time_of_day)

    unless existing_menu
      # Create a new Menu record
      menu = Menu.new(date: menu_date, menu_time: time_of_day)
      
      # Extract the menu items and their respective calorie counts
      menu_items_with_calories = section.scan(/Menu item -  (.*?) - (\d+) cal/)
      
      # Loop through each menu item and calorie count
      menu_items_with_calories.each do |item, calories|
        # Build a MenuItem record and associate it with the Menu
        menu.menu_items.build(item_name: item.strip, calories: calories.to_i)
      end
      
      # Save the Menu record along with its associated MenuItems
      menu.save
    end
  end
    
    # Redirect or render response as needed
    redirect_to root_path
  end

end
