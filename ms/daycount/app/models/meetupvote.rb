class Meetupvote < ActiveRecord::Base
	
	MaxVotes = 3
	validates_presence_of :dayofweek, :weekofmonth, :ipaddr
	attr_accessor :votes_remaining
	attr_accessible :votes_remaining
	attr_protected :dayofweek, :weekofmonth

	def validate
		self.votes_remaining = count_votes_remaining
		errors.add_to_base("You have used all your votes") if self.votes_remaining < 1
	end

	def after_create
		self.votes_remaining -= 1
	end

	def count_votes_remaining
		votes_for_ip = Meetupvote.find_all_by_ipaddr(ipaddr)
		if votes_for_ip.nil? 
			votes_used = 0
		else
			votes_used = votes_for_ip.length
		end 
		
		return MaxVotes - votes_used
	end
end
