//
//-- ODB/SQL file 'decis_robody_1.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY; // .. except those marked with  UPDATED

SET $kset = 0;
SET $tslot = -1;

CREATE VIEW decis_robody_1 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_event1@body  UPDATED,         // possibly updated (in ECMA)
         datum_status@body  UPDATED,         // possibly updated (in ECMA)
         vertco_type,                  // r/o
         varno,                        // r/o
         vertco_reference_1  UPDATED,  // possibly updated (in ECMA)
         obsvalue,                     // r/o
         fg_depar,                     // r/o
         pers_error,                   // r/o
         final_obs_error  UPDATED,     // possibly updated (in ECMA)
         obs_error  UPDATED,           // possibly updated (in ECMA)
  FROM   timeslot_index, index, hdr, body, errstat
  WHERE	 (kset = $kset)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
