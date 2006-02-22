--
-- PostgreSQL database dump
-- schema.sql:
-- Schema for meetup day preference app (daycount)
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
-- Name: dayofmonthvotes_id_seq; Type: SEQUENCE SET
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('dayofmonthvotes', 'id'), 3, true);

--
-- Name: dayofweekvotes; Type: TABLE
--

CREATE TABLE dayofweekvotes (
    value text NOT NULL,
    id serial NOT NULL
);


--
-- Name: dayofweekvotes_id_seq; Type: SEQUENCE SET
--
SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('dayofweekvotes', 'id'), 4, true);


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
