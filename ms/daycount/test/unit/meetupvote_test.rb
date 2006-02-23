require File.dirname(__FILE__) + '/../test_helper'

class MeetupvoteTest < Test::Unit::TestCase
  fixtures :meetupvotes

  def setup
    @meetupvote = Meetupvote.find(1)
  end

  # Replace this with your real tests.
  def test_create
    assert_kind_of Meetupvote,  @meetupvote
    assert_equal 1, @meetupvote.id
    assert_equal '1.2.3.4', @meetupvote.ipaddr
    assert_equal 0, @meetupvote.count_votes_remaining
  end

  def test_ip_counts
    assert_equal Meetupvote.find_all_by_ipaddr('1.2.3.4').length, 3
    assert_equal Meetupvote.find_all_by_ipaddr('4.3.2.1').length, 1
  end
end
