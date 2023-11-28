//
//-- ODB/SQL file 'sathdr_limb.sql'
//
//   Last updated:  23-Nov-2004
//

SET $tslot = -1;
SET $obstype = 0;
SET $codetype = 0;

CREATE VIEW sathdr_limb AS
  SELECT seqno  READONLY,         // r/o; MUST COME FIRST
         satellite_identifier@sat,                   // r/o
         ntan,                    // r/o
         ztan[1:$mx_limb_tan],     // r/o
         ptan[1:$mx_limb_tan],     // r/o
         thtan[1:$mx_limb_tan]     // r/o
  FROM   index, hdr, sat, limb
  WHERE	 obstype = $limb AND codetype = $lrad
    AND  (($tslot == -1 AND timeslot > 0) OR (timeslot == $tslot))
;
