//
//-- ODB/SQL file 'new_thinn_robody_10.sql'
//

READONLY;

SET $tslot = -1;

CREATE VIEW new_thinn_robody_10 AS
  SELECT entryno,                      // r/o
         datum_status@body UPDATED,          // possibly updated (in ECMA)
         datum_event1@body UPDATED,          // possibly updated (in ECMA)
         varno,                        // r/o
         fg_depar,                     // r/o
  FROM   timeslot_index, index, hdr, body
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  (obstype = $radar)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
