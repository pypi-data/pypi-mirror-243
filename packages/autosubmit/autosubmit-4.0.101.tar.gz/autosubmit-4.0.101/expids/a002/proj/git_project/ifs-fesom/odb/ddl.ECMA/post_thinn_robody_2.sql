//
//-- ODB/SQL file 'post_thinn_robody_2.sql'
//
//   Last updated:  05-Mar-2003
//

READONLY;

SET $tslot = -1;
SET $ksensor_v = 0; // Must be initialized to zero

CREATE VIEW post_thinn_robody_2 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_status@body UPDATED,          // possibly updated (in ECMA)
         datum_event1@body UPDATED,          // possibly updated (in ECMA)
         varno,                        // r/o
         repres_error,                 // r/o
         obsvalue,                     // r/o
         fg_depar,                     // r/o
         vertco_reference_1,           // r/o
         vertco_reference_2,           // r/o
  FROM   timeslot_index, index, hdr, body, errstat
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  (obstype = $satem)
    AND  (codetype = $atovs)
    AND  (in_vector(sensor, $ksensor_v))
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
