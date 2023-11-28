//
//-- ODB/SQL file 'decis_robhdr_1.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY; // .. except those marked with  UPDATED

SET $kset = 0;
SET $tslot = -1;

CREATE VIEW decis_robhdr_1 AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         abnob, mapomm,                // r/o
         body.len,                     // r/o
	     obstype,                  // r/o
         codetype,                     // r/o
         instrument_type,                     // r/o
         retrtype,                     // r/o
         areatype,                     // r/o
	     date,                     // r/o
	     time,                     // r/o
         report_event1  UPDATED,              // possibly updated (in ECMA)
         report_status  UPDATED,              // possibly updated (in ECMA)
         report_rdbflag,                      // r/o
         stalt,                        // r/o
         trlat, trlon,                 // r/o
         lat,lon,
         orography,
  FROM   timeslot_index, index, hdr, modsurf
  WHERE	 (kset = $kset)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
