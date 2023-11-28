//
//-- ODB/SQL file 'gather4poolmask_counts.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

CREATE VIEW gather4poolmask_counts AS
   SELECT timeslot, obstype, codetype, sensor
         ,bufrtype, subtype
  	 ,body.len
     FROM index, hdr
  ORDERBY timeslot, obstype, codetype, sensor
         ,bufrtype, subtype
;
