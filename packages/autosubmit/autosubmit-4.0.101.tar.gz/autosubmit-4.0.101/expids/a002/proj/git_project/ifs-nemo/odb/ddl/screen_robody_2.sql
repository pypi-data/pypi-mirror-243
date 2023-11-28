//
//-- ODB/SQL file 'screen_robody_2.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

SET $tslot = -1;

CREATE VIEW screen_robody_2 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
	 datum_rdbflag@body,               // r/o
         datum_status@body  UPDATED,   // possibly updated (in ECMA)
         datum_event1@body  UPDATED,   // possibly updated (in ECMA)
         datum_event2@body  UPDATED,   // possibly updated (in ECMA)
         varno,                        // r/o
         vertco_reference_1,           // r/o
         final_obs_error UPDATED,      // possibly updated (in ECMA)
         datum_status_hires@update_1  UPDATED,
  FROM   timeslot_index, index, hdr, body, errstat, update_1
  WHERE  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
