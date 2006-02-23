require 'error_messages_for_custom'
class VoteController < ApplicationController
  include ActionView::Helpers::TextHelper
  include ActionView::Helpers::ActiveRecordHelper
  include ActionView::Helpers::TagHelper
  layout "mysociety"  

  DaysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
  WeeksOfMonth = ['1st','2nd','3rd','4th','last']

  def index
    @meetupvotes = Meetupvote.find_all
    @counts = Hash.new(nil)
    @meetupvotes.each do |vote|
        @counts[[vote.dayofweek,vote.weekofmonth]] = 0 if @counts[[vote.dayofweek,vote.weekofmonth]].nil?
        @counts[[vote.dayofweek,vote.weekofmonth]] += 1
    end
    @vote = Meetupvote.new
    @weeksofmonth = WeeksOfMonth
    @daysofweek = DaysOfWeek
    setIP(@vote)
  end

  def create
    @vote = Meetupvote.new
    @vote.dayofweek = params[:meetupvote][:dayofweek] if DaysOfWeek.include?(params[:meetupvote][:dayofweek])
    @vote.weekofmonth = params[:meetupvote][:weekofmonth] if WeeksOfMonth.include?(params[:meetupvote][:weekofmonth]) 
    setIP(@vote)
    if @vote.save
      flash[:notice] = "Your vote for #{@vote.dayofweek}, #{@vote.weekofmonth} week of the month was stored. "
      redirect_to :action => 'index'
    else
      flash[:notice] = error_messages_for_custom(:vote)
      redirect_to :action => 'index'
    end
  end
  
  def setIP(vote)
    ipaddr  = request.remote_ip()
    vote.ipaddr = ipaddr
  end
end
