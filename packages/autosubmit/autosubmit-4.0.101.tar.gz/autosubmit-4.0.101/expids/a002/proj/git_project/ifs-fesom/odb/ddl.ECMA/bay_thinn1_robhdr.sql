//
//-- ODB/SQL file 'bay_thinn1_robhdr.sql'
//
//   Last updated:  18-dec-2017
//

READONLY;

SET $tslot = -1;
SET $ksensor = -1;

CREATE VIEW bay_thinn1_robhdr AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         body.len,                     // r/o
             date,                     // r/o
             time,                     // r/o
         codetype,                     // r/o
         obstype,                      // r/o
         report_status  UPDATED,       // possibly updated (in ECMA)
         report_event1  UPDATED,       // possibly updated (in ECMA)
         sensor,                       // r/o
         trlat, trlon,                 // r/o
     	 lat, lon,                     // r/o
         scanline@radiance,            // r/o
         thinningkey[1:$NUMTHBOX] UPDATED,      // u
         thinningtimekey UPDATED,       // u
         numlev UPDATED,                       // u
         numactiveb UPDATED,                   // u
  FROM   timeslot_index, index, hdr, sat, radiance
  WHERE	 (report_status.passive@hdr + report_status.rejected@hdr + report_status.blacklisted@hdr == 0)
    AND  (obstype@hdr == 7)
    AND  ($ksensor == -1 OR sensor@hdr == $ksensor)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
