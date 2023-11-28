//
//-- ODB/SQL file 'redun_robhdr_6.sql'
//
//   Last updated:  10-Apr-2014
//

READONLY;

SET $tslot = -1;

CREATE VIEW redun_robhdr_6 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         abnob, mapomm,                // r/o
         body.len,                     // r/o
         date,                         // r/o
         time,                         // r/o
         obstype,                      // r/o
         codetype,                     // r/o
         bufrtype@hdr,                 // r/o
         instrument_type,                     // r/o
         retrtype,                     // r/o
         areatype,                     // r/o
         report_status  UPDATED,              // possibly updated (in ECMA)
         report_event1  UPDATED,              // possibly updated (in ECMA)
         statid,                       // r/o
         trlat,                        // r/o
         trlon,                        // r/o
	 lat, lon,                     // r/o
 	 numlev,                       // r/o
  FROM   timeslot_index, index, hdr
  WHERE	 obstype IN ($temp, $pilot)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
