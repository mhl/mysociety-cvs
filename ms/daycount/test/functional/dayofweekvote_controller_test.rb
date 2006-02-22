require File.dirname(__FILE__) + '/../test_helper'
require 'dayofweekvote_controller'

# Re-raise errors caught by the controller.
class DayofweekvoteController; def rescue_action(e) raise e end; end

class DayofweekvoteControllerTest < Test::Unit::TestCase
  def setup
    @controller = DayofweekvoteController.new
    @request    = ActionController::TestRequest.new
    @response   = ActionController::TestResponse.new
  end

  # Replace this with your real tests.
  def test_truth
    assert true
  end
end
