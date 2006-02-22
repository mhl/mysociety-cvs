class DayofweekvoteController < ApplicationController
  
  def create
    @vote = Dayofweekvote.new(params[:dayofweekvote])
    if @vote.save
      flash[:notice] = "Vote for #{@vote.value} was stored."
      redirect_to :controller => 'vote', :action => ''
    else
      render :action => 'new'
    end
  end
  
end
