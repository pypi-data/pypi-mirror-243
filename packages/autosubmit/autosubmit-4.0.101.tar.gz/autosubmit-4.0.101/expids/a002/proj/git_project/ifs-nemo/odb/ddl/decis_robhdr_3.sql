//
//-- ODB/SQL file 'decis_robhdr_3.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY; // .. except those marked with  UPDATED

SET $tslot = -1;

CREATE VIEW decis_robhdr_3 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         abnob, mapomm,                // r/o
         body.len,                     // r/o
	     date,                     // r/o
	     time,                     // r/o
         codetype,                     // r/o
         instrument_type,                     // r/o
         retrtype,                     // r/o
         areatype,                     // r/o
         report_status  UPDATED,              // possibly updated (in ECMA)
         statid,                       // r/o
         lat, lon,                     // r/o
  FROM   timeslot_index, index, hdr
  WHERE	 (obstype = $airep)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
