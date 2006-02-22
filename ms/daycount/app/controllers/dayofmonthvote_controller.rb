class DayofmonthvoteController < ApplicationController

  def create
    @vote = Dayofmonthvote.new(params[:dayofmonthvote])
    if @vote.save
      flash[:notice] = "Vote for day of month #{@vote.value} was stored."
      redirect_to :controller => 'vote', :action => ''
    else
      render :action => 'new'
    end
  end

end
  

