//
//-- ODB/SQL file 'new_thinn_robody_4.sql'
//
//   Created:  16-Oct-2003
//

READONLY;

SET $tslot = -1;

CREATE VIEW new_thinn_robody_4 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_status@body UPDATED,    // possibly updated (in ECMA)
         datum_event1@body UPDATED,    // possibly updated (in ECMA)
         varno,                        // r/o
         vertco_reference_1,           // r/o
         obsvalue,                     // r/o
  FROM   timeslot_index, index, hdr, body
  WHERE  (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
   AND   (obstype = $satob)
    AND  ((codetype =  88)
    OR    (codetype =  89))
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
