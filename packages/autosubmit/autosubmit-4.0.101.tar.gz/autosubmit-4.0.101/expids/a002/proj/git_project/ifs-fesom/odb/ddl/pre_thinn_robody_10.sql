//
//-- ODB/SQL file 'pre_thinn_robody_10.sql'
//

READONLY;

SET $tslot = -1;

CREATE VIEW pre_thinn_robody_10 AS
  SELECT entryno,                      // r/o
         datum_status@body,                  // possibly updated (in ECMA)
         datum_event1@body,                  // possibly updated (in ECMA)
         varno,                        // r/o
         fg_depar,                     // r/o
         obs_error,                     // r/o
         azimuth@radar_body                       // r/o
  FROM   timeslot_index, index, hdr, body, errstat, sat, radar, radar_body
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  (obstype = $radar)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
