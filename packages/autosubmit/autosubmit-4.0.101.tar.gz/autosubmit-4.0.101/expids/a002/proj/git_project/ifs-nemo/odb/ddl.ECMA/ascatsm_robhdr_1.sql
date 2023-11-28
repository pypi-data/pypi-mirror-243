//
//-- ODB/SQL file 'ascatsm_robhdr_1.sql'
//
//   Last updated:  02-Feb-2005
//

SET $tslot = -1;
SET $codetype = -1;
SET $sensor = -1;

CREATE VIEW ascatsm_robhdr_1 AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         body.len,                     // r/o
         obstype,                      // r/o
         codetype,                     // r/o
         reportype,                    // r/o
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
  WHERE  obstype = $scatt
    AND  (($codetype == -1) OR (codetype == $codetype))
    AND  (($sensor == -1) OR (sensor == $sensor))
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
