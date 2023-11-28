//
//-- ODB/SQL file 'bay_thinn_robody.sql'
//
//   Last updated:  18-dec-2017
//

READONLY;

SET $tslot = -1;
SET $ksensor = -1;

CREATE VIEW bay_thinn_robody AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         entryno,                      // r/o
         datum_status UPDATED,         // possibly updated (in ECMA)
         datum_event1 UPDATED,         // possibly updated (in ECMA)
         varno,                        // r/o
         vertco_reference_1@body,      // r/o
         obsvalue,                     // r/o
         fg_depar,                     // r/o
         pers_error@errstat,           // r/o
         repres_error@errstat,         // r/o
         tbcorr@body,                  // r/o
         wdeff_bcorr@body,             // r/o
         biascorr,                     // possibly updated
         biascorr_fg,                  // possibly updated
         final_obs_error,              // r/o
         obs_error,                    // r/o

  FROM   timeslot_index,timeslot_index, index, hdr, body, errstat
  WHERE	 (obstype@hdr == 7)
    AND  (report_status.passive@hdr + report_status.blacklisted@hdr == 0)
    AND  ($ksensor == -1 OR sensor == $ksensor)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
