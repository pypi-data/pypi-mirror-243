//
//-- ODB/SQL file 'new_thinn_robody_8.sql'
//
//   Created:  15-Oct-2007
//

READONLY;

SET $tslot = -1;
SET $sensor = -1;

CREATE VIEW new_thinn_robody_8 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_status@body UPDATED,    // possibly updated (in ECMA)
         datum_event1@body UPDATED,    // possibly updated (in ECMA)
         varno,                        // r/o
  FROM   timeslot_index, index, hdr, body
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  (obstype = $satem)
    AND  (codetype = $resat)
//  AND  (obschar.codetype = $resat)
    AND  ($sensor == -1 OR sensor == $sensor)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
