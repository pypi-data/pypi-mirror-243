//
//-- ODB/SQL file 'post_thinn_robhdr_3.sql'
//
//   Last updated:  31-Mar-2010
//

READONLY;

SET $tslot = -1;

CREATE VIEW post_thinn_robhdr_3 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         body.len,                     // r/o
         date,                         // r/o
         time,                         // r/o
         codetype,                    // r/o
         instrument_type,              // r/o
         sensor,                 // r/o
         retrtype,               // r/o
         areatype,                    // r/o
         obstype,                      // r/o
         report_status  UPDATED,              // possibly updated (in ECMA)
         report_event1  UPDATED,              // possibly updated (in ECMA)
         trlat, trlon,                 // r/o
	     lat, lon                      // r/o
  FROM   timeslot_index, index, hdr
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  (obstype = $satem)
    AND  (codetype = $tcwc)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
