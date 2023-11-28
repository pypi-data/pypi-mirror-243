//
//-- ODB/SQL file 'pre_thinn_robhdr_8.sql'
//
//   Last updated:  13-Aug-2004
//


READONLY;

SET $tslot = -1;
SET $sensor = -1;

CREATE VIEW pre_thinn_robhdr_8 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         body.len,                     // r/o
         date,                         // r/o
         time,                         // r/o
         codetype,                     // r/o
         instrument_type@hdr,          // r/o
         obstype,                      // r/o
         report_status  UPDATED,       // possibly updated (in ECMA)
         report_event1  UPDATED,       // possibly updated (in ECMA)
         sensor,                       // r/o
         statid,                       // r/o
         trlat, trlon,                 // r/o
     	 lat, lon,                     // r/o
         thinningkey[1:$NUMTHBOX] UPDATED,      // u
         thinningtimekey UPDATED       // u
  FROM   timeslot_index, index, hdr
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  (obstype = $satem)
    AND  (codetype = $resat)
    AND  ($sensor == -1 OR sensor == $sensor)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
