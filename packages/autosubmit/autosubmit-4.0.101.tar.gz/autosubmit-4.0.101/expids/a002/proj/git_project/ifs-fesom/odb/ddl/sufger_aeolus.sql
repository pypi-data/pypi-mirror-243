//
//-- ODB/SQL file 'sufger_aeolus.sql'
//
//   Last updated:  12-01-2018
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sufger_aeolus AS
  SELECT seqno  READONLY,      // r/o; MUST BECOME FIRST
         body.len,             // r/o
         azimuth  READONLY,    // r/o
    FROM timeslot_index, index, hdr, sat
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset
     AND obstype = $lidar
     AND codetype = 187
;
