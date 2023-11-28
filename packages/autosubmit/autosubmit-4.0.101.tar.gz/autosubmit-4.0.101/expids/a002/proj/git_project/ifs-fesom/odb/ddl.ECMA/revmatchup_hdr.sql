//
//-- ODB/SQL file 'revmatchup_hdr.sql'
//
//   Last updated:  27-Jan-2005
//

SET $tslot = -1;
SET $pe = 0;

CREATE VIEW revmatchup_hdr AS
  SELECT seqno  READONLY,      // r/o
         report_status,               // update
         report_event1,               // update
    FROM timeslot_index, index, hdr
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND report_status.active
     AND paral($pe, target)
;
