//
//-- ODB/SQL file 'redun_robhdr_7.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

SET $tslot = -1;

CREATE VIEW redun_robhdr_7 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         abnob, mapomm,                // r/o
         body.len,                     // r/o
         date,                         // r/o
         time,                         // r/o
         obstype,                      // r/o
         report_status  UPDATED,              // possibly updated (in ECMA)
         statid,                       // r/o
         lat, lon,                     // r/o
         trlat, trlon,                 // r/o
  FROM   timeslot_index, index, hdr
  WHERE	 obstype IN ($temp, $synop)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
