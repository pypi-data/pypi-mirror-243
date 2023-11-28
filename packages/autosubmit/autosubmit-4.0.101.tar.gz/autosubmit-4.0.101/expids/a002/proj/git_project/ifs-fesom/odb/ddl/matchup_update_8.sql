//
//-- ODB/SQL file 'matchup_update_8.sql'
//
//   Last updated:  27-Feb-2003
//

SET $tslot = -1;
SET $pe = 0;

CREATE VIEW matchup_update_8 AS
  SELECT seqno READONLY,            // r/o
         entryno READONLY,          // r/o
         "/.*@update.*/"        // update (even if an MDI)
    FROM timeslot_index, index, hdr, body , update[min(8,$nmxupd)]
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND report_status.active@hdr
     AND datum_status.active@body
     AND paral($pe, procid)
;
