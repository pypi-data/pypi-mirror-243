//
//-- ODB/SQL file 'sat_aeolus.sql'
//
//   Last updated:  12-06-2018
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sat_aeolus AS
  SELECT seqno  READONLY,         // r/o; MUST BECOME FIRST
         azimuth  READONLY,    // r/o
    FROM timeslot_index, index, hdr, sat
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset
     AND obstype = $lidar
     AND codetype = 187
   ORDERBY seqno
;
