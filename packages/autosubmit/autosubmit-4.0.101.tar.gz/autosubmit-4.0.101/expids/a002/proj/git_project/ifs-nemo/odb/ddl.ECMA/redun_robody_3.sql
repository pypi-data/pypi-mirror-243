//
//-- ODB/SQL file 'redun_robody_3.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

SET $tslot = -1;

CREATE VIEW redun_robody_3 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_status@body  UPDATED,         // possibly updated (in ECMA)
  FROM   timeslot_index, index, hdr, body
  WHERE	 (obstype = $synop)
    AND  codetype IN (21, 22, 23, 24)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
