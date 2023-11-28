//
//-- ODB/SQL file 'bay_thinn_robhdr.sql'
//
//   Last updated:  19-Dec-2017
//

READONLY;

SET $tslot = -1;
SET $ksensor = -1;

CREATE VIEW bay_thinn_robhdr AS
  SELECT seqno,                    // r/o; MUST BECOME FIRST
         body.len,                     // r/o
	     date,                     // r/o
	     time,                     // r/o
         codetype,                     // r/o
         instrument_type,              // r/o
         obstype,                      // r/o
         report_status  UPDATED,              // possibly updated (in ECMA)
         report_event1  UPDATED,              // possibly updated (in ECMA)
         sensor,                              // r/o
         thinningkey[1:$NUMTHBOX] UPDATED,      // u
         thinningtimekey UPDATED,              // u
         numlev UPDATED,                       // u
         numactiveb UPDATED,                   // u
  FROM   timeslot_index, index, hdr, sat
  WHERE	 (obstype@hdr == 7)
    AND  (report_status.passive@hdr + report_status.blacklisted@hdr == 0)
    AND  ($ksensor == -1 OR sensor == $ksensor)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
