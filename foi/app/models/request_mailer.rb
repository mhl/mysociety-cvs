# models/request_mailer.rb:
# Emails which go to public bodies on behalf of users.
#
# Copyright (c) 2007 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: request_mailer.rb,v 1.8 2007-12-11 12:09:37 francis Exp $

class RequestMailer < ActionMailer::Base

    def initial_request(info_request, outgoing_message)
        @from = info_request.incoming_email
        if MySociety::Config.getbool("STAGING_SITE", 1)
            @recipients = info_request.user.email
        else
            @recipients = info_request.public_body.request_email
        end
        @subject    = 'Freedom of Information Request - ' + info_request.title
        @body       = {:info_request => info_request, :outgoing_message => outgoing_message}
    end

    def bounced_message(email)
        @from = MySociety::Config.get("CONTACT_EMAIL", 'contact@localhost')
        @recipients = @from
        @subject = "Incoming email to unknown FOI request"
        email.setup_forward(self)
    end

    def new_response(info_request, incoming_message)
        post_redirect = PostRedirect.new(
            :uri => classify_request_url(:incoming_message_id => incoming_message.id),
            :user_id => info_request.user.id)
        post_redirect.save!
        url = confirm_url(:email_token => post_redirect.email_token)

        @from = MySociety::Config.get("CONTACT_EMAIL", 'contact@localhost')
        @recipients = info_request.user.email
        @subject = "New reponse to your FOI request  - " + info_request.title
        @body = { :incoming_message => incoming_message, :info_request => info_request, :url => url }
    end

    # Copy of function from action_mailer/base.rb, which passes the
    # raw_email to the member function, as we want to record it.
    # script/mailin calls this function.
    def self.receive(raw_email)
        logger.info "Received mail:\n #{raw_email}" unless logger.nil?
        mail = TMail::Mail.parse(raw_email)
        mail.base64_decode
        new.receive(mail, raw_email)
    end

    def receive(email, raw_email)
        # Find which info requests the email is for
        info_requests = []
        for address in (email.to || []) + (email.cc || [])
            info_request = InfoRequest.find_by_incoming_email(address)
            info_requests.push(info_request) if info_request
        end

        # Nothing found
        if info_requests.size == 0
            RequestMailer.deliver_bounced_message(email)
        end

        # Send the message to each request
        for info_request in info_requests
            info_request.receive(email, raw_email)
        end
    end

end
