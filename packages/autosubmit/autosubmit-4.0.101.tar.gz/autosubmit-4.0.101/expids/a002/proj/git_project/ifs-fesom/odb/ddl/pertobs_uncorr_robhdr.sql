//
//-- ODB/SQL file 'pertobs_uncorr_robhdr.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY; // All read/only except selected columns marked with  UPDATED

SET $kset = 0;
SET $tslot = -1;

CREATE VIEW pertobs_uncorr_robhdr AS
  SELECT seqno,               // r/o; MUST BE FIRST
         body.len,            // r/o
         report_status,              // r/o
         obstype,             // r/o
         codetype,            // r/o
  FROM   timeslot_index, index, hdr
  WHERE	 (kset = $kset)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
