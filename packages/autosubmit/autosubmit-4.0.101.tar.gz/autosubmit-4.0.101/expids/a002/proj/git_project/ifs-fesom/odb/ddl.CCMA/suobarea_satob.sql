//
//-- ODB/SQL file 'suobarea_satob.sql'
//
//   Last updated:  08-Feb-2005
//

SET $tslot = -1;

READONLY;

CREATE VIEW suobarea_satob AS
  SELECT codetype,
         instrument_type,
         retrtype,
         areatype UPDATED,
    	 obstype, 
         satellite_identifier@sat,
         comp_method@satob,
    FROM timeslot_index, index, hdr, sat, satob
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
         AND (obstype = $satob)
;
