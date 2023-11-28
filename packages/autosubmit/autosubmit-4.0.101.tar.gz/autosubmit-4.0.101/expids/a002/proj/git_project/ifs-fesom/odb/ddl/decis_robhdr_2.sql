//
//-- ODB/SQL file 'decis_robhdr_2.sql'
//
//   Last updated: 27-Apr-2015
//

READONLY; // .. except those marked with  UPDATED

SET $kset = 0;
SET $tslot = -1;

CREATE VIEW decis_robhdr_2 AS
  SELECT seqno,                        // r/o; MUST COME FIRST
         abnob, mapomm,                // r/o
         body.len,                     // r/o
         obstype,                      // r/o
         codetype,                     // r/o
         reportype,                    // r/o
         instrument_type,              // r/o
         retrtype,                     // r/o
         areatype,                     // r/o
	     date,                     // r/o
	     time,                     // r/o
         report_event1  UPDATED,       // possibly updated (in ECMA)
         report_status  UPDATED,       // possibly updated (in ECMA)
         report_rdbflag,               // r/o
         sensor,                       // r/o
         stalt  UPDATED,               // possibly updated (in ECMA)
         lat, lon,                     // r/o
         statid,                       // r/o
  FROM   timeslot_index, index, hdr
  WHERE	 (kset = $kset)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
