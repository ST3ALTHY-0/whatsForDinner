class ApplicationController < ActionController::Base
    python_output = `/home/luke/whatsForDinner/lib/assets/IUPUIDiningWebScrapper.py`

    output_file_path = Rails.public_path.join('output_file.txt')

    File.open(output_file_path, 'w') do |file|
        file.write(python_output)
    
end
