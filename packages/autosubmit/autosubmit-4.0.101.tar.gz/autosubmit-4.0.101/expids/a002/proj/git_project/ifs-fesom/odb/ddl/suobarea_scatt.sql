//
//-- ODB/SQL file 'suobarea_scatt.sql'
//
//   Last updated:  08-Feb-2005
//

SET $tslot = -1;

READONLY;

CREATE VIEW suobarea_scatt AS
  SELECT codetype,
         instrument_type,
         retrtype,
         areatype UPDATED,
    	 obstype, 
         reportype,
    FROM timeslot_index, index, hdr
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
         AND (obstype = $scatt)
;
