//
//-- ODB/SQL file 'suobarea_limb.sql'
//
//   Last updated:  22-Nov-2004
//

SET $tslot = -1;

CREATE VIEW suobarea_limb AS
  SELECT areatype,                    // updated
	     codetype READONLY, 
         satellite_identifier@sat READONLY, 
         sensor READONLY  // r/o
    FROM index, hdr, sat
   WHERE (($tslot == -1 AND timeslot > 0) OR (timeslot == $tslot))
         AND (obstype = $limb )
;
