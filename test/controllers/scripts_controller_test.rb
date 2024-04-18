require "test_helper"

class ScriptsControllerTest < ActionDispatch::IntegrationTest
  test "should get execute_python" do
    get scripts_execute_python_url
    assert_response :success
  end
end
