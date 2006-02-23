--
-- PostgreSQL database dump
-- schema.sql:
-- Schema for mysociety site - first tables 
-- are for meetup day preference app (daycount)
--
-- Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
-- Email: louise.crow@gmail.com; WWW: http://www.mysociety.org/
--

-- Name: meetupvotes; Type: TABLE
--

CREATE TABLE meetupvotes (
    id serial NOT NULL,
    dayofweek text NOT NULL,
    weekofmonth text NOT NULL,
    ipaddr text NOT NULL
);


--
-- Name: pk_meetupvotes; Type: CONSTRAINT
--

ALTER TABLE ONLY meetupvotes
    ADD CONSTRAINT pk_meetupvotes PRIMARY KEY (id);