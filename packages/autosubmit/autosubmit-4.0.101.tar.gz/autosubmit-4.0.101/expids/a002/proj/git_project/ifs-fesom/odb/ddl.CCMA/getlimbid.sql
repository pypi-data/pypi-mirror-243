//
//-- ODB/SQL file 'getlimbid.sql'
//
//   Last updated:  30-Jun-2005
//

READONLY;

CREATE VIEW getlimbid AS
     SELECT DISTINCT satellite_identifier@sat, codetype, sensor
       FROM hdr, sat
      WHERE obstype = $limb
      ORDERBY satellite_identifier@sat, codetype, sensor
;
