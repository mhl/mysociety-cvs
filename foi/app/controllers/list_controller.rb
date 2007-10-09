# app/controllers/list_controller.rb:
# Show all of the FOI requests in the system.
#
# Copyright (c) 2007 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: list_controller.rb,v 1.2 2007-10-09 11:30:01 francis Exp $

class ListController < ApplicationController

    def index
        @info_request_pages, @info_requests = paginate :info_requests, :per_page => 25, :order => "created_at desc"
    end

end
