//
//-- ODB/SQL file 'pre_thinn_robody_9.sql'
//
//   Last updated:  18-Dec-2007
//

READONLY;

SET $tslot = -1;

CREATE VIEW pre_thinn_robody_9 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_status@body  UPDATED,   // possibly updated (in ECMA)
         datum_event1@body  UPDATED,   // possibly updated (in ECMA)
         varno,                        // r/o
         bg_layerno,                    // r/o
         vertco_reference_2,           // r/o
  FROM   timeslot_index, index, hdr, body, sat, gnssro, gnssro_body
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  (obstype = 10)
    AND  (codetype =  250)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
