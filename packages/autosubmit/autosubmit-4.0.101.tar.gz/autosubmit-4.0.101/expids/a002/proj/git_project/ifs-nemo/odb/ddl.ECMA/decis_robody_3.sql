//
//-- ODB/SQL file 'decis_robody_3.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY; // .. except those marked with  UPDATED

SET $tslot = -1;

CREATE VIEW decis_robody_3 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_event1@body  UPDATED,         // possibly updated (in ECMA)
         datum_status@body  UPDATED,         // possibly updated (in ECMA)
         varno,                        // r/o
         vertco_reference_1,                        // r/o
         fg_depar,                     // r/o
         fg_error,                     // r/o
  FROM   timeslot_index, index, hdr, body, errstat
  WHERE	 (obstype = $airep)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
