//
//-- ODB/SQL file 'post_thinn_robhdr_6.sql'
//
//   Last updated:  08-Nov-2007
//

READONLY;

SET $obstype = -1;
SET $codetype = -1;
SET $tslot = -1;

CREATE VIEW post_thinn_robhdr_6 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         body.len,                     // r/o
         date,                         // r/o
         time,                         // r/o
         codetype,                    // r/o
         instrument_type,              // r/o
         retrtype,               // r/o
         areatype,                    // r/o
         obstype,                      // r/o
         report_status  UPDATED,              // possibly updated (in ECMA)
         report_event1  UPDATED,              // possibly updated (in ECMA)
         trlat, trlon,                 // r/o
	     lat, lon                      // r/o
  FROM   timeslot_index, index, hdr
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  ( obstype = $obstype )
    AND  (codetype = $codetype)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
