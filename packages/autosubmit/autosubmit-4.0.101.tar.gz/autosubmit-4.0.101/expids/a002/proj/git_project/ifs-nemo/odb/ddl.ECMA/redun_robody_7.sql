//
//-- ODB/SQL file 'redun_robody_7.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

SET $tslot = -1;

CREATE VIEW redun_robody_7 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_status@body  UPDATED,   // possibly updated (in ECMA)
         datum_event1@body  UPDATED,   // possibly updated (in ECMA)
         varno  UPDATED,               // possibly updated (in ECMA)
         vertco_reference_1,           // r/o
         obsvalue,                     // r/o
  FROM   timeslot_index, index, hdr, body
  WHERE	 obstype IN ($temp, $synop)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
