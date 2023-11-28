//
//-- ODB/SQL file 'max_values.sql'
//
//   Last updated:  01/03/2011
//

READONLY;

CREATE VIEW max_values AS
  SELECT max(scanpos), max(vertco_reference_1),
    FROM hdr,sat,radiance, body
;

