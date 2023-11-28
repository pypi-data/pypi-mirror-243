//
//-- ODB/SQL file 'gather4poolmask.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

CREATE VIEW gather4poolmask AS
  SELECT DISTINCT timeslot@index, obstype, codetype, sensor
                 ,bufrtype, subtype
    FROM index, hdr
 ORDERBY timeslot@index, obstype, codetype, sensor
        ,bufrtype, subtype
;
