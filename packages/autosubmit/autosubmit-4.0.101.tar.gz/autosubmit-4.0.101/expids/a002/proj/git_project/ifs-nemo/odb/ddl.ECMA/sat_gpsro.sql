//
//-- ODB/SQL file 'sat_gpsro.sql'
//
//   Last updated:  17-Mar-2011
//

READONLY; // .. except where  UPDATED qualifier was found

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sat_gpsro AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         radcurv UPDATED,                      // maybe updated?
         undulation,                   // r/o 
  FROM   timeslot_index, index, hdr, sat, gnssro
  WHERE  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
    AND  kset = $kset
    AND obstype=$limb AND codetype=$gpsro
 ORDERBY seqno
;
