//
//-- ODB/SQL file 'pre_thinn_robody_6.sql'
//
//   Last updated:  08-Nov-2007
//

READONLY;

SET $obstype = -1;
SET $codetype = -1;
SET $tslot = -1;

CREATE VIEW pre_thinn_robody_6 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_status@body  UPDATED,         // possibly updated (in ECMA)
         datum_event1@body  UPDATED,         // possibly updated (in ECMA)
         varno,                        // r/o
  FROM   timeslot_index, index, hdr, body
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  ( obstype = $obstype )
    AND  (codetype = $codetype)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
