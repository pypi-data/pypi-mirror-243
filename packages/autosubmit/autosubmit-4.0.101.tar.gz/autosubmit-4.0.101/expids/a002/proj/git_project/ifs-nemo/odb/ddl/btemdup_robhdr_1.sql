//
//-- ODB/SQL file 'btemdup_robhdr_1.sql'
//
//   Last updated:  09-May-2017
//

READONLY;

SET $tslot = -1;

CREATE VIEW btemdup_robhdr_1 AS
  SELECT seqno,                        // r/o; MUST COME FIRST
         reportno,                     // r/o
         abnob, mapomm,                // r/o
         body.len,                     // r/o
         date,                         // r/o
         time,                         // r/o
         obstype,                      // r/o
         codetype,                     // r/o
         instrument_type,              // r/o
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
  ORDERBY reportno, date, time
;
