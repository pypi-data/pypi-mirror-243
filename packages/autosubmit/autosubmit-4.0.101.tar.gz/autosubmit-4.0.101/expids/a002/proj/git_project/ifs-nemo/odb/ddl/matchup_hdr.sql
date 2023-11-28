//
//-- ODB/SQL file 'matchup_hdr.sql'
//
//   Last updated:  22-Jun-2005
//

SET $tslot = -1;
SET $pe = 0;
SET $hdr_min = 1; // Here: the smallest procid (=global poolno) of the obs.grp. (ECMA)
SET $hdr_max = 0; // Here: the number of pools in (output) ECMA-database

CREATE VIEW matchup_hdr AS
  SELECT seqno  READONLY,      // r/o
         report_status,               // update
         report_event1,               // update
    FROM timeslot_index, index, hdr
   WHERE target > 0
     AND 1 <= procid - $hdr_min + 1 <= $hdr_max
     AND (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND report_status.active
     AND paral($pe, procid - $hdr_min + 1)
;
