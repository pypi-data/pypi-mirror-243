//
//-- ODB/SQL file 'satob_robhdr_1.sql'
//
//   Last updated:  02-Feb-2005
//

SET $tslot = -1;

CREATE VIEW satob_robhdr_1 AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         body.len  READONLY,           // r/o
         obstype,                      // r/o
         codetype,                     // r/o
         instrument_type,                     // r/o
         retrtype,                     // r/o
         areatype,                     // r/o
         report_rdbflag,                      // r/o
         report_status,                       // possibly updated (in ECMA)
         report_event1,                       // possibly updated (in ECMA)
         report_event2,                       // possibly updated (in ECMA)
         date,                         // r/o
         time,                         // r/o
         lat, lon,                     // r/o
         statid,                       // r/o
         stalt,                        // r/o
  FROM   timeslot_index, index, hdr
  WHERE	 (obstype = $satob)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
