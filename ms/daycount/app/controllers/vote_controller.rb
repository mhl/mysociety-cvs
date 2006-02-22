class VoteController < ApplicationController
  layout "mysociety"
  
  def index
    @weekvotes = Dayofweekvote.find_all
    @monthvotes = Dayofmonthvote.find_all
  end
  
end
