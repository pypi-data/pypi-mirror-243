//
//-- ODB/SQL file 'scat_robhdr_1.sql'
//
//   Last updated:  02-Apr-2010
//

SET $tslot = -1;
SET $codetype = -1;
SET $sensor = -1;

CREATE VIEW scat_robhdr_1 AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         body.len,                     // r/o
         obstype,                      // r/o
         codetype,                     // r/o
         instrument_type,                     // r/o
         retrtype,                     // r/o
         areatype,                     // r/o
         report_rdbflag,                      // r/o
         report_status,                       // possibly updated (in ECMA)
         report_event1,                       // possibly updated (in ECMA)
         report_event2,                       // possibly updated (in ECMA)
         gen_centre,                   // r/o
         date,                         // r/o
         time,                         // r/o
         lat, lon,                     // r/o
         statid,                       // r/o
         stalt,                        // r/o
  FROM   timeslot_index, index, hdr, sat
  WHERE         obstype = $scatt
    AND  (($codetype == -1) OR (codetype == $codetype))
    AND  (($sensor == -1) OR (sensor == $sensor))
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
