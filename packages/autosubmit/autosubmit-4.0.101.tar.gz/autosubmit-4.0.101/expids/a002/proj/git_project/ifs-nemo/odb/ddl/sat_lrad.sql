//
//-- ODB/SQL file 'sat_lrad.sql'
//
//   Last updated:  22-Nov-2004
//

UPDATED;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sat_lrad AS
  SELECT seqno  READONLY,         // r/o; MUST COME FIRST
         satellite_identifier@sat READONLY,                   // r/o
         ntan,                    // r/o
         ztan[1:$mx_limb_tan],     // r/o
         ptan[1:$mx_limb_tan],     // r/o
         thtan[1:$mx_limb_tan],     // r/o
         window_rad[1:$mx_limb_tan],     // r/o
         cloud_index[1:$mx_limb_tan]     // r/o
  FROM   timeslot_index, index, hdr, sat, limb
  WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND kset = $kset
    AND obstype = $limb AND codetype = $lrad
 ORDERBY seqno
;
