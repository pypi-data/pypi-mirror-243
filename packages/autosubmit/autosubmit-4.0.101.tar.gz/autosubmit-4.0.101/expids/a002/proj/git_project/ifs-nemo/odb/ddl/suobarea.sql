//
//-- ODB/SQL file 'suobarea.sql'
//
//   Last updated:  08-Feb-2005
//

SET $tslot = -1;

READONLY;

CREATE VIEW suobarea AS
  SELECT codetype,
         instrument_type,
         retrtype,
         areatype UPDATED,
	 obstype,
    FROM timeslot_index, index, hdr
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
         AND (obstype /= $satem) AND (obstype /= $satob) AND (obstype /= $limb)
         AND (obstype /= $allsky)
         AND (obstype /= $scatt)
;
