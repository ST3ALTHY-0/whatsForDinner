# Use this file to easily define all of your cron jobs.
#
# It's helpful, but not entirely necessary to understand cron before proceeding.
# http://en.wikipedia.org/wiki/Cron

# Example:
#
# set :output, "/path/to/my/cron_log.log"
#
# every 2.hours do
#   command "/usr/bin/some_great_command"
#   runner "MyModel.some_method"
#   rake "some:great:rake:task"
# end
#
# every 4.days do
#   runner "AnotherModel.prune_old_records"
# end

# Learn more: http://github.com/javan/whenever

#Creates a output log for you to view previously run cron jobs
set :output, "log/cron.log"

#Sets the environment to run during development mode (Set to production by default)
set :environment, "production"

#Runs the python script every day at 12:00 AM
#every 1.day, at: "1:00 am" do
#  runner "ScriptsController.execute_python"
#end

# Runs a custom Ruby script that executes the Python script
every 1.day, at: "1:00 am" do
  command "/bin/bash -l -c 'cd /home/luke/whatsForDinner && bundle exec rails runner /home/luke/whatsForDinner/lib/assets/script.rb'"
  puts "Ran the script"
end
