//
//-- ODB/SQL file 'new_thinn_robhdr_7.sql'
//
//   Last updated:  05-Mar-2003
//

READONLY;

SET $tslot = -1;

CREATE VIEW new_thinn_robhdr_7 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         body.len,                     // r/o
	     date,                         // r/o
	     time,                         // r/o
         codetype,                    // r/o
         instrument_type,              // r/o
         retrtype,               // r/o
         areatype,                    // r/o
         obstype,                      // r/o
         report_status UPDATED,               // possibly updated (in ECMA)
         report_event1 UPDATED,               // possibly updated (in ECMA)
         lat, lon,                     // r/o
         thinningkey[1:$NUMTHBOX],     // r/o
         thinningtimekey               // r/o
  FROM   timeslot_index, index, hdr
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  (obstype = $satem)
    AND  (codetype = $satem500)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
