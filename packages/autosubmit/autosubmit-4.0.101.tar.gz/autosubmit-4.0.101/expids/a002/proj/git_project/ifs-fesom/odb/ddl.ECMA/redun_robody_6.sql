//
//-- ODB/SQL file 'redun_robody_6.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

SET $tslot = -1;

CREATE VIEW redun_robody_6 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_status@body  UPDATED,         // possibly updated (in ECMA)
         datum_event1@body  UPDATED,         // possibly updated (in ECMA)
         datum_anflag,                       // r/o
         level@conv_body,                        // r/o
         vertco_type,                  // r/o
         varno,                        // r/o
         vertco_reference_1,                        // r/o
  FROM   timeslot_index, index, hdr, body, conv, conv_body
  WHERE	 obstype IN ($temp, $pilot)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
