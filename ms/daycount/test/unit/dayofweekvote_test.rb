require File.dirname(__FILE__) + '/../test_helper'

class DayofweekvoteTest < Test::Unit::TestCase
  fixtures :dayofweekvotes

  # Replace this with your real tests.
  def test_truth
    assert_kind_of Dayofweekvote, dayofweekvotes(:first)
  end
end
