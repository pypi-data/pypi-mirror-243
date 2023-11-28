//
//-- ODB/SQL file 'getsatid.sql'
//
//   Last updated:  30-Jun-2005
//

READONLY;

CREATE VIEW getsatid AS
     SELECT DISTINCT satellite_identifier@sat, codetype, retrtype, sensor
       FROM hdr, sat
      WHERE ((obstype = $satem) OR (obstype = $allsky))
      ORDERBY satellite_identifier@sat, codetype, retrtype, sensor
;
