//
//-- ODB/SQL file 'redun_robhdr_1.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

SET $tslot = -1;

CREATE VIEW redun_robhdr_1 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         abnob, mapomm,                // r/o
         body.len,                     // r/o
	     date,                     // r/o
	     time,                     // r/o
         codetype,                     // r/o
         instrument_type,                     // r/o
         retrtype,                     // r/o
         areatype,                     // r/o
         obstype,                      // r/o
         report_event1  UPDATED,              // possibly updated (in ECMA)
         report_status  UPDATED,              // possibly updated (in ECMA)
         lat, lon,                     // r/o
         statid,                       // r/o
         stalt,                        // r/o
  FROM   timeslot_index, index, hdr
  WHERE	 obstype IN ($synop, $paob)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
