//
//-- ODB/SQL file 'getsatid_resat.sql'
//
//   Last updated:  20-Feb-2009
//

READONLY;

CREATE VIEW getsatid_resat AS
     SELECT DISTINCT satellite_identifier@sat, product_type@resat, retrtype, sensor, varno
       FROM hdr, sat, resat, body
      WHERE codetype = $resat
      ORDERBY satellite_identifier@sat, product_type@resat, retrtype, sensor, varno
;
