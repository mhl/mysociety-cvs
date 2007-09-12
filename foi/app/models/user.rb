# models/user.rb:
# Model of people who use the site to file requests, make comments etc.
#
# Copyright (c) 2007 UK Citizens Online Democracy. All rights reserved.
# Email: francis@mysociety.org; WWW: http://www.mysociety.org/
#
# $Id: user.rb,v 1.6 2007-09-12 08:52:23 francis Exp $

require 'digest/sha1'

class User < ActiveRecord::Base
    validates_presence_of :email
    validates_uniqueness_of :email, :case_sensitive => false

    validates_presence_of :name

    has_many :info_request

    attr_accessor :password_confirmation
    validates_confirmation_of :password

    def validate
        errors.add_to_base("Missing password") if hashed_password.blank?
        errors.add(:email, "doesn't look like a valid address") unless MySociety::Validate.is_valid_email(email)
    end

    # Return user given login email and password
    def self.authenticate(email, password)
        user = self.find(:first, :conditions => [ 'email ilike ?', email ] )
        if user
            expected_password = encrypted_password(password, user.salt)
            if user.hashed_password != expected_password
                user = nil
            end
        end
        user
    end

    # Virtual password attribute, which stores the hashed password, rather than plain text.
    def password
        @password
    end
    def password=(pwd)
        @password = pwd
        return if pwd.blank?
        create_new_salt
        self.hashed_password = User.encrypted_password(self.password, self.salt)
    end

    private

    def self.encrypted_password(password, salt)
        string_to_hash = password + salt # XXX need to add a secret here too?
        Digest::SHA1.hexdigest(string_to_hash)
    end
    
    def create_new_salt
        self.salt = self.object_id.to_s + rand.to_s
    end
end

