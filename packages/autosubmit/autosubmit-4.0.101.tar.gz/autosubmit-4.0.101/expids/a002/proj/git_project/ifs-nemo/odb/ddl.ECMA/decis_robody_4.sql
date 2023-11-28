//
//-- ODB/SQL file 'decis_robody_4.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY; // .. except those marked with  UPDATED

SET $kset = -1;
SET $tslot = -1;

CREATE VIEW decis_robody_4 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         varno,                        // r/o
         datum_event1@body  UPDATED,         // possibly updated (in ECMA)
         datum_status@body  UPDATED,         // possibly updated (in ECMA)
         invresid,                     // r/o
         obsvalue,                     // r/o
  FROM   timeslot_index, index, hdr, sat, scatt, body, scatt_body
  WHERE	 (obstype = $scatt)
    AND	 (kset = $kset OR $kset = -1)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
