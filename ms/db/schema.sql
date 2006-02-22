--
-- PostgreSQL database dump
-- schema.sql:
-- Schema for mysociety site - first tables 
-- are formeetup day preference app (daycount)
--
-- Copyright (c) 2005 UK Citizens Online Democracy. All rights reserved.
-- Email: louise.crow@gmail.com; WWW: http://www.mysociety.org/
--

-- Name: dayofmonthvotes; Type: TABLE
--

CREATE TABLE dayofmonthvotes (
    id serial NOT NULL,
    value text NOT NULL
);

--
-- Name: dayofweekvotes; Type: TABLE
--

CREATE TABLE dayofweekvotes (
    value text NOT NULL,
    id serial NOT NULL
);


--
-- Name: pk_dayofweekvote; Type: CONSTRAINT
--

ALTER TABLE ONLY dayofweekvotes
    ADD CONSTRAINT pk_dayofweekvote PRIMARY KEY (id);


--
-- Name: pk_dayofmonthvote; Type: CONSTRAINT
--

ALTER TABLE ONLY dayofmonthvotes
    ADD CONSTRAINT pk_dayofmonthvote PRIMARY KEY (id);
