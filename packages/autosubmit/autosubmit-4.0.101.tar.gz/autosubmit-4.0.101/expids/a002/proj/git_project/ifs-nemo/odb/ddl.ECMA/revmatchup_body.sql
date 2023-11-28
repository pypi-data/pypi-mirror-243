//
//-- ODB/SQL file 'revmatchup_body.sql'
//
//   Last updated:  27-Jan-2005
//

SET $tslot = -1;
SET $pe = 0;

CREATE VIEW revmatchup_body AS
  SELECT seqno  READONLY,            // r/o
         entryno  READONLY,          // r/o
         datum_anflag@body UPDATED,
         datum_status@body UPDATED,
         datum_event1@body UPDATED,
         qc_a@body UPDATED,
         qc_l@body UPDATED,
         qc_pge@body UPDATED,
         an_depar@body UPDATED,
    FROM timeslot_index, index, hdr, body
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND report_status.active@hdr
     AND datum_status.active@body
     AND paral($pe, target)
;

