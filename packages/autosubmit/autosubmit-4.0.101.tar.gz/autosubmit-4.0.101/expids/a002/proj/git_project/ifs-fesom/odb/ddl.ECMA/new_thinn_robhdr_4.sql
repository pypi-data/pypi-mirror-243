//
//-- ODB/SQL file 'new_thinn_robhdr_4.sql'
//
//   Last updated:  05-Mar-2003
//

READONLY;

SET $tslot = -1;
SET $sensor = -1;

CREATE VIEW new_thinn_robhdr_4 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         body.len,                     // r/o
	     date,                     // r/o
	     time,                     // r/o
         codetype,                     // r/o
         instrument_type,              // r/o
         retrtype,                     // r/o
         areatype,                     // r/o
         obstype,                      // r/o
         report_status  UPDATED,              // possibly updated (in ECMA)
         report_event1  UPDATED,              // possibly updated (in ECMA)
         sensor,                       // r/o
         gen_centre,                   // r/o
         comp_method,                  // r/o
         trlat, trlon,                 // r/o
     	 lat, lon,                     // r/o
         thinningkey[1:$NUMTHBOX],     // r/o
         thinningtimekey               // r/o
  FROM   timeslot_index, index, hdr, sat, satob
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  (obstype = $satob)
    AND  ((codetype =  88)
    OR    (codetype =  89))
    AND  ($sensor == -1 OR sensor == $sensor)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
