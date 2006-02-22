require File.dirname(__FILE__) + '/../test_helper'

class DayofmonthvoteTest < Test::Unit::TestCase
  fixtures :dayofmonthvotes

  # Replace this with your real tests.
  def test_truth
    assert_kind_of Dayofmonthvote, dayofmonthvotes(:first)
  end
end
