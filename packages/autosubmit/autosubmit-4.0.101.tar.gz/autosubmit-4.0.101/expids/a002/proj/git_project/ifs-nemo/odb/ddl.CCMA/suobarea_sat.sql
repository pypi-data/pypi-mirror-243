//
//-- ODB/SQL file 'suobarea_sat.sql'
//
//   Last updated:  08-Feb-2005
//

SET $tslot = -1;

READONLY;

CREATE VIEW suobarea_sat AS
  SELECT codetype,
         instrument_type,
         retrtype,
         areatype UPDATED,
         obstype, 
         satellite_identifier@sat, 
         sensor,
    FROM timeslot_index, index, hdr, sat
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
         AND ((obstype = $satem) OR (obstype = $allsky))
;
