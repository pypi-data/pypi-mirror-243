//
//-- ODB/SQL file 'satellite_identifier_list.sql'
//
//   Last updated:  01/02/2011
//


READONLY;
CREATE VIEW satellite_identifier_list AS
  SELECT DISTINCT satellite_identifier,
    FROM sat
    where datastream=0
;

