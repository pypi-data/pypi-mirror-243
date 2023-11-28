//
//-- ODB/SQL file 'sufger_robody_1.sql'
//
//   Last updated:  08-Sep-2006
//

READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sufger_robody_1 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         vertco_type,                  // r/o
         varno,                        // r/o
         datum_status@body,            // possibly updated
         datum_event1@body,            // r/o
         vertco_reference_1,           // r/o
         vertco_reference_2,           // r/o
         fg_depar  UPDATED,            // possibly updated (in ECMA)
         fg_error  UPDATED,            // possibly updated (in ECMA)
         eda_spread UPDATED,           // possible updated (in ECMA)
         final_obs_error,              // r/o
  FROM   timeslot_index, index, hdr, body, errstat
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND  kset = $kset
;
