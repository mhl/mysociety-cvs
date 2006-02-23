require File.dirname(__FILE__) + '/../test_helper'
require 'vote_controller'
require 'error_messages_for_custom'
# Re-raise errors caught by the controller.
class VoteController; def rescue_action(e) raise e end; end

class VoteControllerTest < Test::Unit::TestCase
  def setup
    @controller = VoteController.new
    @request    = ActionController::TestRequest.new
    @response   = ActionController::TestResponse.new
  end

  # Replace this with your real tests.
  def test_index
    get :index
    assert_response :success
  end

  def test_fourth_vote
    @request.remote_addr = '1.2.3.4'
    post :create, :meetupvote => {:dayofweek => 'Sunday', :weekofmonth => '1st'}
    assert_redirected_to :action => 'index'
    follow_redirect
    assert_tag :content => "You have used all your votes"    
  end
end
