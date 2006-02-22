require File.dirname(__FILE__) + '/../test_helper'
require 'dayofmonthvote_controller'

# Re-raise errors caught by the controller.
class DayofmonthvoteController; def rescue_action(e) raise e end; end

class DayofmonthvoteControllerTest < Test::Unit::TestCase
  def setup
    @controller = DayofmonthvoteController.new
    @request    = ActionController::TestRequest.new
    @response   = ActionController::TestResponse.new
  end

  # Replace this with your real tests.
  def test_truth
    assert true
  end
end
