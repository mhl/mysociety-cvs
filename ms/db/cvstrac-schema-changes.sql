--
-- cvstrac-schema-changes.sql:
-- Additions to the cvstrac database for our volunteer tasks system.
--
-- Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
-- Email: chris@mysociety.org; WWW: http://www.mysociety.org/
--
-- $Id: cvstrac-schema-changes.sql,v 1.1 2006-01-09 14:05:51 chris Exp $
--

create table volunteer_interest (
    ticket_num integer not null references ticket(tn),
    name text not null,
    email text not null,
    when integer not null
);
