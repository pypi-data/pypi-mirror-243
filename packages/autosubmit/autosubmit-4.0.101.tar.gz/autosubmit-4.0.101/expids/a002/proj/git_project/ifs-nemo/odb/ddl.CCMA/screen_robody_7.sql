//
//-- ODB/SQL file 'screen_robody_7.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY; // For printing statistics only

SET $tslot = -1;

CREATE VIEW screen_robody_7 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_status@body,                  // r/o
         datum_event1@body,                  // r/o
         varno,                        // r/o
         fg_depar,                     // r/o
  FROM   timeslot_index, index, hdr, body
  WHERE  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
